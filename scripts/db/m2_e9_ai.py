"""M2-E9: AI role, stronger designs. Writes tables ai_matched, ai_event_study, ai_mechanisms and data/aggregates/m2-e9-ai.csv.

Needs data/db/git_history.sqlite (gunzip -k git_history.sqlite.gz) and raw_local.sqlite (MI exclusion).
Run from repo root: python3 -I scripts/db/m2_e9_ai.py
"""
import collections
import csv
import datetime as dt
import glob
import json
import math
import os
import re
import sqlite3
import statistics as st

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")
OUT = os.path.join(ROOT, "data", "aggregates", "m2-e9-ai.csv")
END = dt.datetime(2026, 10, 25, tzinfo=dt.timezone.utc)
MI = re.compile(r"^\s*\[?\s*MI\b|investigatory ki|\bMI[- ]?\d{3,}|major incident", re.I)
INVALID = {"cannot reproduce", "not a bug", "won't do", "duplicate", "won't fix", "works as designed", "invalid"}
TEST = re.compile(r"(^|/)(tests?|__tests__|spec|e2e|integration-tests?)(/|$)|(Tests?|_test|\.test|\.spec|Spec)\.[A-Za-z]+$|Tests?/|\.Tests?(/|\.)", re.I)


def ts(s):
    s = s.replace("Z", "+00:00")
    if len(s) == 10:
        s += "T12:00:00+00:00"
    d = dt.datetime.fromisoformat(s)
    return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)


def bucket(n):
    return "<=50" if n <= 50 else "51-200" if n <= 200 else "201-1000" if n <= 1000 else ">1000"


def mh_rr(strata):
    num = den = P = R = S = 0.0
    used = 0
    for a, n1, c, n0 in strata:
        N = n1 + n0
        if n1 == 0 or n0 == 0:
            continue
        used += 1
        num += a * n0 / N
        den += c * n1 / N
        P += (n1 * n0 * (a + c) - a * c * N) / N ** 2
        R += a * n0 / N
        S += c * n1 / N
    if num == 0 or den == 0:
        return None, None, None, used
    rr = num / den
    se = math.sqrt(P / (R * S))
    return rr, rr * math.exp(-1.96 * se), rr * math.exp(1.96 * se), used


def poisson_ratio(a, ta, b, tb):
    if not (a and b and ta and tb):
        return None, None, None
    r = (a / ta) / (b / tb)
    se = math.sqrt(1 / a + 1 / b)
    return r, r * math.exp(-1.96 * se), r * math.exp(1.96 * se)


def main():
    db = sqlite3.connect(DB)
    db.execute("ATTACH DATABASE ? AS gh", (os.path.join(ROOT, "data", "db", "git_history.sqlite"),))
    db.execute("ATTACH DATABASE ? AS r", (os.path.join(ROOT, "data", "db", "raw_local.sqlite"),))

    # Valid, non-MI customer-found bugs (D-032)
    cfb = {}
    for key, created, res, team, summ in db.execute(
            "SELECT i.key, i.created, i.resolution, i.team, t.summary FROM issues i "
            "LEFT JOIN r.issue_text t ON t.key = i.key WHERE i.is_cfb = 1"):
        if summ and MI.search(summ):
            continue
        if res and res.lower() in INVALID:
            continue
        cfb[key] = (created, team)

    issue_team = {k: t for k, t in db.execute("SELECT key, team FROM issues WHERE team IS NOT NULL")}

    # Fix commits: message names a valid non-MI CFB
    fixes = collections.defaultdict(list)  # repo -> [(date, files, sha)]
    pr_of = {(r_, s): n for r_, s, n in db.execute("SELECT repo, sha, pr_number FROM pr_commits")}
    files_of = collections.defaultdict(set)
    for repo, sha, path in db.execute("SELECT repo, sha, path FROM gh.git_file_changes"):
        files_of[(repo, sha)].add(path)
    commits_month = collections.Counter()
    fix_month = collections.Counter()
    for repo, sha, date, keys, bot, merge in db.execute(
            "SELECT repo, sha, date, msg_keys, is_bot, is_merge FROM git_commits WHERE date >= '2024-07-01'"):
        if bot or merge:
            continue
        commits_month[(repo, date[:7])] += 1
        ks = set(json.loads(keys or "[]"))
        if ks & cfb.keys():
            fixes[repo].append((ts(date), files_of[(repo, sha)], sha))
            fix_month[(repo, date[:7])] += 1

    # Hotspots and owners
    hot = [(r_, p) for r_, p in db.execute(
        "SELECT repo, path FROM r3_dir_hotspots WHERE level='dir' AND is_test_path=0 ORDER BY pilot_fix_24m DESC LIMIT 10")]
    owners = collections.defaultdict(set)
    for repo, path, login in db.execute("SELECT repo, path, login FROM so45_owners WHERE login IS NOT NULL"):
        owners[(repo, path)].add((login or "").lower())

    # Reverts (GitHub "Reverts org/repo#N")
    reverted = set()
    for f in glob.glob(os.path.join(ROOT, "data", "raw", "e9", "reverts-*.json")):
        repo = os.path.basename(f)[8:-5]
        for pr in json.load(open(f)):
            for m in re.finditer(r"#(\d+)", (pr.get("body") or "") + " " + (pr.get("title") or "")):
                reverted.add((repo, int(m.group(1))))

    prs = []
    for (repo, num, author, created, merged, adds, dels, ai, threads, reviews, keys) in db.execute(
            "SELECT repo, number, author, created, merged, adds, dels, ai_flag, review_threads, reviews, jira_keys "
            "FROM prs WHERE merged >= '2025-01-01'"):
        shas = [s for (r_, s), n in pr_of.items() if r_ == repo and n == num]
        files = set().union(*(files_of[(repo, s)] for s in shas)) if shas else set()
        lines = (adds or 0) + (dels or 0)
        t = ts(merged)
        teams = [issue_team[k] for k in json.loads(keys or "[]") if k in issue_team]
        team = collections.Counter(teams).most_common(1)[0][0] if teams else None
        hot_dirs = [(r_, p) for r_, p in hot if r_ == repo and any(f.startswith(p + "/") for f in files)]
        outside_owner = None
        if hot_dirs:
            outside_owner = int(all((author or "").lower() not in owners[h] for h in hot_dirs))

        def follow(days):
            if (END - t).days < days:
                return None
            for d, ff, sha in fixes[repo]:
                if pr_of.get((repo, sha)) == num:
                    continue
                if 0 < (d - t).total_seconds() <= days * 86400 and files & ff:
                    return 1
            return 0

        prs.append(dict(repo=repo, num=num, author=(author or "").lower(), ai=ai, month=merged[:7],
                        q=f"{merged[:4]}-Q{(int(merged[5:7]) - 1) // 3 + 1}", lines=lines, b=bucket(lines),
                        hot=int(bool(hot_dirs)), team=team, f30=follow(30), f90=follow(90),
                        tests=int(any(TEST.search(f) for f in files)), threads=threads or 0, reviews=reviews or 0,
                        hours=(t - ts(created)).total_seconds() / 3600, reverted=int((repo, num) in reverted),
                        outside_owner=outside_owner))

    rows = []

    def add(section, label, **kw):
        rows.append(dict(section=section, label=label, **kw))

    # (a) matched / stratified comparisons
    def strat(outcome, keyfn, sub):
        cells = collections.defaultdict(lambda: [0, 0, 0, 0])
        for p in sub:
            if p[outcome] is None:
                continue
            c = cells[keyfn(p)]
            if p["ai"]:
                c[0] += p[outcome]
                c[1] += 1
            else:
                c[2] += p[outcome]
                c[3] += 1
        return list(map(tuple, cells.values()))

    designs = {
        "repo x size x hotspot x quarter": lambda p: (p["repo"], p["b"], p["hot"], p["q"]),
        "team x size x quarter": lambda p: (p["team"] or "?", p["b"], p["q"]),
        "author x size (within-author)": lambda p: (p["author"], p["b"]),
    }
    for outcome, window in (("f90", "<= 2026-07-25"), ("f30", "<= 2026-09-25"), ("reverted", "all"), ("tests", "all")):
        for name, kf in designs.items():
            sub = [p for p in prs if p["q"] >= "2025-Q4"]
            strata = strat(outcome, kf, sub)
            rr, lo, hi, used = mh_rr(strata)
            a = sum(s[0] for s in strata if s[1] and s[3]); n1 = sum(s[1] for s in strata if s[1] and s[3])
            c = sum(s[2] for s in strata if s[1] and s[3]); n0 = sum(s[3] for s in strata if s[1] and s[3])
            add("matched_rr", f"{outcome} | {name}", window=window, strata_used=used, ai_events=a, ai_n=n1,
                nonai_events=c, nonai_n=n0, rr=round(rr, 2) if rr else None, ci_low=round(lo, 2) if lo else None,
                ci_high=round(hi, 2) if hi else None)

    # (b) staggered adoption, repo level: first month with >= 20% AI PRs and >= 5 PRs
    by_rm = collections.defaultdict(lambda: [0, 0])
    for p in prs:
        x = by_rm[(p["repo"], p["month"])]
        x[0] += 1
        x[1] += p["ai"]
    adopt = {}
    for (repo, m) in sorted(by_rm):
        n, a = by_rm[(repo, m)]
        if repo not in adopt and n >= 5 and a / n >= 0.2:
            adopt[repo] = m
    months = sorted({m for (_, m) in commits_month if m >= "2025-01"})

    def rel(m, a):
        y1, m1 = map(int, m.split("-"))
        y0, m0 = map(int, a.split("-"))
        return (y1 - y0) * 12 + (m1 - m0)

    pre = [0, 0]; post = [0, 0]; cpre = [0, 0]; cpost = [0, 0]
    for repo, am in adopt.items():
        for m in months:
            k = rel(m, am)
            if -6 <= k <= -1:
                pre[0] += fix_month[(repo, m)]; pre[1] += commits_month[(repo, m)]
                for r2 in {r_ for r_, _ in commits_month}:
                    if r2 != repo and (r2 not in adopt or adopt[r2] > m):
                        cpre[0] += fix_month[(r2, m)]; cpre[1] += commits_month[(r2, m)]
            elif 0 <= k <= 5:
                post[0] += fix_month[(repo, m)]; post[1] += commits_month[(repo, m)]
                for r2 in {r_ for r_, _ in commits_month}:
                    if r2 != repo and (r2 not in adopt or adopt[r2] > m):
                        cpost[0] += fix_month[(r2, m)]; cpost[1] += commits_month[(r2, m)]
    tr = poisson_ratio(post[0], post[1], pre[0], pre[1])
    cr = poisson_ratio(cpost[0], cpost[1], cpre[0], cpre[1])
    add("event_study", "repo adoption: CFB-fix commits per commit, 6 mo after vs before",
        adopted_repos=len(adopt), treated_pre=f"{pre[0]}/{pre[1]}", treated_post=f"{post[0]}/{post[1]}",
        rr=round(tr[0], 2) if tr[0] else None, ci_low=round(tr[1], 2) if tr[1] else None, ci_high=round(tr[2], 2) if tr[2] else None)
    add("event_study", "not-yet-adopted repos, same calendar months (control)",
        treated_pre=f"{cpre[0]}/{cpre[1]}", treated_post=f"{cpost[0]}/{cpost[1]}",
        rr=round(cr[0], 2) if cr[0] else None, ci_low=round(cr[1], 2) if cr[1] else None, ci_high=round(cr[2], 2) if cr[2] else None)
    if tr[0] and cr[0]:
        add("event_study", "ratio of ratios (treated / control)", rr=round(tr[0] / cr[0], 2))
    for repo, am in sorted(adopt.items()):
        add("adoption_month", repo, window=am)

    # (b2) team level: adoption month from PRs mapped to team (>= 3 PRs, >= 20% AI); outcome = valid non-MI CFBs created
    tm = collections.defaultdict(lambda: [0, 0])
    for p in prs:
        if p["team"]:
            x = tm[(p["team"], p["month"])]; x[0] += 1; x[1] += p["ai"]
    tadopt = {}
    for (team, m) in sorted(tm):
        n, a = tm[(team, m)]
        if team not in tadopt and n >= 3 and a / n >= 0.2:
            tadopt[team] = m
    cfb_tm = collections.Counter((t, c[:7]) for c, t in cfb.values() if t)
    tpre = tpost = 0
    for team, am in tadopt.items():
        for m in months:
            k = rel(m, am)
            if -6 <= k <= -1:
                tpre += cfb_tm[(team, m)]
            elif 0 <= k <= 5:
                tpost += cfb_tm[(team, m)]
    add("event_study", "team adoption: valid non-MI CFBs, 6 mo after vs before (no workload denominator)",
        adopted_repos=len(tadopt), treated_pre=str(tpre), treated_post=str(tpost),
        rr=round(tpost / tpre, 2) if tpre else None)
    allteams = collections.Counter(c[:7] for c, t in cfb.values())
    add("event_study", "all valid non-MI CFBs, same 12-month span (trend reference)",
        treated_pre=str(sum(v for m, v in allteams.items() if "2025-10" <= m <= "2026-03")),
        treated_post=str(sum(v for m, v in allteams.items() if "2026-04" <= m <= "2026-09")))

    # (2) mechanisms by quarter
    for q in sorted({p["q"] for p in prs if p["q"] >= "2025-Q4"}):
        for grp, ai in (("ai", 1), ("non-ai", 0)):
            g = [p for p in prs if p["q"] == q and p["ai"] == ai]
            if not g:
                continue
            lines = sum(p["lines"] for p in g) or 1
            oo = [p["outside_owner"] for p in g if p["outside_owner"] is not None]
            add("mechanism", f"{q} {grp}", n=len(g), median_lines=st.median(p["lines"] for p in g),
                tests_pct=round(100 * sum(p["tests"] for p in g) / len(g), 1),
                threads_per_100_lines=round(100 * sum(p["threads"] for p in g) / lines, 2),
                median_hours_to_merge=round(st.median(p["hours"] for p in g), 1),
                reverted_pct=round(100 * sum(p["reverted"] for p in g) / len(g), 2),
                hotspot_pct=round(100 * sum(p["hot"] for p in g) / len(g), 1),
                outside_owner_pct=round(100 * sum(oo) / len(oo), 1) if oo else None)
        h = [p for p in prs if p["q"] == q and p["hot"]]
        if h:
            add("ai_share_hotspot", q, n=len(h), ai_pct=round(100 * sum(p["ai"] for p in h) / len(h), 1))

    # Store
    db.execute("DROP TABLE IF EXISTS ai_matched")
    db.execute("CREATE TABLE ai_matched (repo, num, author, team, ai, month, lines, bucket, hotspot, f30, f90, tests, "
               "threads, reviews, hours, reverted, outside_owner)")
    db.executemany("INSERT INTO ai_matched VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   [(p["repo"], p["num"], p["author"], p["team"], p["ai"], p["month"], p["lines"], p["b"], p["hot"],
                     p["f30"], p["f90"], p["tests"], p["threads"], p["reviews"], round(p["hours"], 1), p["reverted"],
                     p["outside_owner"]) for p in prs])
    db.execute("DROP TABLE IF EXISTS ai_event_study")
    db.execute("CREATE TABLE ai_event_study (unit, unit_type, adoption_month)")
    db.executemany("INSERT INTO ai_event_study VALUES (?,?,?)",
                   [(r_, "repo", m) for r_, m in adopt.items()] + [(t, "team", m) for t, m in tadopt.items()])
    db.commit()

    cols = ["section", "label", "window", "strata_used", "ai_events", "ai_n", "nonai_events", "nonai_n", "rr", "ci_low",
            "ci_high", "adopted_repos", "treated_pre", "treated_post", "n", "median_lines", "tests_pct",
            "threads_per_100_lines", "median_hours_to_merge", "reverted_pct", "hotspot_pct", "outside_owner_pct", "ai_pct"]
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r_ in rows:
            w.writerow({k: r_.get(k) for k in cols})
    print("PRs", len(prs), "AI", sum(p["ai"] for p in prs), "team mapped", sum(1 for p in prs if p["team"]),
          "valid non-MI CFB keys", len(cfb), "fix commits", sum(len(v) for v in fixes.values()),
          "reverted PRs found", len(reverted))
    for r_ in rows:
        print({k: v for k, v in r_.items() if v is not None})


if __name__ == "__main__":
    main()
