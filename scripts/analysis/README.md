# Analysis Scripts

Scratch scripts used by research forks (2026-10-22). Kept for traceability.

- Input: Jira MCP query results saved as JSON under `/tmp/<rX>/` at run time. Raw dumps are **not** in repo (D-004: may hold customer text). Re-create them with the JQL in `data/aggregates/README-*.md`.
- Output: aggregate files in `data/aggregates/`.
- Run with `python3 -I`. Paths are hard-coded to `/tmp` scratch dirs.

| Dir | Research item | Output |
|---|---|---|
| `r1b/` | Throughput jump causes | `r1b-throughput.csv` |
| `r5-rca/` | RCA extract, show, aggregate (classification was done by reading, codes in scratch `labels.txt`) | `rca-classification.csv` |
| `r6/` | Controls fill rates | `r6-controls.csv` |
| `r7/` | AI label changelog check | `r7-ai-labels.csv` |

Not saved: R1 time series and R2 concentration (counts via JQL only, no script), R2b tally scripts (deleted by fork).
