# Product Quality Definition v1 (draft)

**Date:** 2026-10-25 | **Status:** draft for review; evidence columns are filled as mission v2 work completes | **Replaces:** interim definition D-006 (CFB count)

## Definition

Product quality = **the degree to which customers can run their contact-center business on the product correctly, without interruption, and without having to find our defects for us.**

Code quality, coverage and tool scores are **inputs** that may explain quality. They are not quality.

## Dimensions

| # | Dimension | Question it answers | Candidate evidence | Source | Limits |
|---|---|---|---|---|---|
| D1 | **Business correctness** | Does the product do the right thing with customer data and work (routing, contact state, reporting data, schedules, recordings, billing/usage)? | Valid customer-found defects classified as correctness failures; data-correction incidents | Jira CFB + failure-type taxonomy; ServiceNow | Only reported defects are visible; silent data errors are missed |
| D2 | **Availability and continuity** | Can customers use the product when they need it? | Major incidents, P1 incidents, outage duration, affected customers | ServiceNow incidents / MI | Monitoring-generated incidents must be separated from customer impact |
| D3 | **Performance** | Is it fast enough at real scale? | Performance-type defects, latency SLO breaches | Jira, SLO data (not yet accessed) | SLO data access unknown |
| D4 | **Detection** | Do we find problems before customers do? | Share of impact first detected by monitoring vs customer report; time to detect | ServiceNow contact type, alert records | Field quality unknown |
| D5 | **Recovery** | How fast do we restore service and correct data? | Time to restore (P1 / MI), time to fix valid CFB | ServiceNow, Jira | Resolve time is not restore time unless recorded |
| D6 | **Change safety** | Do our changes break things for customers? | Change failure rate (changes linked to incidents), regressions, hotfixes | ServiceNow change_request, Jira RCA "introduced by" | Linkage completeness |
| D7 | **Non-recurrence** | Do the same failures come back? | Repeat failure types per service; duplicates per incident | Jira, ServiceNow problem records | Duplicate handling differs by team |

## Reading rules

- **Outcome first:** D1, D2 and D4 are the primary view. D5-D7 explain them. Engineering signals (tests, review, CI, ownership) are explanatory variables, not quality scores.
- **Severity-weighted, not counted:** one major incident across many customers outweighs many minor defects. Every count is shown together with its impact weight.
- **Valid only:** invalid closures (duplicate, not a bug, ...) are a separate data-quality signal.
- **No thresholds yet:** targets are set only after baselines exist per dimension and per team type (mission v2, item 6).

## Open

The evidence columns depend on: M2-IMPACT (D2, D4, D5, D6), M2-CORRECTNESS (D1), M2-TEAMS (variation by team).
