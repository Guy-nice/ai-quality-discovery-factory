# AI Quality Discovery Factory

Evidence-based research initiative to find, prove, and locate the real software quality problem in a complex product (legacy monolith + newer services + growing AI-assisted development) **before** any solution is designed.

## Core principle

No solution before evidence. Every conclusion follows this chain:

```
Observed Signal -> Evidence -> Pattern -> Hypothesis -> Validation Plan
-> Confirmed Problem -> Solution Options -> Recommended Solution
```

Solution design starts only after Gate 4 passes. See [research gates](docs/03-decisions/research-gates.md).

## Current status

| Item | Value |
|---|---|
| Phase | Discovery (Round 1) |
| Current gate | Gate 0 - Charter Alignment: OPEN |
| Last session | [Session 01 - 2026-10-22](docs/99-sessions/2026-10-22-session-01.md) |

## Repository structure

| Path | Purpose |
|---|---|
| `docs/00-charter/` | Charter, problem statement (versioned), glossary |
| `docs/01-discovery/` | Stakeholder questions, discovery map, evidence and access inventory, unknowns and assumptions register |
| `docs/02-research/` | Research plan (versioned), per-source analysis plan |
| `docs/03-decisions/` | Dated decision log, research gate status |
| `docs/99-sessions/` | One log per working session: inputs, outputs, decisions, open items |

## Evidence classification

All claims use one label: `FACT`, `EVIDENCE`, `HYPOTHESIS`, `ASSUMPTION`, `UNKNOWN`, `CONTRADICTION`, `RECOMMENDATION`. Conclusions also state source, confidence (High / Medium / Low), scope, and what could invalidate them.

## Working rules

- Each working session adds a session log and one commit.
- Source references use `[SRC-xxx]` IDs from the [evidence and access inventory](docs/01-discovery/evidence-access-inventory.md).
- No invented organizational facts. Missing information is recorded as `UNKNOWN`.
- No sensitive customer or incident data in this repository until the data-handling rule (U-04) is confirmed.
