# Agent Rules - AI Quality Discovery

Research repo: evidence-based product-quality investigation. Status and entry point: `docs/99-sessions/HANDOFF.md`.

## Scope

- Deliver research, specs and drafts only. Company repos, CI, Jira, ServiceNow and production stay read-only (D-029).
- Write in ASD-STE100: short sentences, simple words, one idea per sentence. Use "-", not em dashes.

## Cost

Spend the cheapest model that can do the step.

| Work | Model |
|---|---|
| Data pulls, loading, counting, classification by rules, scripts, commits, logs, formatting | Sonnet (or Haiku for mechanical edits) |
| Synthesis, research design, quality-model decisions, management messages | Opus |

- Read the local DB first: `data/db/quality.sqlite`. Restore with `scripts/db/restore.sh`.
- Pull only the gap: run `python3 -I scripts/db/sync_state.py`, then fetch what it prints (D-033).
- Classify with Python rules first; let a model check a sample.
- Max 2 subagents per round. Each returns 1 page or less.
- Read files by section (offset / grep), not whole.
- One phase per session; start the next session at `HANDOFF.md`.

## Data correctness

- Customer-found bug (CFB) counts exclude MI-investigation tickets (D-032) and invalid resolutions (D-020). Trends use full quarters (D-035).
- Audit what enters a count before trending it: composition by project, type, summary pattern, resolution, month.
- Run `python3 -I scripts/db/secret_scan.py "$PWD"` before adding any archive to `data/archive/`.
- Every claim carries a class (EVIDENCE / CORRELATION / HYPOTHESIS / UNKNOWN) and a confidence.

## Each iteration ends with

1. One row in `docs/99-sessions/iteration-log.md`, one entry in `docs/99-sessions/full-history.md`.
2. New decisions appended to `docs/03-decisions/decision-log.md`.
3. Commit and push. Commit messages carry no co-author line.
