"""R3 hotspots + R14 ownership for the pilot. Reads git_commits / git_file_changes / issues / causal_links / flow_tags.

Writes tables r3_commit_flags, r3_dir_hotspots, r3_file_hotspots, r14_ownership, r3_test_names and
CSVs data/aggregates/r3-hotspots.csv, r3-file-hotspots.csv, r14-ownership.csv.
"""
import csv, json, os, re, sqlite3, subprocess
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")
GIT = os.path.join(ROOT, "data", "raw", "git")
AGG = os.path.join(ROOT, "data", "aggregates")
W12, W24, LEFT = "2025-10-22", "2024-10-22", "2026-04-22"
BULK = 500
MONO = "inContact"
TEST_REPOS = {"routing-ng-integration-tests", "acd-playwright-e2e"}
TEST = re.compile(r"(^|/)(tests?|spec|specs|__tests__|testing|e2e|it)(/|$)|test|spec\.", re.I)
BOUNDARY = re.compile(r"(Event|Kinesis|Kafka|Publish|ContactState|Entity|Disposition|Stream|Notif|Messag|Queue|Consumer|Producer)", re.I)
CONC = re.compile(r"(Concurren|RaceCondition|Race[A-Z_]|_race|Parallel|LoadTest|Load_|Stress|Chaos|ThreadSafe|Threading|Contention|Deadlock|OutOfOrder|Ordering)")


def dir_of(repo, path):
    """Directory unit: VCSvc providers at depth 6, rest of monolith depth 5; Java services at package depth 8, else 3."""
    parts = path.split("/")
    if repo == MONO:
        depth = 6 if path.startswith("Code/C#/Services/VCSvc/") else 5
    else:
        depth = 8 if re.match(r"src/(main|test|it)/java/", path) else 3
    d = "/".join(parts[:min(depth, len(parts) - 1)]) or "(root)"
    return f"{repo}:{d}"


def prank(values):
    s = sorted(values)
    n = len(s)
    return lambda v: (sum(1 for x in s if x <= v) / n) if n else 0


def main():
    db = sqlite3.connect(DB, timeout=60)
    db.execute("ATTACH DATABASE ? AS gh", (os.path.join(os.path.dirname(DB), 'git_history.sqlite'),))  # git_file_changes lives here (D-019); gunzip git_history.sqlite.gz first
    cfb = {k for (k,) in db.execute("SELECT key FROM issues WHERE is_cfb=1")}
    pilot = {k for (k,) in db.execute("SELECT key FROM flow_tags WHERE in_flow_scope=1")}
    causing = {k for (k,) in db.execute("SELECT DISTINCT causing_key FROM causal_links")}
    files = defaultdict(list)
    for repo, sha, path in db.execute("SELECT repo, sha, path FROM gh.git_file_changes"):
        files[(repo, sha)].append(path)

    flags = {}
    for repo, sha, date, author, merge, keys, bot in db.execute("SELECT * FROM git_commits"):
        ks = set(json.loads(keys))
        n = len(files[(repo, sha)])
        flags[(repo, sha)] = dict(repo=repo, sha=sha, date=date[:10], author=author, merge=merge, bot=bot,
                                  has_key=1 if ks else 0, cfb_fix=1 if ks & cfb else 0, pilot_fix=1 if ks & pilot else 0,
                                  causing=1 if ks & causing else 0, bulk=1 if n > BULK else 0, nfiles=n,
                                  touches_test=1 if any(TEST.search(p) for p in files[(repo, sha)]) else 0)
    db.execute("DROP TABLE IF EXISTS r3_commit_flags")
    cols = list(next(iter(flags.values())))
    db.execute(f"CREATE TABLE r3_commit_flags ({', '.join(cols)})")
    db.executemany(f"INSERT INTO r3_commit_flags VALUES ({','.join('?'*len(cols))})", [tuple(f.values()) for f in flags.values()])

    last_seen = {}
    for f in flags.values():
        last_seen[f["author"]] = max(last_seen.get(f["author"], ""), f["date"])

    def usable(f):
        return not f["merge"] and not f["bot"] and not f["bulk"] and f["date"] >= W24

    def agg(keyfn):
        A = defaultdict(lambda: dict(c12=0, c24=0, a12=set(), fix=0, cause=0, pfix=0, test=0, authors24=Counter(), authors12=Counter()))
        for (repo, sha), f in flags.items():
            if not usable(f):
                continue
            for k in {keyfn(repo, p) for p in files[(repo, sha)]}:
                a = A[k]
                a["c24"] += 1
                a["fix"] += f["cfb_fix"]
                a["cause"] += f["causing"]
                a["pfix"] += f["pilot_fix"]
                a["test"] += f["touches_test"]
                a["authors24"][f["author"]] += 1
                if f["date"] >= W12:
                    a["c12"] += 1
                    a["a12"].add(f["author"])
                    a["authors12"][f["author"]] += 1
        return A

    def score(A):
        live = {k: a for k, a in A.items() if (a["fix"] + a["cause"]) > 0 and a["c12"] > 0}
        rc = prank([a["c12"] for a in live.values()])
        rd = prank([a["fix"] + a["cause"] for a in live.values()])
        return sorted(((round(rc(a["c12"]) * rd(a["fix"] + a["cause"]), 3), k, a) for k, a in live.items()), key=lambda t: (-t[0], -(t[2]["fix"] + t[2]["cause"])))

    def rows(scored, level):
        out = []
        for s, k, a in scored:
            repo, _, path = k.partition(":")
            m = BOUNDARY.search(path)
            out.append(dict(level=level, repo=repo, path=path, area="monolith" if repo == MONO else ("test" if repo in TEST_REPOS else "service"),
                            score=s, commits_12m=a["c12"], commits_24m=a["c24"], authors_12m=len(a["a12"]),
                            cfb_fix_24m=a["fix"], causing_24m=a["cause"], pilot_fix_24m=a["pfix"],
                            test_touch_pct=round(100 * a["test"] / a["c24"], 1) if a["c24"] else 0,
                            is_test_path=1 if TEST.search(path) else 0, boundary_token=m.group(1) if m else ""))
        return out

    D = agg(dir_of)
    F = agg(lambda r, p: f"{r}:{p}")
    drows, frows = rows(score(D), "dir"), rows(score(F), "file")

    own = []
    for r in drows:
        a = D[f"{r['repo']}:{r['path']}"]
        c12 = sum(a["authors12"].values())
        top12 = a["authors12"].most_common()
        cum, bus = 0, 0
        for _, n in top12:
            cum += n
            bus += 1
            if cum >= c12 / 2:
                break
        c24 = sum(a["authors24"].values())
        gone = [(au, n) for au, n in a["authors24"].most_common() if last_seen.get(au, "") < LEFT and n / c24 > 0.30]
        own.append(dict(repo=r["repo"], path=r["path"], score=r["score"], commits_12m=c12,
                        authors_ge10pct=sum(1 for _, n in top12 if c12 and n / c12 >= 0.10),
                        top_author=top12[0][0] if top12 else "", top_author_share_pct=round(100 * top12[0][1] / c12, 1) if c12 else 0,
                        bus_factor_50=bus if c12 else 0,
                        departed_owner_gt30pct="; ".join(f"{au} ({round(100*n/c24)}%)" for au, n in gone)))

    tests = []
    for repo in sorted(os.listdir(GIT)):
        p = os.path.join(GIT, repo)
        if not os.path.isdir(os.path.join(p, ".git")):
            continue
        names = subprocess.run(["git", "-C", p, "ls-tree", "-r", "--name-only", "HEAD"], capture_output=True, text=True, errors="replace").stdout.splitlines()
        tpaths = [n for n in names if TEST.search(n)]
        conc = [n for n in tpaths if CONC.search(n.rsplit("/", 1)[-1])]
        tests.append(dict(repo=repo, files=len(names), test_files=len(tpaths), concurrency_named_test_files=len(conc),
                          examples="; ".join(c.rsplit("/", 1)[-1] for c in conc[:5])))

    for name, data in (("r3_dir_hotspots", drows), ("r3_file_hotspots", frows), ("r14_ownership", own), ("r3_test_names", tests)):
        db.execute(f"DROP TABLE IF EXISTS {name}")
        c = list(data[0])
        db.execute(f"CREATE TABLE {name} ({', '.join(c)})")
        db.executemany(f"INSERT INTO {name} VALUES ({','.join('?'*len(c))})", [tuple(d.values()) for d in data])
    db.commit()

    for fn, data in (("r3-hotspots.csv", drows), ("r3-file-hotspots.csv", frows[:300]), ("r14-ownership.csv", own), ("r3-test-names.csv", tests)):
        with open(os.path.join(AGG, fn), "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(data[0]))
            w.writeheader()
            w.writerows(data)
    print(len(drows), "dirs;", len(frows), "files;", len(own), "ownership;", len(tests), "repos")


if __name__ == "__main__":
    main()
