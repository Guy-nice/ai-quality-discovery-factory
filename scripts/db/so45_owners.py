"""SO-4 owner candidates and SO-5 PR size risk for the top-10 pilot hotspot directories.

Inputs: quality.sqlite, git_history.sqlite (ATTACH gh), data/raw/so45/{authors,logins,reviews}.tsv (gh API pulls).
Outputs: tables so45_owners, so45_size_risk; CSVs in data/aggregates/.
"""
import collections as C, csv, datetime as dt, math, os, sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")
RAW = os.path.join(ROOT, "data", "raw", "so45")
AGG = os.path.join(ROOT, "data", "aggregates")
SINCE_12M, SINCE_6M, END = "2025-10-22", "2026-04-22", "2026-10-22"

TOP = [
    ("inContact", "Code/C#/Services/VCSvc/Providers/ACD"),
    ("inContact", "Code/C#/Library/AgentHelper"),
    ("routing-ng-advanced-findmatch", "src/main/java/com/nice/routing/afm/service"),
    ("inContact", "Code/C#/Library/inContact.InterVCCommWrapper/SynchronizerMessages"),
    ("inContact", "Code/C#/Services/VCSvc/Providers/Data"),
    ("inContact", "Database/InDB_DACPAC/inCode/dbo/StoredProcedures"),
    ("inContact", "Code/C#/Library/AgentHelper/MCH"),
    ("inContact", "Code/C#/Library/inContact.InterVCCommWrapper/Messages"),
    ("inContact", "Code/C#/Services/VCSvc/Providers/Agent"),
    ("routing-ng-agent-capacity-service", "src/main/java/com/nice/routing/agentcapacityservice/client"),
]
# GitHub commit API returned no login for these names; resolved from another commit by the same author.
LOGIN_OVERRIDES = {"A.J. Bobo": "ajbobo-nice"}
# Confluence shows the account as deactivated while commits continue: keep, but rank last and flag.
VERIFY_ACTIVE = {"onkargadekar"}
BUCKETS = [(0, 50), (51, 150), (151, 400), (401, 1000), (1001, 10**9)]


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0.0, c - h), min(1.0, c + h))


def load_logins():
    name_of = {}
    for line in open(os.path.join(RAW, "authors.tsv")):
        repo, sha, name = line.rstrip("\n").split("\t")
        name_of[(repo, sha)] = name
    login_of = {}
    for line in open(os.path.join(RAW, "logins.tsv")):
        repo, sha, login = (line.rstrip("\n").split("\t") + [""])[:3]
        if login:
            login_of[name_of[(repo, sha)]] = login
    login_of.update(LOGIN_OVERRIDES)
    return login_of


def load_reviews():
    rev = C.defaultdict(list)
    for line in open(os.path.join(RAW, "reviews.tsv")):
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 5:
            continue
        repo, num, login, state, utype = parts
        if utype == "User" and login and state in ("APPROVED", "CHANGES_REQUESTED", "COMMENTED"):
            rev[(repo, int(num))].append(login)
    return rev


def owners(db, login_of, reviews):
    out = []
    for repo, path in TOP:
        like = path + "/%"
        commits = db.execute(
            """SELECT c.author, COUNT(DISTINCT c.sha), MAX(c.date) FROM git_commits c
               JOIN gh.git_file_changes f ON f.repo=c.repo AND f.sha=c.sha
               WHERE c.repo=? AND f.path LIKE ? AND c.is_bot=0 AND c.is_merge=0 AND c.date>=? GROUP BY 1""",
            (repo, like, SINCE_12M)).fetchall()
        prs_recent = [n for (n,) in db.execute(
            """SELECT DISTINCT pc.pr_number FROM pr_commits pc JOIN gh.git_file_changes f ON f.repo=pc.repo AND f.sha=pc.sha
               JOIN git_commits c ON c.repo=pc.repo AND c.sha=pc.sha
               WHERE pc.repo=? AND f.path LIKE ? AND c.date>=? AND pc.pr_number IS NOT NULL""",
            (repo, like, SINCE_6M))]
        rcount = C.Counter(l for n in prs_recent for l in set(reviews.get((repo, n), [])))
        people = {}
        for name, n, last in commits:
            lg = login_of.get(name) or name
            p = people.setdefault(lg, {"name": name, "commits": 0, "last": "", "reviews": 0})
            p["commits"] += n
            p["last"] = max(p["last"], last[:10])
        for lg, n in rcount.items():
            people.setdefault(lg, {"name": lg, "commits": 0, "last": "", "reviews": 0})["reviews"] = n
        for lg, p in people.items():
            committer = p["commits"] >= 5 and p["last"] >= SINCE_6M
            reviewer = p["reviews"] >= 10
            linked = " " not in lg  # CODEOWNERS needs a GitHub account; unlinked commit emails resolve to a display name
            p["qualifies"] = (committer or reviewer) and linked
            p["basis"] = "+".join(b for b, ok in (("commits", committer), ("reviews", reviewer)) if ok)
            p["rank_score"] = (p["commits"] + p["reviews"]) - (1000 if lg in VERIFY_ACTIVE else 0)
            if lg in VERIFY_ACTIVE:
                p["basis"] = (p["basis"] + "; verify active (Confluence deactivated)").lstrip("; ")
        ranked = sorted(people.items(), key=lambda kv: -kv[1]["rank_score"])
        chosen = [kv for kv in ranked if kv[1]["qualifies"]][:4]
        grow = [kv for kv in ranked if not kv[1]["qualifies"] and kv[1]["last"] >= SINCE_6M and kv[1]["commits"] >= 2][:3] if len(chosen) < 3 else []
        for role, group in (("owner", chosen), ("to_grow", grow)):
            for lg, p in group:
                out.append({"repo": repo, "path": path, "role": role, "login": lg, "name": p["name"],
                            "commits_12m": p["commits"], "last_commit": p["last"], "reviews_6m": p["reviews"],
                            "basis": p["basis"] or "nearest active", "owners_found": len(chosen)})
        if not chosen and not grow:
            out.append({"repo": repo, "path": path, "role": "none", "login": "", "name": "", "commits_12m": 0,
                        "last_commit": "", "reviews_6m": 0, "basis": "", "owners_found": 0})
    return out


def size_risk(db):
    hot = {(r, p) for r, p in TOP}
    fix_files = C.defaultdict(list)
    for repo, sha, date, path in db.execute(
            """SELECT f.repo, f.sha, x.date, f.path FROM r3_commit_flags x JOIN gh.git_file_changes f
               ON f.repo=x.repo AND f.sha=x.sha WHERE x.cfb_fix=1"""):
        fix_files[(repo, path)].append((date[:10], sha))
    pr_files = C.defaultdict(set)
    pr_shas = C.defaultdict(set)
    for repo, num, sha, path in db.execute(
            """SELECT pc.repo, pc.pr_number, pc.sha, f.path FROM pr_commits pc JOIN gh.git_file_changes f
               ON f.repo=pc.repo AND f.sha=pc.sha WHERE pc.pr_number IS NOT NULL"""):
        pr_files[(repo, num)].add(path)
        pr_shas[(repo, num)].add(sha)
    cut = (dt.date.fromisoformat(END) - dt.timedelta(days=30)).isoformat()
    stats = C.defaultdict(lambda: [0, 0, 0, 0])
    for repo, num, merged, adds, dels, ai, threads in db.execute(
            "SELECT repo, number, merged, adds, dels, ai_flag, review_threads FROM prs WHERE merged >= '2025-01-01'"):
        if not merged or merged[:10] > cut:
            continue
        lines = (adds or 0) + (dels or 0)
        files = pr_files.get((repo, num), set())
        in_hot = any(any(fp.startswith(p + "/") for r, p in hot if r == repo) for fp in files)
        m0 = dt.date.fromisoformat(merged[:10])
        m30 = (m0 + dt.timedelta(days=30)).isoformat()
        own = pr_shas.get((repo, num), set())
        follow = any(m0.isoformat() < d <= m30 and s not in own for fp in files for d, s in fix_files.get((repo, fp), []))
        b = next(i for i, (lo, hi) in enumerate(BUCKETS) if lo <= lines <= hi)
        for scope in ("all", "hotspot" if in_hot else "non_hotspot", "ai" if ai else "non_ai"):
            s = stats[(scope, b)]
            s[0] += 1
            s[1] += int(follow)
            s[2] += lines
            s[3] += threads or 0
    rows = []
    for (scope, b), (n, k, lines, threads) in sorted(stats.items()):
        p, lo, hi = wilson(k, n)
        lo_b, hi_b = BUCKETS[b]
        rows.append({"scope": scope, "bucket": f"{lo_b}-{hi_b}" if hi_b < 10**9 else f">{lo_b - 1}", "prs": n,
                     "followup_fix": k, "rate_pct": round(100 * p, 1), "ci_low_pct": round(100 * lo, 1),
                     "ci_high_pct": round(100 * hi, 1),
                     "review_threads_per_100_lines": round(100 * threads / lines, 3) if lines else 0})
    return rows


def write(rows, name, db, table):
    path = os.path.join(AGG, name)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    cols = list(rows[0])
    db.execute(f"DROP TABLE IF EXISTS {table}")
    db.execute(f"CREATE TABLE {table} ({', '.join(cols)})")
    db.executemany(f"INSERT INTO {table} VALUES ({','.join('?' * len(cols))})", [tuple(r[c] for c in cols) for r in rows])


if __name__ == "__main__":
    db = sqlite3.connect(DB, timeout=60)
    db.execute("ATTACH DATABASE ? AS gh", (os.path.join(os.path.dirname(DB), "git_history.sqlite"),))
    o = owners(db, load_logins(), load_reviews())
    s = size_risk(db)
    write(o, "so45-owners.csv", db, "so45_owners")
    write(s, "so45-size-risk.csv", db, "so45_size_risk")
    db.commit()
    for r in o:
        print(r["path"].split("/")[-1], r["role"], r["login"], r["commits_12m"], r["reviews_6m"], r["basis"], r["owners_found"])
    for r in s:
        print(r)
