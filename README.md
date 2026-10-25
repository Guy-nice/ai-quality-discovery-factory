# AI Quality Discovery Factory

Evidence-based investigation of product quality in CXone (legacy monolith, modern services, AI-assisted development, independent teams). It finds where and why quality fails, and recommends actions that teams can test before rollout.

## Start here

| Need | Link |
|---|---|
| **What we do now** | [Action plan v1](docs/05-summary/action-plan-v1.md) |
| 1-page summary | [Brief](docs/00-brief.md) |
| Gates / Definition of Done v2 | [DoD v2 doc](docs/05-summary/dod-v2-evidence-based.md), [DoD v2 deck (pptx)](docs/05-summary/dod-v2-deck.pptx) / [pdf](docs/05-summary/dod-v2-deck.pdf) |
| Management slides | [Deck v3 (pptx)](docs/05-summary/management-deck-v3.pptx) / [pdf](docs/05-summary/management-deck-v3.pdf) |
| Company page | [Shared summary](https://claude.ai/artifact/QDD8cDsvj7t1NzPsZgdLdf) |
| Quality model and experiments | [Model v0](docs/07-quality-model/quality-model-v0.md), [experiment protocols](docs/07-quality-model/experiment-protocols-v0.md) |
| Agent rules / new session | [AGENTS.md](AGENTS.md), [HANDOFF](docs/99-sessions/HANDOFF.md) |

## The answer in short

- **Quality fell in severity, not volume:** P1/P2 customer-found bugs +49%, all customer-found bugs +13% (Jan-Sep 2026 vs 2025, MI investigations removed).
- **Customers find our problems first:** 96% of P1 incidents enter through customer cases.
- **Almost half of valid bugs are business-correctness failures** (report data, routing, contact lifecycle).
- **AI is not riskier per change**; it adds volume and larger changes in hotspot code.
- **Teams differ strongly**, so one workflow does not fit all.

## Action plan

| | What |
|---|---|
| **Keep** | RCA for P1/P2 bugs; feature toggles; AI under the same rules as all changes; Xray |
| **Change** | Bug intake (defect vs MI vs expectation gap); Go/No-Go based on data; trusted E2E signal before it blocks; review depth by change size in hotspot code; QSU per team |
| **Stop** | Raw bug count as the quality number; one gate set for all teams; unused Jira quality fields; "mandatory" items with no control |
| **Start** | 8-dimension quality model; team-service-code map; detection monitors for routing, lifecycle, report data; expectation-gap triage; owner backups; experiments X1-X5 |

| When | What |
|---|---|
| Now (Nov 2026) | Management decisions; start X1 (intake) and X2 (detection, shadow); QSU per team; triage failing routing E2E |
| Q1 2027 | X3/X4 step 1, X5; monthly team review; AI re-test (90 days) |
| April 2027 | Results vs controls; quality model v1 with justified targets; decide which checks block |
| H2 2027 | Spread proven practices; decide RIA agents, mutation testing, agent harness from evidence |

Gates and quality automation are **means**: a few blocking checks where risk is proven now; the rest after experiment results.

## Status

| Item | Value |
|---|---|
| Phase | Action plan v1 (D-039); awaiting management decisions (deck v3, last slide) |
| Gates | G0-G3 passed (interim); G4 reopened under mission v2 (D-030); experiments decide readiness |
| Open | ServiceNow record read (U-26); team-service map (U-27); ServiceNow P1 fall (C-08); human validation |
| Data | All data in repo (D-033): [data/db](data/db/README.md), `data/archive/` |
| History | [Iteration log](docs/99-sessions/iteration-log.md), [full history](docs/99-sessions/full-history.md), [decision log](docs/03-decisions/decision-log.md), [why numbers changed](docs/06-reassessment/why-numbers-changed.md) |
| Earlier phase (superseded) | [Summary v1](docs/05-summary/summary-and-recommendations.md), [solution options](docs/04-solutions/solution-options-v0.md), [deck v1](docs/05-summary/management-deck-v1-superseded.pptx) |

## Repository structure

| Path | Purpose |
|---|---|
| `docs/00-charter/` | Charter, problem statement (versioned), glossary |
| `docs/01-discovery/` | Stakeholder questions, discovery map, evidence and access inventory, unknowns and assumptions register |
| `docs/02-research/` | Research plan (versioned), per-source analysis plan |
| `docs/03-decisions/` | Dated decision log, research gate status |
| `docs/04-solutions/` | Solution options, wave 1 specs, drafts |
| `docs/06-reassessment/` | Mission v2: reassessment, findings, quality definition, corrections |
| `docs/07-quality-model/` | Quality model (draft) |
| `data/archive/` | All raw data, compressed and dated (D-033) |
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
