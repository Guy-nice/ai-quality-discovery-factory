# Handoff - start a new session here (saves tokens)

Read only these, in order: `README.md` (status) -> `docs/00-brief.md` -> `docs/07-quality-model/quality-model-v0.md` -> `docs/03-decisions/decision-log.md` (last 10 rows) -> `docs/99-sessions/iteration-log.md` (last 5 rows).

## Rules
- No PRs or changes in company systems (D-029). Specs and research only.
- Data: never re-download. `scripts/db/restore.sh`, then `scripts/db/sync_state.py` for gap-only pulls (D-033). Secret scan before archiving.
- Exclude MI-investigation tickets from CFB counts (D-032). Valid = invalid resolutions removed (D-020).
- Each iteration: one line in `iteration-log.md`, entry in `full-history.md`, commit + push, no co-author line.
- Write in ASD-STE100, short.
- Cost: Opus only for synthesis and design. Data work in subagents with `model: "sonnet"` (forks always run on the parent model). Max 2 agents per round, 1-page outputs. Use `/effort low` for mechanical steps.

## State (2026-10-25)
- Quality model v0 draft (D-034); experiments X1-X5 proposed; awaiting management decisions (deck v2 slide 11).
- Open: U-26 ServiceNow record read, U-27 team map, C-08 ServiceNow P1 fall, human validation.
- Shared page: https://claude.ai/artifact/QDD8cDsvj7t1NzPsZgdLdf
