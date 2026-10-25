> **Correction 2026-10-25 (D-032):** without MI-investigation tickets, H1 2026 vs H1 2025 is CFB **+29%**, P1/P2 **+46%** (not +51% / +72%). ServiceNow P1 incidents fell in 2026 (C-08). See [mission v2 findings](../06-reassessment/m2-findings-round-1.md).

# Research Findings - Round 1

**Date:** 2026-10-22 | **Sources:** SRC-001 Jira (read-only), SRC-013 Confluence | **Data:** [`data/aggregates/`](../../data/aggregates/)

Population: customer-found bugs (CFB) = `issuetype = Bug and salesforceAssociatedTypes is not EMPTY` (11,662 issues, 2017-05 to 2026-10). Definition provided by initiative lead.

## F1 - Trend: has quality declined? (R1)

| Metric | 2025-H1 | 2026-H1 | Change |
|---|---|---|---|
| CFB created | 574 | 864 | +51% |
| CFB P1/P2 | 296 | 509 | +72% |

| Metric | 2025-Q3 | 2026-Q3 | Change |
|---|---|---|---|
| CFB created | 383 | 468 | +22% |
| CFB P1/P2 | 167 | 316 | +89% |
| P1/P2 share | 44% | 68% | +24 pt |
| Stories resolved | 23,573 | 42,960 | +82% |
| CFB per 100 stories | 1.62 | 1.09 | -33% |

- **EVIDENCE (High):** 2021-2025 CFB volume was flat (1.24k-1.45k per year). 2026 reached 1,428 by Oct 22, so it already passes every earlier full year.
- **EVIDENCE (High):** Severity mix is worse. P1/P2 share was about 50% in 2023-2024 and is 63-68% in 2026-Q2/Q3.
- **EVIDENCE (Medium):** CFBs per resolved story fell because story throughput grew 2.4× (2024-Q3 to 2026-Q3).
- **CONTRADICTION C-01:** Customer-felt defect load and severity went up. Defects per unit of delivery went down. Both are true. Which one is "quality" depends on the definition (U-05).
- **No migration artifact:** CFB counts were 394 in the 3 months before the 2022-11-25 Jira migration and 367 in the 3 months after.

Confounders not resolved yet:
- U-13: step jumps in stories resolved and all bugs (2024-Q1, 2026-Q3). Possible causes: new projects, bulk or tool-created issues, AI-generated tickets.
- U-14: invalid CFBs (Cannot Reproduce / Not a Bug / Won't Do / Duplicate) are 30-36% of CFBs. That share varied from 20% to 44% over time.
- Triage lag: recent quarters still have open CFBs, so their invalid share is understated.
- No customer-base or usage normalization yet (U-15).

## F2 - Concentration: where is the risk? (R2)

Windows: W_prev = 2024-10-22 to 2025-10-21, W_last = 2025-10-22 to 2026-10-22. Total CFBs went from 1,318 to 1,760 (+34%).

| R&D VP | W_prev | W_last | Change | Share W_last |
|---|---|---|---|---|
| Analytics and Data | 306 | 473 | +55% | 27% |
| Orchestration Core | 170 | 296 | +74% | 17% |
| WFM | 129 | 281 | +118% | 16% |
| AHW | 251 | 250 | 0% | 14% |
| LiveVox & Digital | 205 | 138 | -33% | 8% |
| APQ | 106 | 120 | +13% | 7% |
| VMS, Recording, QM & FM | 47 | 99 | +111% | 6% |
| (empty) | 93 | 101 | +9% | 6% |

- **EVIDENCE (High):** The top 3 VPs (A&D, Orchestration Core, WFM) produce 60% of CFBs, and nearly all of the growth comes from them plus VMS.
- **EVIDENCE (Medium):** Teams are spread wide: 185 teams, and the top 5 hold 19% of CFBs. So concentration shows at domain level, not at team level.
- **EVIDENCE (Medium):** 229 of 1,545 sampled W_last CFBs (15%) have 5 or more linked incidents.
- **HYPOTHESIS H-13:** A cross-domain "stuck / lost contacts" defect theme exists (labels `stuck_contact` 61, `LostStuckContacts` 51, `LostStuckAgentContacts` 11). It spans data, orchestration and digital. It may be a legacy-modern boundary cluster.
- **CONTRADICTION C-02:** Some project-level shifts look like re-homing, not quality change. AW and DE fell by about 150 while CXDV and CSA rose by about 160. Use VP / team, not project, until projects are mapped (U-16).

## F3 - Escape causes: why do defects reach customers? (R5)

Sample: 240 fixed CFBs from W_last. 213 have a usable RCA. Single rater. The sample does not cover 2026-01 to 2026-06. See [README-rca](../../data/aggregates/README-rca.md).

| Escape cause | % (n=213) |
|---|---|
| Missing test coverage (scenario never tested) | 27.7 |
| Regression from recent change (RIA miss) | 15.0 |
| Scale / performance / concurrency / race | 13.1 |
| Unclear / not stated | 9.4 |
| Deployment / release process | 7.0 |
| Environment / config / data difference | 7.0 |
| Requirements / spec gap | 6.6 |
| Third-party / integration | 5.2 |
| Legacy / unknown behavior | 3.8 |
| Test existed but ineffective | 3.3 |
| Monitoring gap | 1.9 |

- **EVIDENCE (Medium):** Test gaps are the largest class: 31% (missing coverage plus ineffective tests).
- **EVIDENCE (Medium):** 39% of escapes come from a specific recent change and 35% from long-standing latent code. Of the recent-change escapes, 32 (15% of all) are RIA misses: shared code paths, other consumers, copy-pasted logic, fixes not ported across versions.
- **EVIDENCE (Medium):** About 20% are scale, race or environment gaps that lower environments cannot show (small tenants, single region, data shape).
- **EVIDENCE (Medium):** Only 1.9% of prevention actions add monitoring or alerts. 15% state no prevention action.
- **HYPOTHESIS (Low):** Legacy is a smaller direct cause than perceived: 3.8% primary cause, 11% mention it. Self-reported RCAs may under-report it.
- **Domain differences:** Orchestration Core has the most scale/race escapes (9 of 33). A&D has the most third-party and deployment escapes (13 of 41). WFM RCAs are often unclear (10 of 34), which points to weak RCA practice there.

## F4 - AI-assisted development (R7)

- **EVIDENCE (High):** AI-code labels on CFBs went from 1 (W_prev) to 159 (W_last, 9%). There are 11 label variants and no standard (`AGENTIC_AI_CODE`, `AGENT_AI_CODE`, `AI-Assisted`, `copilot`, `claude-assisted-issue`, ...).
- **UNKNOWN U-17:** What the labels mean. They could mark the bug as caused by AI code, or the fix as made with AI. Without that, no attribution is possible.
- **EVIDENCE (Medium):** 0 of 213 RCAs name AI-generated code as a cause. The RCA template asks no AI question, so this is **not** evidence of no effect.
- **EVIDENCE (Low, n=2):** In one RCA an AI PR reviewer flagged a missing test and nobody acted on it. In another, an AI reviewer missed the gap.
- **Conclusion:** With the current data we cannot test whether AI-assisted development causes the decline. The timing matches: CFB growth and the throughput surge are both in 2026. A timing match is not a cause.

## F5 - Data quality of the quality data

| Field (W_last CFBs) | Empty |
|---|---|
| Component | 88% |
| Bug Type | 48% |
| R&D VP | 6% |
| Team Name | 2% |
| RCA (fixed CFBs) | 11% template-only, empty or N/A |

- **EVIDENCE (High):** Root-cause analysis by component or bug type is not possible. VP and Team are usable.
- No dedicated regression field. Regression is marked by inconsistent labels in about 6 issues per sample.

## What could invalidate these findings

- Changes in Salesforce-to-Jira linking practice: the CFB definition depends on the connector.
- A growth in customers or usage that explains the absolute rise.
- The invalid-CFB share and triage lag changing the 2026 numbers once triage finishes.
- Rater bias in the RCA classification. A second rater on a subset is needed (R5b).
