# Mission v2 - Findings Round 1

**Date:** 2026-10-25 | **Detail:** [impact](m2-impact-servicenow.md), [failure types](m2-failure-types.md), [teams](m2-teams.md) | **Quality definition:** [v1 draft](quality-definition-v1-draft.md)

Lead asked research to answer Q-B, Q-C, Q-D from data (D-031).

## C-09 Correction: the 2026 rise was overstated

In 2026, major-incident (MI) investigation tickets started to be created as Jira bugs with a Salesforce link: 3 in H1 2025, 128 in H1 2026. They are a process change, not new product defects.

| H1 2026 vs H1 2025 | Reported before | Without MI-investigation tickets |
|---|---|---|
| All CFBs | +51% | **+29%** (571 -> 736) |
| P1/P2 CFBs | +72% | **+46%** (293 -> 427) |
| Valid CFBs | +41% | **+28%** (313 -> 400) |
| Valid P1/P2 CFBs | +63% | **+43%** (165 -> 236) |

- **EVIDENCE (High):** Customer-reported defects still rose in 2026, and severity rose more than volume.
- **CONTRADICTION C-08 (open):** ServiceNow P1 incidents from the customer-case channel fell by about half in 2026 (about 150 -> 76 per quarter), with the drop at 2026-Q1. A priority-rule change is possible. So the **incident** view does not confirm the decline.
- **Status:** "quality declined" is now **Medium** confidence (was Medium-High). It holds for customer-reported defects; it is not confirmed for incidents.

## F17 - Who detects (D4, PH-5)

- **EVIDENCE (Medium):** 852 of 887 P1 incidents since 2025 (96%) were opened through the Salesforce customer-case channel. Monitoring opened 0. This shows the intake channel, not the first observer.
- **EVIDENCE (High):** `caused_by` change link on 0.6% of P1s; problem link on 67%.
- **Limit:** current ServiceNow role reads counts only. No record-level data, no service or CI grouping, no problem table.

## F18 - Change safety (D6)

- **EVIDENCE (Medium):** Emergency changes rose from about 90 to about 330 per month (6.8% -> 14.4% of normal + emergency changes). Normal-change failure rate stayed flat to lower (3.9% -> 2.6%).
- **HYPOTHESIS (Low):** more emergency changes reflect more urgent fixes in 2026. Not linked to incidents yet (access).

## F19 - What fails: business correctness (D1, Q-B)

1,565 valid CFBs (2025-01..2026-10), 13 failure types; manual correction of 769 labels; precision 93-95% on 40 checks (single AI rater).

| Rank | Correctness type | Evidence | Trend |
|---|---|---|---|
| 1 | **DATA:** wrong or stale report and dashboard data | 399 CFBs; 66% P1/P2; highest total impact | wrong metric values 26 -> 50 |
| 2 | **ROUTING:** wrong routing | 73% P1/P2 (highest); 20% with 5+ incidents | +39% |
| 3 | **LIFECYCLE:** stuck / lost / dropped contacts, dead air | | +92% (24 -> 46) |
| 4 | **RECQM:** recording, QM and AI-output errors | | +40% |
| 5 | **AGENTSTATE:** wrong agent state | 18 CFBs, 11 incidents per CFB | - |

- **EVIDENCE (Medium):** Correctness failures are 46% of valid CFBs, more severe (62.5% vs 55.1% P1/P2) and slower to fix (12 vs 8 days median) than other types.
- **Answer Q-B:** data/reporting correctness, routing correctness and contact lifecycle hurt customers most.
- **Analytics and Data (E4):** valid CFBs +23%; 59% correctness; report/dashboard failures 43 -> 70; wrong metric values 5.8 incidents per CFB.
- **Blind spot:** billing has only 4 CFBs. Customers rarely report billing errors as bugs, so this type is likely under-seen.

## F20 - Teams and PODs (E5, Q-C)

- **EVIDENCE (High):** No org-wide map of team -> service -> code exists. Best current key: Jira "Team Name" (98% filled), but teams were renamed and split. GitHub has 295 teams (14 of 40 Jira teams match by name). ServiceNow groups are operations groups (NOC holds 759 of 887 P1s).
- **Answer Q-C:** Jira "Team Name" is the best available source of truth today. A maintained team -> service -> repo map does not exist.
- **EVIDENCE (Medium):** Outcomes vary strongly between teams (40 teams with >= 10 valid CFBs):

| Measure | Range across teams | Share of variation explained by VP |
|---|---|---|
| Incidents per CFB | 1.1 - 10.4 | 17% |
| P1/P2 share | 10 - 93% | 46% |
| Invalid share | 6 - 79% | - |
| Days to fix | 3 - 31 | - |
| AI share of fixes | 0 - 64% | - |
| RCA filled | 80 - 100% | uniform |

- **Archetypes (descriptive):** high impact (9 teams), fast growing (8, partly re-homed), high intake noise (5), stable (18).
- **Implication (evidence only):** impact, severity and intake noise are team-specific. RCA practice is already uniform. AI comparisons must control for team.

## Q-D - Validation without SMEs

Data-only triangulation was planned (Jira RCA vs ServiceNow problem records). It is **blocked**: the problem table is denied. Human or record-level validation stays open.

## Evidence gaps after round 1

| Gap | Status |
|---|---|
| E1-E3 impact, who affected, detection | Partly (counts). Needs a ServiceNow read role on incident, problem, change_request. |
| E4 correctness | Answered (F19) |
| E5 team variation | Answered for outcomes; practices only for 17 teams |
| E6 validation | Blocked (no SME, no problem records) |
| E7 delivery | Partly (emergency changes) |
| E8 requirements | Open |
| E9 AI causal | Open |
