# Answers: Production Issues, AI Code, AI-Caused Issues, Test Gaps

**Date:** 2026-11-01 | **Data:** `data/db/quality.sqlite` (Jira to 2026-10-25, ServiceNow aggregates, 1,663 merged PRs in 13 pilot repos) | **Rules:** MI investigation tickets removed (D-032); full quarters for trends (D-035) | **Report:** [management report](management-report.md)

2026-Q4 is partial (data to about 2026-10-25). Do not compare it with full quarters.

## 1. Over time, how many issues have we had in production?

| Quarter | Customer-found bugs | of which P1/P2 | Incidents from customer cases (all priorities) | of which P1 |
|---|---|---|---|---|
| 2025-Q1 | 297 | 173 | 687 | 113 |
| 2025-Q2 | 274 | 120 | 832 | 157 |
| 2025-Q3 | 383 | 167 | 899 | 163 |
| 2025-Q4 | 425 | 242 | 1,084 | 170 |
| 2026-Q1 | 326 | 170 | 905 | 68 |
| 2026-Q2 | 410 | 257 | 923 | 74 |
| 2026-Q3 | 346 | 258 | 933 | 85 |
| 2026-Q4 (partial) | 80 | 49 | 260 | 22 |

**Read:**
- **Customer-found bugs:** Jan-Sep 2025 = 954; Jan-Sep 2026 = 1,082 (+13%). EVIDENCE, high.
- **Severe bugs (P1/P2):** 460 to 685 (+49%). EVIDENCE, high.
- **Incidents from customer cases:** 3,502 in 2025 (4 quarters). Q1-Q3 2026 is 2,761 vs 2,418 in Q1-Q3 2025 (+14%). EVIDENCE, high.
- **P1 incidents fell by about half from 2026-Q1.** The cause is open (C-08). A change in how P1 is set is possible. UNKNOWN.
- **Changes:** failed normal changes fell from 3.9% (2025-H1) to 2.6% (2026 Jul-Oct). Emergency changes rose from 6.8% to 14.4% of all changes. EVIDENCE, high.

Sources: `issues` (is_cfb), `sn_aggregates`; [why numbers changed](../06-reassessment/why-numbers-changed.md), [impact](../06-reassessment/m2-impact-servicenow.md).

## 2. Over time, how much new code has been added or changed by AI?

Scope: 13 pilot repos (monolith and routing / orchestration services). PRs over 5,000 changed lines are left out of the line share, because a few bulk PRs (generated or moved code) distort it.

| Quarter | Merged PRs | AI PRs (% of PRs) | AI share of changed lines | Bulk PRs left out |
|---|---|---|---|---|
| 2025-Q1 | 52 | 0% | 0% | 7 |
| 2025-Q2 | 78 | 0% | 0% | 3 |
| 2025-Q3 | 61 | 4.9% | 14.4% | 0 |
| 2025-Q4 | 111 | 14.4% | 10.1% | 13 |
| 2026-Q1 | 184 | 27.2% | 23.7% | 15 |
| 2026-Q2 | 404 | 40.8% | 54.6% | 39 |
| 2026-Q3 | 526 | 43.9% | 55.9% | 34 |
| 2026-Q4 (partial) | 129 | 58.9% | 70.6% | 7 |

**Read:**
- **AI went from 0% to about half of PRs and changed lines in 18 months.** EVIDENCE, high (within the pilot repos).
- **Total PR volume grew about 10 times** (2025-Q1 to 2026-Q3).
- **AI PRs are larger:** median 227-233 changed lines vs 57-62 for other PRs (2026). They touch tests more (62% vs 35-40%).
- **AI share of hotspot PRs:** 5% (2025-Q4) to 47% (2026-Q4, partial).

**Limits:**
- AI is found by markers in PR text (for example a co-author line). AI use without a marker is not counted. So these numbers are a **minimum**.
- Only 13 pilot repos. An org-wide view needs the data of the AI-metrics GitHub Action (Confluence 3915612323). We have not pulled it.

Sources: `prs` (ai_flag); [AI analysis](../06-reassessment/m2-e9-ai.md), [AI PRs](../02-research/r16-ai-prs.md).

## 3. How many of the issues were written with AI?

**Short answer:** at least 31 customer-found bugs trace back to AI-marked work, all in 2026. The true number is unknown, because the cause is recorded for only 23% of bugs.

| Measure | Value | Class, confidence |
|---|---|---|
| Valid customer-found bugs, 2025-2026 | 1,452 | EVIDENCE, high |
| With a known causing change (story, bug or PR) | 330 (22.7%) | EVIDENCE, high |
| Causing change marked as AI (Jira AI field or label, or AI PR) | 31 (all 2026) | EVIDENCE, medium |
| Share of 2026 known-cause bugs | 31 of 164 (19%) | EVIDENCE, medium |
| Share where AI status can be checked | 31 of 81 (38%) | EVIDENCE, low (small sample) |

**Is AI code riskier? Per PR, no difference was found:**

| Design (same repo, size, hotspot, quarter) | AI PRs | Other PRs |
|---|---|---|
| PRs with a customer-bug fix on the same files within 90 days | 37 of 236 (15.7%) | 87 of 414 (21.0%) |
| Risk ratio (95% interval) | 0.84 (0.64-1.11) | - |

- The interval includes 1, so there is **no proof either way**. CORRELATION, medium.
- The 38% AI share among checkable causes is close to the AI share of PRs (about 40%). This also fits "no more risk per change".
- **What drives the rise:** AI adds volume and larger changes in hotspot code. In hotspot code, large PRs link to more follow-up fixes (21% to 54%). HYPOTHESIS, low-medium.

**To answer this well in future:** record the causing change on every valid bug (gate G0.2, experiment X1), and label AI PRs (G2.2).

Sources: `causal_links`, `issues`, `prs`, `agg_m2_e9_ai`; [AI analysis](../06-reassessment/m2-e9-ai.md), [owners and PR rules](../04-solutions/so4-so5-owners-pr-rules.md).

## 4. How do we close the gaps in what is tested?

**Why bugs escaped** (108 pilot customer bugs with a root-cause analysis, Orchestration Core):

| Escape cause | Share | Other VPs (n=180) |
|---|---|---|
| Missing test coverage (scenario not tested) | 27.8% | 27.2% |
| Scale, performance, concurrency, race | 25.9% | 10.6% |
| Deployment or release process | 9.3% | 7.8% |
| Environment, config or data difference | 9.3% | 7.2% |
| Requirements or spec gap | 8.3% | 7.2% |
| Regression from a recent change (impact analysis missed) | 7.4% | 16.1% |
| Legacy or unknown behavior | 7.4% | 2.2% |
| Test existed but was weak | 0% | 3.9% |

**What this tells us:** the main gap is **missing scenarios and race conditions**, not weak tests. More unit tests or a mutation gate alone will not close it.

**Actions, in order of impact:**

| # | Action | Closes | Gate | Evidence |
|---|---|---|---|---|
| 1 | **Escape-to-test:** every valid customer bug closes with a test that fails on the pre-fix code, or a reason | Missing scenarios (28%) | G8.2 | Only 38% of RCAs add a test today |
| 2 | **Race and ordering tests** for routing and contact lifecycle: design section in risky Epics, chaos and load stage before release | Races (26%) | G1.2, G5.3 | Races 26% in pilot vs 11% elsewhere |
| 3 | **Fix the E2E signal before it blocks:** triage the 13 failing routing scenarios; remove environment failures; quarantine flaky tests with an owner | Real failures hidden by noise | G4.5, G4.6 | Routing suite passed 1.2% of runs; its failures match real race bugs |
| 4 | **Tests with every hotspot change** (or an owner-approved reason) | Missing scenarios in risky code | G3.4 | Size x hotspot risk curve |
| 5 | **Spec link and acceptance criteria** on risky stories | Spec gaps (8%) | G1.1 | Causing stories link a spec 6.8% vs 31.8% |
| 6 | **Risk impact analysis aimed at bug fixes and hotspot changes** | Regressions (7-16%) | G1.3 | 1 in 4 known causes is a fix |
| 7 | **Correctness monitors in production** for what tests cannot reach | Environment, data, scale | G7.1 | 96% of P1 via customer cases |
| 8 | **Measure coverage of escapes, not lines:** link escape tests in Xray; score any new test tool on our past escapes | Proof that the gap closes | C-01 (D-043) | Xray links 18-25% today |

**AI for tests:** AI agents can write the escape tests and scenario tests. Accept a generated test only when it builds, passes reliably and fails on the pre-fix code (rule A6). Outside evidence (Meta) shows this filter is what makes generated tests useful.

**Limits:** escape causes come from RCA text, rated by a model, with no expert check yet. Pilot area only for the 108 cases.

Sources: `agg_r9_pilot_escape_profile`; [pilot RCA](../02-research/r9-pilot-orchestration-core.md), [escape-to-test](../04-solutions/so2-escape-to-test.md), [E2E trust](../04-solutions/so3a-e2e-trust.md), [gate catalog](../08-pod-quality/gate-catalog.md).
