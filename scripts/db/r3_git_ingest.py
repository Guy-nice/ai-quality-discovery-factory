"""Ingest git history of pilot repos into quality.sqlite (R3/R14).

Stores commit metadata, Jira keys found in the message (not the message text) and changed paths.
Usage: python3 -I scripts/db/r3_git_ingest.py [repo ...]   (clones in data/raw/git/<repo>)
"""
import json, os, re, sqlite3, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")
GIT = os.path.join(ROOT, "data", "raw", "git")
SINCE = "2024-10-22"
KEY = re.compile(r"\b([A-Z][A-Z0-9]{1,9}-\d{1,7})\b")
BOT = re.compile(r"(\[bot\]|\bbot\b|jenkins|dependabot|renovate|github-actions|svc[-_]|service account|automation)", re.I)
NOT_JIRA = {"UTF-8", "ISO-8859", "SHA-256", "SHA-1", "AES-256", "TLS-1", "HTTP-2", "RFC-7231"}


def ingest(db, repo):
    path = os.path.join(GIT, repo)
    fmt = "%x1e%H%x1f%aI%x1f%an%x1f%P%x1f%B%x1d"
    out = subprocess.run(["git", "-C", path, "log", f"--since={SINCE}", f"--format={fmt}", "--name-only", "--no-renames"],
                         capture_output=True, text=True, errors="replace", check=True).stdout
    db.execute("DELETE FROM gh.git_file_changes WHERE repo=?", (repo,))
    db.execute("DELETE FROM git_commits WHERE repo=?", (repo,))
    nc = nf = 0
    for rec in out.split("\x1e")[1:]:
        head, _, files = rec.partition("\x1d")
        sha, date, author, parents, msg = head.split("\x1f", 4)
        keys = sorted({k for k in KEY.findall(msg) if k not in NOT_JIRA})
        db.execute("INSERT OR REPLACE INTO git_commits VALUES (?,?,?,?,?,?,?)",
                   (repo, sha, date, author, 1 if len(parents.split()) > 1 else 0, json.dumps(keys),
                    1 if BOT.search(author) else 0))
        nc += 1
        for f in files.strip().splitlines():
            f = f.strip()
            if f:
                db.execute("INSERT OR IGNORE INTO gh.git_file_changes VALUES (?,?,?)", (repo, sha, f))
                nf += 1
    print(f"{repo}: {nc} commits, {nf} file changes")


def main():
    db = sqlite3.connect(DB, timeout=60)
    db.execute("ATTACH DATABASE ? AS gh", (os.path.join(os.path.dirname(DB), 'git_history.sqlite'),))  # git_file_changes lives here (D-019); gunzip git_history.sqlite.gz first
    db.executescript("""
    CREATE TABLE IF NOT EXISTS git_commits (repo TEXT, sha TEXT, date TEXT, author TEXT, is_merge INTEGER,
      msg_keys TEXT, is_bot INTEGER, PRIMARY KEY (repo, sha));
    CREATE TABLE IF NOT EXISTS gh.git_file_changes (repo TEXT, sha TEXT, path TEXT, PRIMARY KEY (repo, sha, path));
    """)
    repos = sys.argv[1:] or sorted(d for d in os.listdir(GIT) if os.path.isdir(os.path.join(GIT, d, ".git")))
    for r in repos:
        ingest(db, r)
    db.commit()


if __name__ == "__main__":
    main()
