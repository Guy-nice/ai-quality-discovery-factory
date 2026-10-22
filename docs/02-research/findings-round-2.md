# Research Findings - Round 2

**Date:** 2026-10-22 | **Sources:** SRC-001 Jira, SRC-002 Confluence (read-only) | **Data:** `data/aggregates/r1b-*`, `r2b-*`, `r6-*`, `r7-*`

## F6 - Throughput jumps are data imports (R1b, U-13 closed)

| Jump | Raw | Cause | Adjusted |
|---|---|---|---|
| Bugs 2024-Q1 | 10,993 | Project ENG bulk load 2024-01-01..07 (4,738 bugs) | 5,905 |
| Bugs 2026-Q3 | 18,014 | New project CGY, Azure DevOps import (`ado-bug`) | 11,651 |
| Stories 2026-Q3 | 42,960 | CGY import of done items (8,967) | 33,993 |

| CFB per 100 stories (adjusted) | 2025 | 2026 | Change |
|---|---|---|---|
| Q2 | 1.22 | 1.68 | **+38%** |
| Q3 | 1.62 | 1.38 | -15% |

- **EVIDENCE (High):** Raw all-bug counts are not usable as a denominator (imports).
- **EVIDENCE (High):** C-01 is weaker than reported in round 1. The per-story rate rose in Q2 and fell only 15% in Q3.
- **HYPOTHESIS (Medium):** AI work splits work into more, smaller stories, which inflates the denominator. Story size is not measured (U-19).
- Non-AI, non-import story growth: +57% (2024-Q3 to 2026-Q3), spread across projects.

## F7 - AI labels and AI adoption (R7, U-17 closed)

- **FACT (High):** `AGENTIC_AI_CODE` is set by a GitHub Action when Claude Code opens the PR. On merge it becomes `AGENTIC_AI_CODE_<pct>` (share of AI lines). Source: Confluence 3915612323 (AI Metrics Automation).
- **FACT (High):** "Implemented by AI Agent" (cf_15229) is set by a monthly PgM KPI audit. Source: Confluence 4011230379.
- **EVIDENCE (High):** On a bug, the label means the **fix** was AI-made, not the cause. Changelogs show the label added after creation in 7 of 7 sampled CFBs.
- **EVIDENCE (High):** AI adoption (stories with AI indicator, resolved):

| Quarter | 2025-Q3 | 2025-Q4 | 2026-Q1 | 2026-Q2 | 2026-Q3 |
|---|---|---|---|---|---|
| AI stories % | 0.4 | 2.0 | 10.2 | 31.3 | 22.8 |

- **EVIDENCE (High):** The AI adoption ramp (2026-Q1/Q2) matches the CFB rise in time (2026-Q2 = peak CFB quarter, 532). A timing match is **not** a cause.
- **EVIDENCE (Low, n=27):** 33% of causing items resolved in 2026 were AI-implemented vs a 22% base rate. Not significant.
- **Method now possible (R8):** Extract the causing Jira key from RCA "How was it introduced?" (31% of RCAs name one). Compare the CFB rate for AI vs non-AI stories by quarter and team. Formal "is caused by" links exist on only 2.7% of CFBs.

## F8 - Controls inventory (R6)

| Control | Fill / use | Class |
|---|---|---|
| Acceptance Criteria (Epic / Story) | 100% / 88% | Policy |
| RIA (Epic) | 58% real content | Policy, not blocking |
| RIA (Story) | 0% (39/40 template) | Not used |
| RIA (CFB fix) | 88% | Policy |
| RCA (CFB fix) | 89%; review status set 33% | Policy |
| EOR Broken? / Mitigation? | 0% real | Not used |
| Quality / Architecture / Code Review Status | 0.3-2% | Not used |
| QPlan, Escape Analysis, Test Stage Found, Gating, Reopen Counter | 0-0.6% | Not used |
| Xray Test link (Epic / Story / CFB fix) | 25% / 18% / 30% | Suggested |
| Domain Go/No-Go (9 exit criteria, per release) | 26.4 pages all "TBD" | Policy, human gate |
| Sonar + Aikido pre-push hooks | Opt-in (pages 2026-10-17) | Real control only if installed |
| CI Sonar gate | Exists; enforcement UNKNOWN | UNKNOWN |
| Mutation Testing Agent | Rollout | Suggested |

- **EVIDENCE (High):** 9 of about 15 Jira quality fields are under 2% filled. Most controls are policy on paper.
- **EVIDENCE (Medium):** RIA happens at Epic level, not at Story level. Regressions come from Stories and Bugs as much as from Epics.
- **EVIDENCE (Medium, n=14):** Regressions: RIA done but missed 7, RIA not done 7. Enforcing RIA alone would cover at most half.
- **EVIDENCE (High):** Xray is used heavily: 137k tests and 1.15M executions in 2026. Links to requirements are weak (18-25%). High activity does not mean traceability.
- **EVIDENCE (High):** No blocking automated gate was found in Jira or Confluence. The release gate is human.
- **UNKNOWN U-18:** No "XCX Quality Process" page was found.

## F9 - Pilot selection (R2b, Gate 3)

| Candidate | Density | Criticality | Growth | Boundary | Score /50 |
|---|---|---|---|---|---|
| **Orchestration Core** | 4 | 5 | 4 | 1 | **37** |
| Analytics and Data | 5 | 4 | 3 | 1 | 35 |
| Routing flow | 2 | 3 | 5 | 5 | 35 |
| WFM | 4 | 3 | 5 | 1 | 33 |
| Stuck/lost contacts flow | 2 | 3 | 2 | 5 | 29 |

Weights: density 3, criticality 3, growth 2, boundary 2.

- **EVIDENCE (High):** Orchestration Core has the highest severity: 70% P1/P2, 3.8 incidents per CFB, 19% of CFBs with 5+ incidents.
- **EVIDENCE (Medium):** Routing CFBs: 40 -> 106 (+165%), 62% P1/P2, across 3 VPs. Orchestration Core holds 55% of them.
- **EVIDENCE (Medium):** Stuck/lost contacts: 245 CFBs all time. It peaked in waves in 2025 and is falling in 2026. Low incident load (1.8 per CFB). It is part of the flow, not the main pilot.
- **Recommendation:** Pilot = Orchestration Core, bounded to the **contact routing and lifecycle flow** (routing + stuck/lost contacts). Rank 1 also without the boundary weight. Supersedes D-009.
- **Could invalidate:** keyword-based routing theme; team renames; invalid CFBs not removed per VP; weights are a judgment call (A&D at 35 is close).

## Security note

A security issue in Jira data was found outside scope and reported to the lead directly. Details are not stored here.
