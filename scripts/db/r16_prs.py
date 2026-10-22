"""R16: map pilot commits (2025-01..) to merged PRs via GitHub GraphQL; store PR facts and AI flags in quality.sqlite.

PR bodies and commit messages are read only to set flags and extract Jira keys; they are not stored.
Usage: python3 -I scripts/db/r16_prs.py
"""
import json, os, re, sqlite3, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")
CACHE = os.path.join(ROOT, "data", "raw", "r16")
SINCE = "2025-01-01"
BATCH = 40

KEY = re.compile(r"\b[A-Z][A-Z0-9]{1,9}-\d{1,6}\b")
AI_TEXT = re.compile(r"(generated with \[?claude|co-authored-by:.*(claude|copilot|cursor|anthropic|openai)|noreply@anthropic\.com|copilot-swe-agent|\bclaude code\b)", re.I)
AI_BRANCH = re.compile(r"(^|/)(claude|copilot|cursor|ai)[/_-]", re.I)
AI_LABEL = re.compile(r"^(AGENTIC_AI_CODE|AGENT_AI_CODE|AI[-_]Assisted|UseAIAgent|copilot|claude)", re.I)
PCT = re.compile(r"AGENTIC_AI_CODE_(\d{1,3})")

PR_FIELDS = """number title createdAt mergedAt additions deletions changedFiles headRefName bodyText
 author { login }
 labels(first: 30) { nodes { name } }
 reviews(first: 60) { totalCount nodes { author { login } state } }
 reviewThreads(first: 1) { totalCount }
 commits(last: 40) { nodes { commit { message } } }"""


def gql(query):
    for attempt in range(4):
        p = subprocess.run(["gh", "api", "graphql", "-f", f"query={query}"], capture_output=True, text=True)
        if p.returncode == 0:
            return json.loads(p.stdout)
        if "rate limit" in p.stderr.lower() or "502" in p.stderr or "timeout" in p.stderr.lower():
            time.sleep(20 * (attempt + 1))
            continue
        try:
            return json.loads(p.stdout)
        except Exception:
            sys.stderr.write(p.stderr[:500])
            time.sleep(5)
    return {}


def strip(pr):
    """Reduce a PR node to flags + facts; drop free text."""
    body = pr.get("bodyText") or ""
    msgs = [n["commit"]["message"] for n in (pr.get("commits") or {}).get("nodes", [])]
    labels = [n["name"] for n in (pr.get("labels") or {}).get("nodes", [])]
    author = (pr.get("author") or {}).get("login") or ""
    revs = (pr.get("reviews") or {}).get("nodes", [])
    reviewers = sorted({(r.get("author") or {}).get("login") for r in revs if (r.get("author") or {}).get("login") and (r.get("author") or {}).get("login") != author})
    pct = [int(m.group(1)) for l in labels for m in [PCT.search(l)] if m]
    flags = {
        "label": any(AI_LABEL.search(l) for l in labels),
        "text": bool(AI_TEXT.search(body) or any(AI_TEXT.search(m) for m in msgs)),
        "branch": bool(AI_BRANCH.search(pr.get("headRefName") or "")),
        "bot": author.endswith("[bot]") or "copilot" in author.lower(),
    }
    keys = sorted(set(KEY.findall(pr.get("title") or "") + KEY.findall(pr.get("headRefName") or "") + [k for m in msgs for k in KEY.findall(m.split("\n")[0])]))
    return {
        "number": pr["number"], "author": author, "created": pr["createdAt"], "merged": pr["mergedAt"],
        "adds": pr.get("additions"), "dels": pr.get("deletions"), "files": pr.get("changedFiles"),
        "ai_flag": int(any(flags.values())), "ai_sources": ",".join(k for k, v in flags.items() if v),
        "ai_pct": max(pct) if pct else None,
        "reviews": (pr.get("reviews") or {}).get("totalCount"), "review_threads": (pr.get("reviewThreads") or {}).get("totalCount"),
        "reviewers": len(reviewers), "jira_keys": json.dumps(keys),
    }


def main():
    os.makedirs(CACHE, exist_ok=True)
    db = sqlite3.connect(DB, timeout=60)
    db.executescript("""
    CREATE TABLE IF NOT EXISTS prs (repo TEXT, number INTEGER, author TEXT, created TEXT, merged TEXT, adds INTEGER, dels INTEGER,
      files INTEGER, ai_flag INTEGER, ai_sources TEXT, ai_pct INTEGER, reviews INTEGER, review_threads INTEGER, reviewers INTEGER,
      touches_tests INTEGER, touches_hotspot INTEGER, jira_keys TEXT, PRIMARY KEY (repo, number));
    CREATE TABLE IF NOT EXISTS pr_commits (repo TEXT, sha TEXT PRIMARY KEY, pr_number INTEGER);
    """)
    done = {r[0] for r in db.execute("SELECT sha FROM pr_commits")}
    rows = [r for r in db.execute("SELECT repo, sha FROM git_commits WHERE date >= ? AND is_merge = 0 ORDER BY repo, date", (SINCE,)) if r[1] not in done]
    by_repo = {}
    for repo, sha in rows:
        by_repo.setdefault(repo, []).append(sha)
    for repo, shas in by_repo.items():
        for i in range(0, len(shas), BATCH):
            chunk = shas[i:i + BATCH]
            parts = " ".join(f'c{j}: object(oid: "{s}") {{ ... on Commit {{ associatedPullRequests(first: 1) {{ nodes {{ {PR_FIELDS} }} }} }} }}' for j, s in enumerate(chunk))
            res = gql(f'query {{ repository(owner: "inContact", name: "{repo}") {{ {parts} }} }}')
            repo_node = ((res or {}).get("data") or {}).get("repository") or {}
            stripped = {}
            for j, s in enumerate(chunk):
                node = repo_node.get(f"c{j}") or {}
                prs = ((node.get("associatedPullRequests") or {}).get("nodes")) or []
                pr = prs[0] if prs else None
                if pr and pr.get("mergedAt"):
                    sp = strip(pr)
                    stripped[s] = sp
                    db.execute("""INSERT OR REPLACE INTO prs(repo, number, author, created, merged, adds, dels, files, ai_flag, ai_sources, ai_pct,
                      reviews, review_threads, reviewers, jira_keys) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                               (repo, sp["number"], sp["author"], sp["created"], sp["merged"], sp["adds"], sp["dels"], sp["files"], sp["ai_flag"],
                                sp["ai_sources"], sp["ai_pct"], sp["reviews"], sp["review_threads"], sp["reviewers"], sp["jira_keys"]))
                db.execute("INSERT OR REPLACE INTO pr_commits VALUES (?,?,?)", (repo, s, pr["number"] if pr and pr.get("mergedAt") else None))
            json.dump(stripped, open(os.path.join(CACHE, f"{repo}-{i}.json"), "w"))
            db.commit()
            print(repo, i + len(chunk), "/", len(shas), flush=True)
    db.execute("INSERT INTO query_log(run_at,purpose,source,jql,dump_file,issues_loaded) VALUES (datetime('now'),'R16','github-graphql',?,?,?)",
               ("commit -> associatedPullRequests, since " + SINCE, "data/raw/r16/*.json", db.execute("SELECT COUNT(*) FROM prs").fetchone()[0]))
    db.commit()


if __name__ == "__main__":
    main()
