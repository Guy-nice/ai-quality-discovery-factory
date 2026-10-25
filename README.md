# AI Quality Discovery Factory

Evidence-based research initiative to find, prove, and locate the real software quality problem in a complex product (legacy monolith + newer services + growing AI-assisted development) **before** any solution is designed.

## Core principle

No solution before evidence. Every conclusion follows this chain:

```
Observed Signal -> Evidence -> Pattern -> Hypothesis -> Validation Plan
-> Confirmed Problem -> Solution Options -> Recommended Solution
```

Solution design starts only after Gate 4 passes. See [research gates](docs/03-decisions/research-gates.md).

**Mission v2 (2026-10-25): [reassessment](docs/06-reassessment/mission-v2-reassessment.md) | [findings round 1](docs/06-reassessment/m2-findings-round-1.md) | [quality definition v1](docs/06-reassessment/quality-definition-v1-draft.md). Headline corrected (D-032): CFB +29%, P1/P2 +46%. Solution docs, gates and the deck are provisional (D-030).**

**Previous summary: [Summary and recommendations](docs/05-summary/summary-and-recommendations.md)** | [Management deck (pptx, superseded numbers)](docs/05-summary/management-deck.pptx) | [1-page brief](docs/00-brief.md)

## Current status

| Item | Value |
|---|---|
| Phase | Mission v2 reassessment; solutions provisional (D-030) |
| Gates | G0 PASSED (i), G1 PARTIAL, G2 PASSED (i), G3 PASSED (i), G4 PASSED (interim, data-based) |
| Problem statement | [v4](docs/00-charter/problem-statement-v4.md) |
| Latest findings | [Round 1](docs/02-research/findings-round-1.md), [Round 2](docs/02-research/findings-round-2.md), [Round 3](docs/02-research/findings-round-3.md), [Round 4](docs/02-research/findings-round-4.md) |
| Last session | [Session 10 - 2026-10-22](docs/99-sessions/2026-10-22-session-10.md) |
| History | [Iteration log](docs/99-sessions/iteration-log.md), [Full history](docs/99-sessions/full-history.md) |
| Pilot | Orchestration Core - contact routing and lifecycle flow (D-010, D-016) |
| Database | [data/db](data/db/README.md) - `quality.sqlite` |
| Shared summary (company) | [claude.ai doc: AI Quality Discovery - Research Summary](https://claude.ai/artifact/QDD8cDsvj7t1NzPsZgdLdf) |

## Repository structure

| Path | Purpose |
|---|---|
| `docs/00-charter/` | Charter, problem statement (versioned), glossary |
| `docs/01-discovery/` | Stakeholder questions, discovery map, evidence and access inventory, unknowns and assumptions register |
| `docs/02-research/` | Research plan (versioned), per-source analysis plan |
| `docs/03-decisions/` | Dated decision log, research gate status |
| `docs/04-solutions/` | Solution options, wave 1 specs, drafts |
| `docs/05-summary/` | Summary and recommendations, management deck |
| `scripts/deck/` | Deck build script |
| `docs/99-sessions/` | One log per working session: inputs, outputs, decisions, open items |
| `data/aggregates/` | Aggregated counts and label-only classifications, with exact JQL and method per dataset |
| `scripts/analysis/` | Scratch analysis scripts used to make the aggregates |
| `scripts/db/` | DB schema, loader, R8 / R9 analysis scripts |
| `data/db/` | Research database (see README) |
| `docs/99-sessions/agent-reports/` | Verbatim reports of research agents |
| `docs/99-sessions/replies/` | Verbatim long replies |

## Evidence classification

All claims use one label: `FACT`, `EVIDENCE`, `HYPOTHESIS`, `ASSUMPTION`, `UNKNOWN`, `CONTRADICTION`, `RECOMMENDATION`. Conclusions also state source, confidence (High / Medium / Low), scope, and what could invalidate them.

## Working rules

- Each iteration (prompt -> result) adds one line to the [iteration log](docs/99-sessions/iteration-log.md), then one commit and push.
- Each working session adds a session log.
- All text uses ASD-STE100 (Simplified Technical English): short sentences, simple words, one idea per sentence.
- Source references use `[SRC-xxx]` IDs from the [evidence and access inventory](docs/01-discovery/evidence-access-inventory.md).
- No invented organizational facts. Missing information is recorded as `UNKNOWN`.
- No sensitive customer or incident data in this repository until the data-handling rule (U-04) is confirmed.
- Not stored by design: raw Jira dumps (D-004), security finding details (D-013).
