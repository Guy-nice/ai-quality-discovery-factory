# Research Database

## All data is in the repo (D-033)

| What | Where (committed) | Restore |
|---|---|---|
| Structured data | `data/db/quality.sqlite` | ready |
| Text (summaries, RCA, RIA) | `data/archive/raw_local-<date>.sqlite.gz` | `scripts/db/restore.sh` |
| Git file history | `data/db/git_history.sqlite.gz` | `scripts/db/restore.sh` |
| Raw source dumps + blobless git clones | `data/archive/raw-<source>-<date>.tar.gz` | `scripts/db/restore.sh` |

**Rule: never re-download.** Query the local DB first. To refresh, run `python3 -I scripts/db/sync_state.py`: it shows each source's watermark and the query for the **gap only**. Pull the gap, load it, add a new dated archive (`raw-<source>-<date>.tar.gz`; old archives stay as they are), then re-run `sync_state.py`.

Secret scan before each archive: `python3 -I scripts/db/secret_scan.py "$PWD"`. The 2026-10-25 scan found 10 matches, all code identifiers (false positives).


All data pulled for this research is stored here (user order, iteration 7).

| File | Content | In Git |
|---|---|---|
| `git_history.sqlite.gz` | Git file changes (184k rows: repo, sha, path). Gunzip to `git_history.sqlite`; scripts ATTACH it as `gh` (D-019) | Yes (gzipped) |
| `quality.sqlite` | Structured data: issues (keys, dates, VP, team, priority, AI flag, labels, RCA/RIA fill state), links, causal links, RCA classifications, JQL counts, query log, all aggregate tables (`agg_*`) | Yes |
| `raw_local.sqlite` | Free text: summary, RCA, RIA per issue | **No** (gitignored, D-004: may hold customer data) |
| `../raw/` | Raw MCP JSON dumps | **No** (gitignored) |

## Load and rebuild

- Loader: `scripts/db/load.py` (modes: `dump`, `count`, `csv`). Schema: `scripts/db/schema.sql`.
- Each dump load writes one row to `query_log` (time, purpose, JQL, file, rows). Each count writes one row to `jql_counts`.
- Re-load is idempotent (upsert by issue key).

## Core tables

| Table | Key | Notes |
|---|---|---|
| `issues` | key | `is_cfb` = 1 when from CFB query. `rca_state` / `ria_state` = empty / template / filled. `ai_implemented` = cf_15229. `ai_label` = 1 when AI label present (means AI fix, D-012). |
| `issue_links` | key, type, direction, other_key | From Jira issuelinks |
| `causal_links` | cfb_key, causing_key | From RCA text ("How was it introduced") or Jira links (R8) |
| `rca_class` | key, round, rater | Escape-cause classification. Rounds: `R5-round1`, `R9` |
| `jql_counts` | purpose, label | Count-only queries |
| `query_log` | id | Audit trail of every load |
| `agg_*` | - | Imported from `data/aggregates/*.csv` |
| `flow_tags` | key | Pilot sub-flow tag (R9, precision 80%) |
| `confluence_pages` | page_id | One-line summaries (R9) |
| `git_repos` | org, repo | Repo list + activity (R9) |
| `git_commits` | repo, sha | 7,866 commits, 24 months; Jira keys from message only (R3) |
| `r3_*`, `r14_ownership` | - | Hotspots, flags, ownership (R3, R14) |
| `migration_events`, `migration_mentions`, `migration_causal` | - | R11 |
| `prs`, `pr_commits`, `team_quarter`, `team_r15` | - | R15, R16 |
| `failure_modes` | key | SO-1 state failure modes |
| `ci_runs`, `ci_jobs`, `test_failures` | - | SO-3A CI data (test names only) |
| `so45_owners`, `so45_size_risk` | - | SO-4/5 |
| `metrics_monthly` | month | S1-S7 (`scripts/db/metrics.py`) |

Residual risk: Jira labels are stored as-is; a few labels may hold customer names. The repo is private.

## Example

```sql
SELECT rnd_vp, COUNT(*) FROM issues WHERE is_cfb = 1 AND created >= '2025-10-22' GROUP BY 1 ORDER BY 2 DESC;
```

Open with `sqlite3 data/db/quality.sqlite` or any SQLite browser.
