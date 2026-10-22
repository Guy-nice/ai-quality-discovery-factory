"""R16 analysis: AI vs non-AI merged PRs in pilot code. Writes data/aggregates/r16-ai-prs.csv and prints a summary.
Needs data/db/git_history.sqlite (gunzip -k git_history.sqlite.gz).
"""
import csv, datetime as dt, json, math, os, re, sqlite3, statistics as st

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")
OUT = os.path.join(ROOT, "data", "aggregates", "r16-ai-prs.csv")
TEST = re.compile(r"(^|/)(tests?|__tests__|spec|e2e|integration-tests?)(/|$)|(Tests?|_test|\.test|\.spec|Spec)\.[A-Za-z]+$|Tests?/|\.Tests?(/|\.)", re.I)
END = "2026-10-22"
FOLLOW_DAYS = 30


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def quarter(s):
    return f"{s[:4]}-Q{(int(s[5:7]) - 1) // 3 + 1}"


def bucket(lines):
    return "<=50" if lines <= 50 else "51-200" if lines <= 200 else "201-1000" if lines <= 1000 else ">1000"


def mh_rr(strata):
    """Mantel-Haenszel risk ratio over strata of (a, n1, c, n0); Greenland-Robins 95% CI."""
    num = den = P = R = S = 0.0
    for a, n1, c, n0 in strata:
        N = n1 + n0
        if N == 0 or n1 == 0 or n0 == 0:
            continue
        num += a * n0 / N
        den += c * n1 / N
        P += (n1 * n0 * (a + c) - a * c * N) / N ** 2
        R += a * n0 / N
        S += c * n1 / N
    if num == 0 or den == 0:
        return None, None, None
    rr = num / den
    se = math.sqrt(P / (R * S))
    return rr, rr * math.exp(-1.96 * se), rr * math.exp(1.96 * se)


def main():
    db = sqlite3.connect(DB)
    db.execute("ATTACH DATABASE ? AS gh", (os.path.join(ROOT, "data", "db", "git_history.sqlite"),))
    hot = [(r, p) for r, p in db.execute("SELECT repo, path FROM r3_dir_hotspots WHERE level='dir' AND is_test_path=0 ORDER BY score DESC LIMIT 20")]
    hot10 = hot[:10]
    pr_files = {}
    for repo, num, path in db.execute("""SELECT c.repo, c.pr_number, f.path FROM pr_commits c JOIN gh.git_file_changes f ON f.repo=c.repo AND f.sha=c.sha WHERE c.pr_number IS NOT NULL"""):
        pr_files.setdefault((repo, num), set()).add(path)
    flags = {(r, s): (cf, ca) for r, s, cf, ca in db.execute("SELECT repo, sha, cfb_fix, causing FROM r3_commit_flags")}
    sha_pr = {(r, s): n for r, s, n in db.execute("SELECT repo, sha, pr_number FROM pr_commits")}
    causing_keys = {k for (k,) in db.execute("SELECT DISTINCT causing_key FROM causal_links")}
    # CFB-fix commits with their files and dates
    fixes = []
    for repo, sha, date in db.execute("SELECT repo, sha, date FROM r3_commit_flags WHERE cfb_fix=1 AND date >= '2025-01-01'"):
        files = {p for (p,) in db.execute("SELECT path FROM gh.git_file_changes WHERE repo=? AND sha=?", (repo, sha))}
        fixes.append((repo, sha_pr.get((repo, sha)), date, files))
    pr_shas = {}
    for repo, sha, n in db.execute("SELECT repo, sha, pr_number FROM pr_commits WHERE pr_number IS NOT NULL"):
        pr_shas.setdefault((repo, n), []).append(sha)

    prs = []
    for repo, num, created, merged, adds, dels, ai, pct, reviews, threads, reviewers, keys in db.execute(
            "SELECT repo, number, created, merged, adds, dels, ai_flag, ai_pct, reviews, review_threads, reviewers, jira_keys FROM prs WHERE merged >= '2025-01-01'"):
        files = pr_files.get((repo, num), set())
        lines = (adds or 0) + (dels or 0)
        t = ts(merged)
        follow = None
        if (ts(END + "T00:00:00+00:00") - t).days >= FOLLOW_DAYS:
            follow = 0
            for frepo, fpr, fdate, ffiles in fixes:
                if frepo != repo or fpr == num:
                    continue
                d = ts(fdate + "T12:00:00+00:00" if len(fdate) == 10 else fdate)
                if 0 < (d - t).total_seconds() <= FOLLOW_DAYS * 86400 and files & ffiles:
                    follow = 1
                    break
        causing = int(bool(set(json.loads(keys or "[]")) & causing_keys) or any(flags.get((repo, s), (0, 0))[1] for s in pr_shas.get((repo, num), [])))
        tests = int(any(TEST.search(p) for p in files))
        in_hot = int(any(r == repo and any(p.startswith(h + "/") for p in files) for r, h in hot))
        in_hot10 = int(any(r == repo and any(p.startswith(h + "/") for p in files) for r, h in hot10))
        db.execute("UPDATE prs SET touches_tests=?, touches_hotspot=? WHERE repo=? AND number=?", (tests, in_hot, repo, num))
        prs.append(dict(repo=repo, q=quarter(merged), ai=ai, pct=pct, lines=lines, bucket=bucket(lines), reviews=reviews or 0,
                        threads=threads or 0, reviewers=reviewers or 0, hours=(t - ts(created)).total_seconds() / 3600,
                        tests=tests, hot=in_hot, hot10=in_hot10, follow=follow, causing=causing))
    db.commit()

    rows = []
    for q in sorted({p["q"] for p in prs}):
        for grp, ai in (("ai", 1), ("non-ai", 0)):
            g = [p for p in prs if p["q"] == q and p["ai"] == ai]
            if not g:
                continue
            lines = sum(p["lines"] for p in g)
            f = [p for p in g if p["follow"] is not None]
            rows.append(dict(section="quarter", quarter=q, group=grp, n=len(g), ai_share_pct=None,
                             median_lines=st.median(p["lines"] for p in g),
                             reviews_per_pr=round(sum(p["reviews"] for p in g) / len(g), 2),
                             no_reviewer_pct=round(100 * sum(1 for p in g if p["reviewers"] == 0) / len(g), 1),
                             threads_per_100_lines=round(100 * sum(p["threads"] for p in g) / lines, 2) if lines else None,
                             median_hours_to_merge=round(st.median(p["hours"] for p in g), 1),
                             touches_tests_pct=round(100 * sum(p["tests"] for p in g) / len(g), 1),
                             touches_hotspot_pct=round(100 * sum(p["hot"] for p in g) / len(g), 1),
                             followup_fix_pct=round(100 * sum(p["follow"] for p in f) / len(f), 1) if f else None,
                             causing_pct=round(100 * sum(p["causing"] for p in g) / len(g), 1)))
        allq = [p for p in prs if p["q"] == q]
        h10 = [p for p in allq if p["hot10"]]
        rows.append(dict(section="ai_share", quarter=q, group="all-prs", n=len(allq), ai_share_pct=round(100 * sum(p["ai"] for p in allq) / len(allq), 1)))
        if h10:
            rows.append(dict(section="ai_share", quarter=q, group="top10-hotspot-prs", n=len(h10), ai_share_pct=round(100 * sum(p["ai"] for p in h10) / len(h10), 1)))

    def rr(outcome, sub):
        strata = []
        for b in ("<=50", "51-200", "201-1000", ">1000"):
          for h in (0, 1):
            s = [p for p in sub if p["bucket"] == b and p["hot"] == h and p[outcome] is not None]
            a = sum(p[outcome] for p in s if p["ai"]); n1 = sum(1 for p in s if p["ai"])
            c = sum(p[outcome] for p in s if not p["ai"]); n0 = sum(1 for p in s if not p["ai"])
            strata.append((a, n1, c, n0))
        return strata, mh_rr(strata)

    w26 = [p for p in prs if p["q"] >= "2026"]
    summary = {}
    for outcome in ("follow", "causing", "tests"):
        for label, sub in (("2025-2026", prs), ("2026", w26)):
            strata, (r, lo, hi) = rr(outcome, sub)
            a = sum(s[0] for s in strata); n1 = sum(s[1] for s in strata); c = sum(s[2] for s in strata); n0 = sum(s[3] for s in strata)
            summary[(outcome, label)] = (r, lo, hi, a, n1, c, n0)
            rows.append(dict(section="rate_ratio_size_hotspot_adjusted", quarter=label, group=outcome, n=n1 + n0,
                             ai_events=a, ai_n=n1, nonai_events=c, nonai_n=n0,
                             rr=round(r, 2) if r else None, ci_low=round(lo, 2) if lo else None, ci_high=round(hi, 2) if hi else None))
    cols = ["section", "quarter", "group", "n", "ai_share_pct", "median_lines", "reviews_per_pr", "no_reviewer_pct", "threads_per_100_lines",
            "median_hours_to_merge", "touches_tests_pct", "touches_hotspot_pct", "followup_fix_pct", "causing_pct",
            "ai_events", "ai_n", "nonai_events", "nonai_n", "rr", "ci_low", "ci_high"]
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) for k in cols})
    print("PRs", len(prs), "AI", sum(p["ai"] for p in prs))
    for k, v in summary.items():
        print(k, v)
    for r in rows:
        if r["section"] != "rate_ratio_size_hotspot_adjusted":
            print({k: v for k, v in r.items() if v is not None})


if __name__ == "__main__":
    main()
