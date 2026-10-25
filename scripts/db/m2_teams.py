"""M2-TEAMS: team map (sources of truth) and team profiles (outcomes + practices) for mission v2.

Run from repo root: python3 -I scripts/db/m2_teams.py /tmp/gh_teams.tsv
Writes tables team_map, m2_team_profiles and data/aggregates/m2-team-profiles.csv.
"""
import csv
import json
import os
import re
import sqlite3
import statistics as st
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")
OUT = os.path.join(ROOT, "data", "aggregates", "m2-team-profiles.csv")
INVALID = {"cannot reproduce", "not a bug", "won't do", "duplicate", "won't fix", "works as designed", "invalid"}
CAP = 40


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def window(created):
    if created[:10] < "2025-01-01":
        return None
    md = created[5:10]
    if md > "10-22":
        return None
    return created[:4]


def gh_teams(path):
    teams = {}
    if path and os.path.exists(path):
        for line in open(path):
            p = line.rstrip("\n").split("\t")
            if p and p[0]:
                teams[norm(p[1] if len(p) > 1 else p[0])] = p[0]
                teams.setdefault(norm(p[0]), p[0])
    return teams


def match_gh(team, gh):
    n = norm(team)
    if not n:
        return None
    if n in gh:
        return gh[n]
    for k, slug in gh.items():
        if len(n) >= 6 and (n in k or k in n) and len(k) >= 6:
            return slug
    return None


def main():
    gh = gh_teams(sys.argv[1] if len(sys.argv) > 1 else "")
    db = sqlite3.connect(DB)
    issues = db.execute(
        "SELECT key, team, rnd_vp, created, resolved, resolution, priority, incidents, rca_state, ai_label, ai_implemented "
        "FROM issues WHERE is_cfb = 1 AND created >= '2025-01-01' AND team IS NOT NULL").fetchall()
    by_team = {}
    for r in issues:
        by_team.setdefault(r[1], []).append(r)

    def valid(r):
        return not (r[5] and r[5].lower() in INVALID)

    ranked = sorted(by_team, key=lambda t: -sum(valid(r) for r in by_team[t]))
    ranked = [t for t in ranked if sum(valid(r) for r in by_team[t]) >= 10][:CAP]

    key_team = {k: t for k, t, *_ in issues}
    team_prs = {}
    for repo, number, adds, dels, ai_flag, reviews, tests, keys in db.execute(
            "SELECT repo, number, adds, dels, ai_flag, reviews, touches_tests, jira_keys FROM prs"):
        for k in json.loads(keys or "[]"):
            t = key_team.get(k)
            if t:
                team_prs.setdefault(t, {})[(repo, number)] = (repo, (adds or 0) + (dels or 0), ai_flag, reviews, tests)
    repo_ci = {}
    for repo, n, ok in db.execute(
            "SELECT repo, COUNT(*), SUM(conclusion = 'success') FROM ci_runs "
            "WHERE conclusion IN ('success', 'failure') GROUP BY repo"):
        repo_ci[repo] = (ok or 0) / n if n else None

    db.execute("DROP TABLE IF EXISTS team_map")
    db.execute("CREATE TABLE team_map (team_jira TEXT PRIMARY KEY, rnd_vp TEXT, gh_team TEXT, sn_group TEXT, "
               "repos TEXT, source TEXT, confidence TEXT)")
    rows = []
    for t in ranked:
        rs = by_team[t]
        vp = st.mode([r[2] for r in rs if r[2]]) if any(r[2] for r in rs) else None
        prs = list(team_prs.get(t, {}).values())
        repos = sorted({p[0] for p in prs})
        g = match_gh(t, gh)
        db.execute("INSERT INTO team_map VALUES (?,?,?,?,?,?,?)", (
            t, vp, g, None, json.dumps(repos),
            "Jira Team Name (cf_10098); GitHub team by name match; repos via PR Jira keys",
            "medium" if g and repos else ("low" if g or repos else "jira-only")))
        v = [r for r in rs if valid(r)]
        y25 = sum(1 for r in v if window(r[3]) == "2025")
        y26 = sum(1 for r in v if window(r[3]) == "2026")
        inc = [r[7] for r in rs if r[7] is not None]
        fixed = [r for r in rs if r[5] in ("Fixed", "Fixed - Config")]
        rca_known = [r for r in fixed if r[8]]
        days = []
        for r in fixed:
            if r[4]:
                days.append((int(r[4][:4]) * 365 + int(r[4][5:7]) * 30 + int(r[4][8:10]))
                            - (int(r[3][:4]) * 365 + int(r[3][5:7]) * 30 + int(r[3][8:10])))
        ci_vals = [repo_ci[x] for x in repos if repo_ci.get(x) is not None]
        rows.append({
            "team": t, "rnd_vp": vp, "gh_team": g or "",
            "cfb_all": len(rs), "cfb_valid": len(v),
            "valid_2025_janoct": y25, "valid_2026_janoct": y26,
            "valid_change_pct": round(100 * (y26 - y25) / y25, 0) if y25 else "",
            "p12_share_valid_pct": round(100 * sum(r[6] in ("P1", "P2") for r in v) / len(v), 1),
            "incidents_per_cfb": round(sum(inc) / len(inc), 2) if inc else "",
            "invalid_pct": round(100 * (len(rs) - len(v)) / len(rs), 1),
            "rca_filled_pct": round(100 * sum(r[8] == "filled" for r in rca_known) / len(rca_known), 1) if rca_known else "",
            "median_days_to_fix": st.median(days) if days else "",
            "ai_fix_share_pct": round(100 * sum((r[9] or 0) == 1 or r[10] == "Yes" for r in fixed) / len(fixed), 1) if fixed else "",
            "prs_linked": len(prs),
            "pr_median_lines": st.median([p[1] for p in prs]) if prs else "",
            "pr_ai_share_pct": round(100 * sum(1 for p in prs if p[2]) / len(prs), 1) if prs else "",
            "pr_reviews_median": st.median([p[3] or 0 for p in prs]) if prs else "",
            "pr_test_touch_pct": round(100 * sum(1 for p in prs if p[4]) / len(prs), 1) if prs else "",
            "ci_pass_pct": round(100 * st.mean(ci_vals), 1) if ci_vals else "",
            "repos": ";".join(repos),
        })
    db.commit()
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"teams profiled: {len(rows)}; with gh match: {sum(1 for r in rows if r['gh_team'])}; "
          f"with PR data: {sum(1 for r in rows if r['prs_linked'])}")


if __name__ == "__main__":
    main()
