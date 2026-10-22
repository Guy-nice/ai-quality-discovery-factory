# Research Findings - Round 3

**Date:** 2026-10-22 | **Sources:** SRC-001 Jira, SRC-002 Confluence, SRC-004 Git (read-only) | **DB:** [`data/db/quality.sqlite`](../../data/db/README.md)
**Detail:** [R8 AI vs non-AI](r8-ai-vs-non-ai.md), [R9 pilot deep dive](r9-pilot-orchestration-core.md)

## F10 - AI-implemented changes vs non-AI changes (R8, P-04)

Method: from 1,209 fixed CFBs (2025+), the causing Jira key was taken from the RCA "How was it introduced" section (316 CFBs, 26%; precision 19/20) plus Jira links. Rate = CFB-causing items / items resolved, for AI (cf_15229 = Yes) vs non-AI, per quarter of causing item resolution. Projects CGY and ENG are excluded.

| Quarter | AI | Non-AI | Rate ratio |
|---|---|---|---|
| 2026-Q1 | 3 / 2,819 | 26 / 28,377 | 1.16 |
| 2026-Q2 | 10 / 10,041 | 16 / 29,325 | 1.83 |
| 2026-Q3 | 7 / 10,012 | 14 / 36,010 | 1.80 (short exposure) |

| Scope | RR | 95% CI |
|---|---|---|
| Pooled 2026-Q1..Q2, crude | 1.39 | 0.75-2.59 |
| Reviewed-by-AI-audit items only (Yes vs No), Q1..Q3 | **1.03** | 0.57-1.86 |
| Stories only | 1.61 | 0.74-3.49 |
| Per VP | 0.50-2.44 | all CIs include 1 |

- **EVIDENCE (Low-Medium):** No higher CFB rate per AI-implemented change. In like-for-like (reviewed) items, RR is about 1.0.
- **Limit:** only 13-29 AI causing items. A small effect (RR < 2) cannot be excluded.
- **Bias:** cause-naming rate differs by VP (A&D 9%, WFM 16%, others 31-41%). It does not differ between AI and non-AI fixes (27% vs 26%). AI items have shorter exposure, which works against finding AI CFBs.
- **HYPOTHESIS (Medium):** The 2026 rise is mainly more change volume. It is not a higher per-change risk from AI.
- **CONTRADICTION C-07:** F6 shows adjusted CFB per story +38% (2026-Q2 vs 2025-Q2). So the per-change escape rate is not fully constant over time, but AI and non-AI changes have the same rate inside each quarter. Possible reasons: a mix shift to higher-risk areas (Orchestration Core, migrations) or system-level effects (many parallel changes). See PH-2.

## F11 - Pilot: Orchestration Core, contact routing and lifecycle (R9)

Data: 466 CFBs (W_prev 170, W_last 296), 108 RCAs classified, 30 Confluence pages, 13 Git repos.

| Sub-flow | W_prev -> W_last | Note |
|---|---|---|
| Routing / skill / queue | 39 -> 58 | 7.1 incidents per CFB; 26% with 5+; median 28 days to fix |
| Stuck / lost contact | 12 -> 57 (+375%) | Cleanup jobs used as a fix; many "unknown" causes |
| ACD / contact state | 22 -> 40 | 58% invalid |
| IVR / Studio | 16 -> 27 | |
| **Flow total** | **123 -> 218 (+77%)** | Admin/config only +8% |

Tag precision: 80% for the sub-flow, 93% for in-flow vs out-of-flow. 42% of pilot CFBs close as invalid.

| Escape cause | Pilot (n=108) | Other VPs (n=180) |
|---|---|---|
| Missing test coverage | 28% | 27% |
| **Scale / race / event ordering** | **26%** (29% in-flow) | 11% |
| RIA miss | 7% | 16% |
| Legacy behavior | 7% | 2% |

- Legacy code is named in 20% of pilot RCAs (11% overall). 3 of 108 prevention actions add monitoring. 0 RCAs name AI code as a cause.

**Pilot root-cause hypotheses**

| ID | Hypothesis | Confidence | Main evidence | Could invalidate |
|---|---|---|---|---|
| PH-1 | Distributed state races: out-of-order or dropped events between the VC monolith, Entity Management and the routing services (AFM/VFM, Contact Retry). No concurrency tests. | Medium-High | 26-29% race escapes; Findmatch gap analysis (Confluence 4072866234): no real-Kafka/DB integration test, no concurrency test | Code review shows concurrency tests exist; races are isolated to one service |
| PH-2 | 5 parallel 2026 migrations change the same contact lifecycle: VFM->AFM, Voltron decoupling, State Streams KDA->EKS, .NET upgrades, tenant moves | Medium | Confluence architecture pages; RCAs; timing | CFB rise not aligned to migration dates |
| PH-3 | Library / serializer swaps in the monolith break behavior; no parity tests | Medium | 11 RCAs | Parity test suite found |
| PH-4 | Production scale, real streams, failover and customer scripts cannot be reproduced before release | Medium | Environment + scale = 35% | Perf / chaos env exists and runs; AFM chaos plan shows "not started" |
| PH-5 | Customers detect issues first; monitoring is rarely added | Medium | 3/108 monitoring actions | Alert data shows early internal detection |

**Test assets:** 1 of 50 Orchestration Core epics resolved in 2026 has a direct Xray Test link (story links not checked). About half of the Playwright E2E suite is marked fixme or skipped (Findmatch analysis). The AFM chaos test plan shows "not started".

**Component map (from docs):** legacy = VC monolith, VFM. New = AFM, Entity Management, State Streams, TFS.

**Git:** read access to the `inContact` org confirmed. Commits in the last 12 months: AFM 254, agent-capacity 222, contact-retry 182, VFM 20. The VC monolith is not in GitHub (probably in TFS), so it needs TFS access (U-21).

## F12 - Classification reliability (partial R5b)

Second rating of 33 RCAs: escape cause 79% agreement, regression 88%, prevention 97%, other columns 100%. **Limit:** both raters are Claude, so they are not independent. A human SME must still rate about 20 RCAs.
