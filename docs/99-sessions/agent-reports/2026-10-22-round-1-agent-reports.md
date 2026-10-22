# Agent Reports - Round 1 (verbatim)

**Date:** 2026-10-22 | **Iteration:** 3 | Final reports of research forks, as returned. Synthesis: [findings-round-1](../../02-research/findings-round-1.md).

---

## R1 - CFB quarterly trend

Done. Files (not committed): `data/aggregates/cfb-quarterly.csv`, `data/aggregates/cfb-yearly.csv`, `data/aggregates/README-timeseries.md`.

**Quarterly**

| Quarter | CFB | P1/P2 | P1/P2 % | Invalid % | All bugs | Stories resolved | CFB/100 stories | CFB % of bugs | Open now |
|---|---|---|---|---|---|---|---|---|---|
| 2021-Q1 | 290 | 112 | 38.6 | 38.3 | 3449 | 7968 | 3.64 | 8.4 | 0 |
| 2021-Q2 | 325 | 138 | 42.5 | 40.9 | 3325 | 8747 | 3.72 | 9.8 | 0 |
| 2021-Q3 | 305 | 157 | 51.5 | 38.0 | 3309 | 9860 | 3.09 | 9.2 | 0 |
| 2021-Q4 | 324 | 164 | 50.6 | 32.1 | 3437 | 9646 | 3.36 | 9.4 | 0 |
| 2022-Q1 | 333 | 153 | 45.9 | 43.8 | 3834 | 12318 | 2.70 | 8.7 | 0 |
| 2022-Q2 | 337 | 151 | 44.8 | 39.5 | 3781 | 13481 | 2.50 | 8.9 | 0 |
| 2022-Q3 | 433 | 185 | 42.7 | 43.0 | 4735 | 13441 | 3.22 | 9.1 | 0 |
| 2022-Q4 | 348 | 172 | 49.4 | 43.1 | 4329 | 12971 | 2.68 | 8.0 | 0 |
| 2023-Q1 | 401 | 187 | 46.6 | 35.7 | 5274 | 15892 | 2.52 | 7.6 | 0 |
| 2023-Q2 | 334 | 171 | 51.2 | 35.9 | 4971 | 15795 | 2.11 | 6.7 | 0 |
| 2023-Q3 | 332 | 179 | 53.9 | 33.1 | 5593 | 15471 | 2.15 | 5.9 | 0 |
| 2023-Q4 | 297 | 155 | 52.2 | 31.0 | 4587 | 12953 | 2.29 | 6.5 | 0 |
| 2024-Q1 | 336 | 186 | 55.4 | 23.5 | 10993 | 16248 | 2.07 | 3.1 | 0 |
| 2024-Q2 | 360 | 178 | 49.4 | 23.6 | 6155 | 15341 | 2.35 | 5.8 | 0 |
| 2024-Q3 | 354 | 199 | 56.2 | 20.1 | 5700 | 17949 | 1.97 | 6.2 | 0 |
| 2024-Q4 | 363 | 185 | 51.0 | 24.5 | 5336 | 17440 | 2.08 | 6.8 | 0 |
| 2025-Q1 | 298 | 174 | 58.4 | 33.9 | 5373 | 19883 | 1.50 | 5.5 | 0 |
| 2025-Q2 | 276 | 122 | 44.2 | 29.3 | 5764 | 22676 | 1.22 | 4.8 | 2 |
| 2025-Q3 | 383 | 167 | 43.6 | 31.1 | 5866 | 23573 | 1.62 | 6.5 | 3 |
| 2025-Q4 | 425 | 242 | 56.9 | 34.6 | 5782 | 22847 | 1.86 | 7.4 | 0 |
| 2026-Q1 | 332 | 175 | 52.7 | 31.6 | 7102 | 25472 | 1.30 | 4.7 | 1 |
| 2026-Q2 | 532 | 334 | 62.8 | 35.9 | 10095 | 31595 | 1.68 | 5.3 | 14 |
| 2026-Q3 | 468 | 316 | 67.5 | 29.5 | 18014 | 42960 | 1.09 | 2.6 | 31 |
| 2026-Q4 (partial, to 10-22) | 96 | 58 | 60.4 | 10.4 | 3228 | 9207 | 1.04 | 3.0 | 61 |

**Yearly CFB:** 2017* 297, 2018 989, 2019 1058, 2020 1036, 2021 1244, 2022 1451, 2023 1364, 2024 1413, 2025 1382, 2026 (partial) 1428. (*from first CFB 2017-05-12.)

Jira migration 2022-11-25: 394 CFB in 3 months before, 367 in 3 months after. No step change.

**Observations**
- EVIDENCE - absolute CFB volume up since mid-2025: 2025-H1 574 -> 2026-H1 864 (+51%). 2026-Q2 = 532, highest quarter in series. 2026 YTD (1,428) passes every full year 2021-2025 (flat ~1.25k-1.45k/yr).
- EVIDENCE - severity up faster than volume. P1/P2 2026-Q2 334, 2026-Q3 316 vs earlier quarterly peak 242. P1/P2 share ~50% (2023-24) -> 63-68% (2026-Q2/Q3). 2026-Q3 vs 2024-Q3: CFB ×1.32, P1/P2 ×1.59.
- EVIDENCE - CFB per 100 resolved stories down (3.6 in 2021, ~2.0 in 2024, ~1.1 in 2026-Q3), because stories resolved grew ×2.4 (2024-Q3 -> 2026-Q3).
- HYPOTHESIS - per-story drop may not mean better quality: faster story throughput, smaller stories, or new projects counted. Not checked. Do not report as improvement.
- EVIDENCE - anomalies: all-bug step jumps 2024-Q1 (10,993, ~2× neighbors) and 2026-Q3 (18,014), cause unknown (new project / tool bugs / bulk import?) - do not use all bugs as denominator until explained. Invalid CFB (Cannot Reproduce, Not a Bug, Won't Do, Duplicate) = 37% overall; share ~40% (2021-22) -> ~22% (2024) -> ~30-36% again. Big classification confounder.
- EVIDENCE + caveat - open CFB = 0 for every quarter before 2025-Q2; "open now" cannot show backlog history. Recent quarters (2026-Q3/Q4) have triage lag: high open, low invalid share.

---

## R2 - CFB concentration

Windows W_prev (2024-10-22 to 2025-10-22) vs W_last (2025-10-22 to 2026-10-22). Files (not committed): `data/aggregates/cfb-concentration.csv`, `data/aggregates/README-concentration.md`. Raw dumps in /tmp deleted.

**Total:** 1,318 -> 1,760 CFB (+33.5%). Exact, not normalized.

**R&D VP (exact)**

| VP | W_prev | W_last | Change | Share W_last |
|---|---|---|---|---|
| Analytics and Data | 306 | 473 | +55% | 26.9% |
| Orchestration Core | 170 | 296 | +74% | 16.8% |
| WFM | 129 | 281 | +118% | 16.0% |
| AHW | 251 | 250 | 0% | 14.2% |
| LiveVox & Digital | 205 | 138 | -33% | 7.8% |
| APQ | 106 | 120 | +13% | 6.8% |
| VMS, Recording, QM & FM | 47 | 99 | +111% | 5.6% |
| EMPTY | 93 | 101 | +9% | 5.7% |

**Project top 10 (exact):** CXDV 162->248 (+53%), PMSTND 47->152 (+223%), ORC 50->128 (+156%), DE 181->110 (-39%), AW 179->102 (-43%), CSA 18->96 (+433%), DAT 20->75 (+275%), AOR 32->64 (+100%), CXWFM 65->62 (-5%), CXIA 76->58 (-24%).

**Team top 5** (ranked from sample, counts exact; 185 distinct teams): Hornet 85->76 (-11%), Better Calls Devs 22->71 (+223%), Orchestration II 18->68 (+278%), IN-Agent Copilot 14->57 (+307%), Data-Sandy 14->57 (+307%).

**Sample-only distributions** (n=1,576, 89.5% of W_last; 184 issues from 6 inline page-2 results not saved): Bug Type Functional 800, UI 8, Performance 6, Security 2, empty 760. Number of Incidents 0: 96, 1: 898, 2-4: 322, 5+: 229 (14.5%), null: 31. Component empty 87%; top value Agent-Copilot (53).

**Pareto:** top 3 VPs (A&D, Orch Core, WFM) = 1,050/1,760 = 59.7%. Top 5 teams = 329/1,760 = 18.7% (wide spread). All growth from 4 VPs (A&D, Orch Core, WFM, VMS); AHW flat; LiveVox & Digital down.

**Field completeness W_last (exact):** Component empty 1,546 (87.8%); Bug Type 845 (48.0%); R&D VP 101 (5.7%); Team Name 30 (1.7%).

**Regression and AI markers:** no regression field in fields pulled; regression labels ~6 in sample (`Regression_Fail_26.1`, `26.3_Regression`). AI labels, 11 variants (`AGENTIC_AI_CODE`, `_100`, `AGENT_AI_CODE`, `AI-Assisted`, `UseAIAgent`, `copilot`, `claude-assisted-issue`, ...): exact W_prev 1, W_last 159 (9.0%). Sample: `AGENTIC_AI_CODE` 106, `AGENTIC_AI_CODE_100` 26, `AGENT_AI_CODE` 25. Other repeated labels: `stuck_contact` 61, `LostStuckContacts` 51, `LostStuckAgentContacts` 11 (cross-team theme).

**Observations**
1. EVIDENCE: CFB +33.5% YoY, growth in A&D, Orch Core, WFM; AHW flat; LiveVox & Digital down. Not normalized.
2. EVIDENCE: project shifts look like re-homing (AW -77, DE -71 vs CXDV +86, CSA +78). HYPOTHESIS: reorg distorts project trends. Map projects first.
3. EVIDENCE: AI-code labels ~0 -> 9% of CFB in one year, no naming standard. HYPOTHESIS: label marks fix as AI-made, not cause. Cannot attribute defects to AI as-is.
4. EVIDENCE: Bug Type empty 48%, Component empty 88%. Root-cause classification by these fields not possible. Team and VP usable.
5. HYPOTHESIS: stuck/lost contacts theme spans DAT, ORC, DE. May be legacy-modern boundary cluster; pilot candidate.

---

## R5 - RCA escape-cause classification

240 fixed CFB RCAs (created since 2025-10-22; population 715) classified. Files (not committed): `data/aggregates/rca-classification.csv` (213 rows, labels only), `data/aggregates/README-rca.md`.

**Sample gap:** no issues created 2026-01 to 2026-06 (DESC pages covered 2026-07..10, ASC pages 2025-10..12).

**Fill rate:** 213/240 (88.8%) have answers; 20 (8.3%) template-only or empty; 7 (2.9%) "N/A"/blank. Of 213, 20 (9.4%) state no classifiable cause, mostly PMSTND (WFM).

**escape_cause (n=213):** missing test coverage 59 (27.7%); regression from recent change (RIA miss) 32 (15.0%); scale/performance/concurrency/race 28 (13.1%); unclear/not stated 20 (9.4%); deployment/release process 15 (7.0%); environment/config/data difference 15 (7.0%); requirements/spec gap 14 (6.6%); third-party/integration 11 (5.2%); legacy/unknown behavior 8 (3.8%); test existed but ineffective 7 (3.3%); monitoring gap 4 (1.9%).

**introduced_by:** specific recent change 83 (39.0%); long-standing/legacy code 74 (34.7%); unknown 43 (20.2%); external change 13 (6.1%).
**regression:** no 103 (48.4%); yes 61 (28.6%); unknown 49 (23.0%).
**prevention_action_type:** test added 84 (39.4%); process change 60 (28.2%); code fix only 33 (15.5%); none stated 32 (15.0%); monitoring/alert 4 (1.9%).

**escape_cause by top 5 VP** (AHW 41 / A&D 41 / WFM 34 / Orch Core 33 / VMS 20): missing test 14/11/7/10/2; regression 9/4/6/3/3; scale/race 3/5/1/9/4; unclear 1/4/10/3/0; deployment 2/6/0/1/4; env diff 2/1/2/2/1; requirements 4/2/5/1/1; third-party 0/7/2/0/1; legacy 2/0/0/4/1; test ineffective 3/0/1/0/3. 9 issues empty VP.

**Legacy / AI:** legacy/monolith named in 24/213 (11.3%). AI-generated code named as cause in 0. 4 RCAs name AI tools in review/remediation: in 1, AI PR review flagged the missing test and team did not act; in 1, AI reviewer missed the gap.

**Observations**
1. EVIDENCE (Medium): largest class = untested scenario (27.7%); + ineffective tests = 31%.
2. EVIDENCE (Medium): 39% trace to specific recent change, 35% to latent long-standing code. Of 83 recent-change, 32 are RIA misses (shared code paths, other consumers, copy-paste, fixes not ported across versions/branches).
3. EVIDENCE (Medium): ~22% scale/race/test-env gaps not shown in lower envs (small tenants, single region, data shape).
4. HYPOTHESIS (Low): legacy smaller direct cause than expected (3.8% primary, 11% mention). Self-reported RCAs may under-report.
5. HYPOTHESIS (Low): AI impact not testable from RCAs; template has no AI question.

**Limits:** single rater (Medium confidence); not random; 2026-01..06 gap; self-reported by owning teams.
