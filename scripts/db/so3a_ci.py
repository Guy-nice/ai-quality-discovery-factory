"""SO-3A: ingest GitHub Actions runs / jobs / failed test names for pilot E2E and integration workflows.

Read-only (gh api GET, gh run view --log-failed). Stores only run metadata, job conclusions,
test names and a short error class; no log text.
Usage: python3 -I scripts/db/so3a_ci.py [runs|jobs|tests|all]
"""
import datetime, json, os, re, sqlite3, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")
ORG = "inContact"
SINCE = "2026-04-25"
CAP = 1000
JOBS_PER_WF = 100
FAILED_LOGS_PER_WF = 30

WORKFLOWS = [
    ("acd-playwright-e2e", 342256537, "E2E cluster run"),
    ("acd-playwright-e2e", 342279436, "E2E lab suites"),
    ("acd-playwright-e2e", 347646183, "Run test suites"),
    ("acd-playwright-e2e", 386835691, "Run AOR suite"),
    ("acd-playwright-e2e", 376621589, "Run DE suite"),
    ("acd-playwright-e2e", 376852112, "Run EM suite"),
    ("acd-playwright-e2e", 392003600, "UIQ end-to-end"),
    ("routing-ng-integration-tests", 71429687, "VFM-AFM Automated Test Pipeline"),
    ("routing-ng-integration-tests", 263609364, "Integration Tests with BU Profiles"),
    ("routing-ng-integration-tests", 371757145, "Unit Tests"),
    ("routing-ng-advanced-findmatch", 60011475, "test"),
    ("routing-ng-contact-retry", 88791239, "test"),
    ("routing-ng-agent-capacity-service", 186274941, "test"),
]
LOG_WORKFLOWS = {342256537, 342279436, 347646183, 71429687, 263609364}

SCHEMA = """
CREATE TABLE IF NOT EXISTS ci_runs (repo TEXT, workflow TEXT, workflow_id INTEGER, run_id INTEGER PRIMARY KEY,
  created TEXT, conclusion TEXT, attempt INTEGER, branch TEXT, event TEXT, duration_s INTEGER, head_sha TEXT);
CREATE TABLE IF NOT EXISTS ci_jobs (run_id INTEGER, job TEXT, conclusion TEXT, PRIMARY KEY (run_id, job));
CREATE TABLE IF NOT EXISTS test_failures (run_id INTEGER, test TEXT, error_class TEXT, PRIMARY KEY (run_id, test));
"""


def gh(args, check=True):
    r = subprocess.run(["gh"] + args, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(r.stderr[:300])
    return r.stdout


def secs(a, b):
    try:
        f = lambda s: datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
        return int((f(b) - f(a)).total_seconds())
    except Exception:
        return None


def ingest_runs(db):
    for repo, wid, name in WORKFLOWS:
        n, page = 0, 1
        while n < CAP:
            out = gh(["api", f"repos/{ORG}/{repo}/actions/workflows/{wid}/runs?per_page=100&page={page}&created=>={SINCE}"], check=False)
            try:
                runs = json.loads(out).get("workflow_runs", [])
            except json.JSONDecodeError:
                break
            if not runs:
                break
            for r in runs:
                db.execute("INSERT OR REPLACE INTO ci_runs VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                           (repo, name, wid, r["id"], r["created_at"], r.get("conclusion"), r.get("run_attempt"),
                            r.get("head_branch"), r.get("event"), secs(r.get("run_started_at") or r["created_at"], r["updated_at"]),
                            r.get("head_sha")))
                n += 1
            page += 1
        db.commit()
        print(f"{repo}/{name}: {n} runs")


def ingest_jobs(db):
    for repo, wid, name in WORKFLOWS:
        ids = [r[0] for r in db.execute("SELECT run_id FROM ci_runs WHERE workflow_id=? AND conclusion IS NOT NULL ORDER BY created DESC LIMIT ?", (wid, JOBS_PER_WF))]
        for rid in ids:
            out = gh(["api", f"repos/{ORG}/{repo}/actions/runs/{rid}/jobs?per_page=100", "--jq", "[.jobs[]|{name,conclusion}]"], check=False)
            try:
                for j in json.loads(out or "[]"):
                    db.execute("INSERT OR REPLACE INTO ci_jobs VALUES (?,?,?)", (rid, j["name"][:200], j.get("conclusion")))
            except json.JSONDecodeError:
                pass
        db.commit()
        print(f"jobs {repo}/{name}: {len(ids)} runs")


GRADLE = re.compile(r"^\s*(\w+) > (.+?) > com\.[\w.]+\.(.+?) FAILED\s*$")
PWT = re.compile(r"^\s*(?:\d+\)\s+)?(?:\[[^\]]+\]\s+›\s+)?(e2e/[^\s:]+\.spec\.ts):\d+:\d+ › (.+?)\s*[─\-]*\s*$")
SUMMARY = re.compile(r"^\s*(\d+) (failed|flaky|did not run|skipped|passed|interrupted)\b")
PROGRESS = re.compile(r"^\s*\[\d+/\d+\]")
EMAIL = re.compile(r"[\w.+-]+@[\w.-]+")


def err_class(text):
    t = text.lower()
    if re.search(r"login failed|access_denied|credential|password|401|403|secret .*not set|codeartifact role", t):
        return "setup/credentials"
    if re.search(r"not found\. available|must hold|rejected: |missing required fi|fixture|already exists|shared-state restore|is not stopped before this test", t):
        return "test data/fixture"
    if re.search(r"runner has received a shutdown|operation was canceled|no space left|econnrefused|enotfound|forcibly closed|server_error|systemerror|503|502|kafka|broker|unavailable|cluster", t):
        return "env/infra"
    if re.search(r"did not reach|did not go|not published within|no \w+event .* reached|never reached|still running|is not stopped", t):
        return "async state wait"
    if re.search(r"timeout|timed out|exceeded", t):
        return "timeout"
    if re.search(r"expect\(|assert|expected", t):
        return "assertion"
    if re.search(r"unmappable character|compil|build failure", t):
        return "build"
    return "other"


def clean_lines(log):
    out = []
    for l in log.splitlines():
        l = re.sub(r"^\S*Z\s", "", l.split("\t", 2)[-1])
        if "[36;1m" in l:
            continue
        out.append(l)
    return out


def ingest_tests(db):
    for repo, wid, name in WORKFLOWS:
        if wid not in LOG_WORKFLOWS:
            continue
        ids = [r[0] for r in db.execute("SELECT run_id FROM ci_runs WHERE workflow_id=? AND conclusion='failure' ORDER BY created DESC LIMIT ?", (wid, FAILED_LOGS_PER_WF))]
        for rid in ids:
            db.execute("DELETE FROM test_failures WHERE run_id=?", (rid,))
            L = clean_lines(gh(["run", "view", str(rid), "-R", f"{ORG}/{repo}", "--log-failed"], check=False))
            found = {}
            mode = None
            for i, l in enumerate(L):
                m = GRADLE.search(l)
                if m:
                    test = EMAIL.sub("<email>", f"{m.group(1)} > {m.group(2)} > {m.group(3)}")[:250]
                    ctx = " ".join(x for x in L[i:i + 40] if re.search(r"Error|FAILURE|expected|Timeout|##\[error\]", x))
                    found.setdefault(test, err_class(ctx))
                    continue
                h = SUMMARY.match(l)
                if h:
                    mode = h.group(2)
                    continue
                if mode in ("failed", "flaky"):
                    pm = PWT.search(l)
                    if pm and not PROGRESS.search(l):
                        title = pm.group(2)
                        test = EMAIL.sub("<email>", f"{pm.group(1)} > {title}")[:250]
                        if mode == "flaky":
                            found.setdefault(test, "flaky (passed on retry)")
                        else:
                            j = next((k for k, x in enumerate(L) if title[:60] in x and k < i), None)
                            ctx = " ".join(x for x in L[j:j + 60] if re.search(r"Error|expected|Timeout", x)) if j is not None else ""
                            found.setdefault(test, err_class(ctx))
                    elif l.strip() == "" or not l.startswith(" "):
                        mode = None
            if not L:
                found["(run-level: no test name)"] = "no log available"
            if not found:
                errs = " ".join(x for x in L if "##[error]" in x or x.strip().startswith("Error:"))
                found["(run-level: no test name)"] = err_class(errs or " ".join(L[-100:]))
            for t, c in found.items():
                db.execute("INSERT OR REPLACE INTO test_failures VALUES (?,?,?)", (rid, t, c))
        db.commit()
        print(f"tests {repo}/{name}: {len(ids)} failed runs parsed")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    db = sqlite3.connect(DB, timeout=60)
    db.executescript(SCHEMA)
    if mode in ("runs", "all"):
        ingest_runs(db)
    if mode in ("jobs", "all"):
        ingest_jobs(db)
    if mode in ("tests", "all"):
        ingest_tests(db)
