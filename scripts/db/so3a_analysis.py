"""SO-3A analysis: pass rate, flakiness, top failing tests, failure classes, owners, quarantine effect.

Writes data/aggregates/so3a-e2e.csv (section,key,metric,value) and prints a summary.
"""
import collections, csv, datetime, os, sqlite3, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")
OUT = os.path.join(ROOT, "data", "aggregates", "so3a-e2e.csv")
CLONES = os.path.join(ROOT, "data", "raw", "git")

db = sqlite3.connect(DB, timeout=60)
rows = []
add = lambda sec, key, met, val: rows.append((sec, key, met, val))

# 1. Pass rate per workflow (completed runs; cancelled/skipped excluded from denominator but counted)
wf = db.execute("""SELECT repo, workflow, COUNT(*),
  SUM(conclusion='success'), SUM(conclusion='failure'), SUM(conclusion IN ('cancelled','skipped')),
  SUM(conclusion='timed_out'), MIN(created), MAX(created)
  FROM ci_runs GROUP BY 1,2 ORDER BY 3 DESC""").fetchall()
print("workflow | runs | pass% (success/(success+failure+timed_out)) | cancelled")
for repo, w, n, ok, fail, canc, to, lo, hi in wf:
    dec = (ok or 0) + (fail or 0) + (to or 0)
    pr = round(100 * ok / dec, 1) if dec else None
    add("pass_rate", f"{repo}/{w}", "runs", n); add("pass_rate", f"{repo}/{w}", "pass_pct", pr)
    add("pass_rate", f"{repo}/{w}", "cancelled", canc)
    print(f"{repo}/{w} | {n} | {pr} | {canc}")

# weekly pass rate, last 12 weeks, main suites
MAIN = ["Run test suites", "E2E cluster run", "VFM-AFM Automated Test Pipeline", "Integration Tests with BU Profiles"]
for w in MAIN:
    wk = db.execute("""SELECT strftime('%Y-%W', created) wk, SUM(conclusion='success'), SUM(conclusion IN ('failure','timed_out'))
      FROM ci_runs WHERE workflow=? GROUP BY 1 ORDER BY 1 DESC LIMIT 12""", (w,)).fetchall()
    for k, ok, f in wk:
        if (ok or 0) + (f or 0):
            add("weekly_pass", f"{w}|{k}", "pass_pct", round(100 * ok / (ok + f), 1))

# 2. Flaky: same workflow + head_sha has both failure and success (re-run or re-trigger)
fl = db.execute("""SELECT workflow, COUNT(*), SUM(has_f AND has_s) FROM (
   SELECT workflow, head_sha, MAX(conclusion IN ('failure','timed_out')) has_f, MAX(conclusion='success') has_s
   FROM ci_runs WHERE head_sha IS NOT NULL GROUP BY 1,2 HAVING COUNT(*)>1) GROUP BY 1""").fetchall()
for w, shas, flaky in fl:
    add("flaky_sha", w, "multi_run_shas", shas); add("flaky_sha", w, "fail_and_pass_same_sha", flaky)
retry = db.execute("SELECT workflow, SUM(attempt>1), COUNT(*) FROM ci_runs GROUP BY 1").fetchall()
for w, r, n in retry:
    add("reattempt", w, "runs_with_attempt_gt1", r)

# 3. Failure classes (per failed run: primary class = most common among its rows)
cls = db.execute("""SELECT r.workflow, t.run_id, t.error_class FROM test_failures t JOIN ci_runs r USING(run_id) WHERE t.error_class != 'flaky (passed on retry)'""").fetchall()
per_run = collections.defaultdict(collections.Counter)
for w, rid, c in cls:
    per_run[(w, rid)][c] += 1
cls_count = collections.defaultdict(collections.Counter)
for (w, rid), cnt in per_run.items():
    cls_count[w][cnt.most_common(1)[0][0]] += 1
for w, cnt in cls_count.items():
    tot = sum(cnt.values())
    for c, n in cnt.items():
        add("failure_class", f"{w}|{c}", "share_pct", round(100 * n / tot, 1))
    print("classes", w, dict(cnt))

# 4. Top failing tests: count of failed runs (of parsed) that list the test
tt = db.execute("""SELECT r.workflow, t.test, COUNT(DISTINCT t.run_id), GROUP_CONCAT(DISTINCT t.error_class)
  FROM test_failures t JOIN ci_runs r USING(run_id) WHERE t.test NOT LIKE '(run-level%' AND t.error_class != 'flaky (passed on retry)'
  GROUP BY 1,2 ORDER BY 3 DESC LIMIT 20""").fetchall()
parsed = dict(db.execute("SELECT r.workflow, COUNT(DISTINCT t.run_id) FROM test_failures t JOIN ci_runs r USING(run_id) GROUP BY 1").fetchall())
for w, t, n, c in tt:
    add("top_test", f"{w}|{t}", "failed_runs", n); add("top_test", f"{w}|{t}", "class", c)
print("top tests:"); [print(" ", w, "|", t[:110], "|", n, "|", c) for w, t, n, c in tt]

fk = db.execute("""SELECT r.workflow, COUNT(*), COUNT(DISTINCT t.test) FROM test_failures t JOIN ci_runs r USING(run_id) WHERE t.error_class='flaky (passed on retry)' GROUP BY 1""").fetchall()
for w, n, d in fk:
    add("flaky_tests", w, "flaky_occurrences", n); add("flaky_tests", w, "distinct_flaky_tests", d)
    print("flaky tests", w, n, d)
dist = db.execute("""SELECT r.workflow, COUNT(DISTINCT t.run_id), COUNT(*), COUNT(DISTINCT t.test), MAX(c) FROM test_failures t JOIN ci_runs r USING(run_id)
   JOIN (SELECT test tt, COUNT(DISTINCT run_id) c FROM test_failures GROUP BY 1) x ON x.tt=t.test WHERE t.error_class != 'flaky (passed on retry)' AND t.test NOT LIKE '(run-level%' GROUP BY 1""").fetchall()
for w, runs, occ, d, mx in dist:
    add("failed_tests", w, "runs_with_named_failures", runs); add("failed_tests", w, "distinct_failed_tests", d); add("failed_tests", w, "max_runs_per_test", mx)
    print("failed tests", w, runs, occ, d, mx)

# 5. Quarantine effect per workflow: runs whose ONLY failing tests are in the quarantine set (top N) would pass
def quarantine_effect(w, N=10):
    q = [t for (t,) in db.execute("""SELECT t.test FROM test_failures t JOIN ci_runs r USING(run_id)
        WHERE r.workflow=? AND t.test NOT LIKE '(run-level%' AND t.error_class != 'flaky (passed on retry)' GROUP BY 1 ORDER BY COUNT(DISTINCT run_id) DESC LIMIT ?""", (w, N))]
    runs = collections.defaultdict(set)
    for rid, t in db.execute("SELECT t.run_id, t.test FROM test_failures t JOIN ci_runs r USING(run_id) WHERE r.workflow=? AND t.error_class != 'flaky (passed on retry)'", (w,)):
        runs[rid].add(t)
    if not runs:
        return q, None
    saved = sum(1 for ts in runs.values() if ts and ts <= set(q))
    return q, saved / len(runs)

for w in MAIN:
    q, frac = quarantine_effect(w)
    ok, f = db.execute("SELECT SUM(conclusion='success'), SUM(conclusion IN ('failure','timed_out')) FROM ci_runs WHERE workflow=?", (w,)).fetchone()
    if not (ok or f) or frac is None:
        continue
    now = ok / (ok + f)
    after = (ok + f * frac) / (ok + f)
    add("quarantine", w, "pass_pct_now", round(100 * now, 1))
    add("quarantine", w, "failed_runs_fixed_by_top10_quarantine_pct", round(100 * frac, 1))
    add("quarantine", w, "pass_pct_after_top10_quarantine", round(100 * after, 1))
    print(f"quarantine {w}: now {now:.1%} -> {after:.1%} (top-10 tests fix {frac:.0%} of failed runs)")

# 6. Owners of failing test files (active authors last 6 months), from clones if present
def owners(repo, path):
    d = os.path.join(CLONES, repo)
    if not os.path.isdir(d):
        return None
    out = subprocess.run(["git", "-C", d, "log", "--since=6 months ago", "--format=%an", "--", path], capture_output=True, text=True).stdout.split("\n")
    c = collections.Counter(a for a in out if a)
    return ", ".join(f"{a} ({n})" for a, n in c.most_common(2)) or "none active"

for w, t, n, c in tt[:10]:
    repo = "acd-playwright-e2e" if t.startswith("e2e/") else "routing-ng-integration-tests"
    path = t.split(" > ")[0] if t.startswith("e2e/") else "src"
    o = owners(repo, path)
    if o is not None:
        add("owner", f"{w}|{t}", "active_authors_6m", o)

with open(OUT, "w", newline="") as f:
    wr = csv.writer(f); wr.writerow(["section", "key", "metric", "value"]); wr.writerows(rows)
print("rows", len(rows))

# 7. Expected pass rate if env-type failures are removed (primary class per failed run, parsed sample applied to all failures)
ENV = {"setup/credentials", "test data/fixture", "env/infra", "no log available"}
ENV_T = ENV | {"timeout"}
extra = []
for w in MAIN:
    ok, f = db.execute("SELECT SUM(conclusion='success'), SUM(conclusion IN ('failure','timed_out')) FROM ci_runs WHERE workflow=?", (w,)).fetchone()
    cnt = cls_count.get(w)
    if not cnt or not (ok or f):
        continue
    tot = sum(cnt.values())
    for label, S in (("env_fixed", ENV), ("env_and_timeout_fixed", ENV_T)):
        share = sum(n for c, n in cnt.items() if c in S) / tot
        exp = (ok + f * share) / (ok + f)
        extra.append(("expected_pass", f"{w}|{label}", "pass_pct", round(100 * exp, 1)))
        print(f"expected {w} {label}: {100*exp:.1f}% (env share of failures {share:.0%})")
with open(OUT, "a", newline="") as fh:
    csv.writer(fh).writerows(extra)
