# M2 Impact - ServiceNow (E1-E3, E7)

**Date:** 2026-10-25 | **Source:** ServiceNow CXone Prod, aggregate API only | **Data:** DB `sn_aggregates`, `agg_m2_impact`; raw counts `data/raw/servicenow/` (gitignored) | **No solution design.**

## 1. Access and data model

- **FACT:** This account can read **aggregate counts** only. Record reads on `incident`, `problem` and `change_request` return empty lists. Grouping by `business_service` / `cmdb_ci` is denied. The `problem` table is denied.
- **FACT:** `contact_type` shows the intake channel: `bmc_truesight` (monitoring events, 1.40M since 2025), `salesforce` (incident from a customer support case, 6,523), `email` (8,260), `Rapid7 IDR` (security, 5,732).
- **FACT:** `major_incident_state` is almost unused (27 "proposed" since 2025). Major incidents are not tracked in this field.
- **UNKNOWN:** The fields that hold Jira keys, Salesforce case IDs, outage minutes, or the customer. Field discovery needs record read.

## 2. P1 incidents (2025-01 to 2026-10, n = 887)

| Measure | Value | Class |
|---|---|---|
| Intake channel | Salesforce (customer case) 852 (96%); email 32; security 2; monitoring 0 | EVIDENCE (High) |
| Assigned to | Service Operations NOC 759 (86%), Voice Ops 67, InfoSec CSOC 34, Network Ops 10 | EVIDENCE (High) |
| Time open to resolve | < 4 h 602 (71%); 4-24 h 145 (17%); > 24 h 97 (12%) | EVIDENCE (Medium: resolve time, not restore time) |
| Linked to a problem record | 597 (67%) | EVIDENCE |
| Linked to a causing change (`caused_by`) | 5 (0.6%) | EVIDENCE: the link is almost never used |
| Company (customer) filled | 146 (16%) | EVIDENCE: "who was affected" is not in ServiceNow |

**HYPOTHESIS (Medium):** P1 incidents start from a customer case, not from monitoring. This supports PH-5 ("customers detect first"). Limit: the channel shows how the incident record was opened, not who saw the problem first. NOC may open a Salesforce case after an alert.

## 3. Trend: customer-channel incidents by quarter

| Quarter | P1 | P2 | All priorities |
|---|---|---|---|
| 2025-Q1 | 113 | 237 | 687 |
| 2025-Q2 | 157 | 305 | 832 |
| 2025-Q3 | 163 | 333 | 899 |
| 2025-Q4 | 170 | 379 | 1,084 |
| 2026-Q1 | 68 | 336 | 905 |
| 2026-Q2 | 74 | 311 | 923 |
| 2026-Q3 | 85 | 254 | 933 |

- **EVIDENCE (High):** P1 incidents fell by half from 2025-Q4 to 2026-Q1 (170 -> 68) and stayed low. Total customer-channel incidents stayed flat at about 900 per quarter in 2026.
- **CONTRADICTION C-08:** Jira customer-found bugs: P1/P2 +72% (H1 2026 vs H1 2025). ServiceNow P1 incidents: about -55% in the same period. Possible explanations: (a) a change in incident priority rules on 2026-01-01 (the step is sharp and at a year boundary), (b) fewer outages but more functional defects, (c) the two systems count different things (incident = service event; CFB = defect). **Not resolved.**

## 4. Change failure signals

| Period | Emergency changes | Emergency share (of normal + emergency) | Normal changes failed | Normal "success with issues" |
|---|---|---|---|---|
| 2025-H1 | 543 | 6.8% | 3.9% | 3.4% |
| 2025-H2 | 806 | 10.5% | 4.5% | 4.8% |
| 2026-H1 | 854 | 9.5% | 3.4% | 4.7% |
| 2026-Jul..Oct (4 mo) | 1,269 | 14.4% | 2.6% | 3.9% |

- **EVIDENCE (High):** Emergency changes rose from about 90 per month (2025-H1) to about 330 per month (2026-Jul..Oct). Their share doubled (6.8% -> 14.4%).
- **EVIDENCE (Medium):** The failure rate of normal changes is flat or falling (3.9% -> 2.6%). Limit: 2026-Jul..Oct has 2,343 changes without a close code yet.
- **HYPOTHESIS (Medium):** More work goes through the emergency path: urgent fixes and bypass of normal review. This is consistent with a reactive delivery mode, but the change purpose cannot be read.

## 5. Cross-check of RCA causes (Q-D, data validation)

**Not possible.** The `problem` table is denied, and incidents cannot be linked to Jira. The RCA classification has no independent check from ServiceNow.

## 6. Limits

- Aggregates only: no per-incident view, no customer, no service, no R&D team, no Jira link.
- "Time to resolve" is the time from open to resolve. It is not time to detect or time to restore.
- P2 total (1.11M) and P3 are mostly monitoring events. They are not customer impact.

## 7. Access needed to close E1-E3

Read role on `incident` (fields: number, opened_at, resolved_at, priority, contact_type, business_service, cmdb_ci, company, problem_id, caused_by, custom Jira / Salesforce / outage fields), `problem`, `change_request`, and the `business_service` reference. Usually this is the `itil` role or a read-only reporting role.
