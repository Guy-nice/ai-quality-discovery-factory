"""Gap-only refresh: record what each source holds and print the query for the missing part.

Usage (repo root):
  python3 -I scripts/db/sync_state.py            # refresh table sync_state and print gap queries
Then pull only the gap with the printed query, load it (scripts/db/load.py or the source script),
archive the new raw files as data/archive/raw-<source>-<date>.tar.gz, and re-run this script.
"""
import datetime
import os
import re
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")

SOURCES = [
    ("jira_cfb", "SELECT MAX(created), COUNT(*) FROM issues WHERE is_cfb = 1",
     'issuetype = Bug and salesforceAssociatedTypes is not EMPTY and (created >= "{d}" or updated >= "{d}")'),
    ("jira_all_issues", "SELECT MAX(last_pulled_at), COUNT(*) FROM issues",
     'key in (<keys referenced by new causal_links>) - pull only keys missing from issues'),
    ("git_commits", "SELECT MAX(date), COUNT(*) FROM git_commits",
     "git -C data/raw/git/<repo> fetch && git log --since={d} (per repo, then scripts/db/r3_git_ingest.py)"),
    ("github_prs", "SELECT MAX(merged), COUNT(*) FROM prs",
     "gh pr list --state merged --search 'merged:>={d}' (per pilot repo, then scripts/db/r16_prs.py)"),
    ("ci_runs", "SELECT MAX(created), COUNT(*) FROM ci_runs",
     "gh run list --created '>={d}' (per workflow, then scripts/db/so3a_ci.py)"),
    ("servicenow_counts", "SELECT MAX(period), COUNT(*) FROM sn_aggregates",
     "snow_get_stats with opened_at>={d} (counts only until U-26)"),
]


def main():
    db = sqlite3.connect(DB)
    db.execute("CREATE TABLE IF NOT EXISTS sync_state (source TEXT PRIMARY KEY, watermark TEXT, rows INTEGER, "
               "checked_at TEXT, gap_query TEXT)")
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    for name, sql, gap in SOURCES:
        try:
            mark, rows = db.execute(sql).fetchone()
        except sqlite3.OperationalError as e:
            mark, rows = None, 0
            gap = f"table missing ({e}); full pull needed"
        d = (mark or "2025-01-01")[:10]
        q = re.match(r"(\d{4})-Q(\d)", d)
        if q:
            d = f"{q.group(1)}-{3 * int(q.group(2)) - 2:02d}-01"
        query = gap.replace("{d}", d)
        db.execute("INSERT OR REPLACE INTO sync_state VALUES (?,?,?,?,?)", (name, mark, rows, now, query))
        print(f"{name:18} rows={rows:<7} watermark={mark}\n  gap: {query}")
    db.commit()


if __name__ == "__main__":
    main()
