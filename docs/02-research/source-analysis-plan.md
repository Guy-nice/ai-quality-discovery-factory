# Source Analysis Plan

**Version:** v0 | **Date:** 2026-10-22

Per-source plan: what to extract, how, and known pitfalls. All access is read-only. Queries and exact filters are recorded here when run.

## SRC-001 Jira

- **Extract:** bugs / CFBs / MIs per month (24 mo); severity; component; found-in environment / phase; reopen count; time to resolve; links to Epics / changes.
- **Method:** JQL counts by month and component. Field completeness check per field.
- **Pitfalls:** classification changes over time; duplicate tickets; components not mapped to code.
- **Query log:** none yet.

## SRC-002 Confluence

- **Extract:** RCAs / postmortems (root-cause category, component, detection gap); architecture docs and ADRs (boundaries, age); QA strategy.
- **Method:** CQL search by label / title; sample and code RCAs into categories.
- **Pitfalls:** stale docs; RCAs inconsistent in depth.

## SRC-003 Xray

- **Extract:** tests per requirement; manual vs automated ratio; execution history; untested requirements.
- **Pitfalls:** traceability links may be incomplete; executed is not the same as effective.

## SRC-004 Git

- **Extract:** churn per file / module; author concentration; PR size, review time, comment count; reverts and hotfixes; defect-linked commits (via ticket keys in messages).
- **Pitfalls:** squash merges hide history; ticket key usage inconsistent; bots inflate counts.

## SRC-005 Sonar

- **Extract:** trend of coverage, complexity, duplication, reliability issues per module.
- **Pitfalls:** rule set changes break trends; coverage is not test effectiveness.

## SRC-006 CI/CD

- **Extract:** build failure rate; reruns; flaky / quarantined / skipped tests; pipeline duration; deploy and rollback frequency.
- **Pitfalls:** retention limits; reruns not logged.

## SRC-007 Power BI / SRC-008 Incidents / SRC-009 Observability

- **Extract:** existing CFB, OLA, regression metrics with definitions; MIs linked to changes; time to restore; SLO breaches near releases.
- **Pitfalls:** metric definitions undocumented; incident-to-change linkage missing.

## SRC-010 AI usage

- **Extract:** tool, team, adoption date, usage intensity.
- **Method options:** license / telemetry data; PR labels or commit trailers; developer survey (self-report, lower confidence).
- **Pitfalls:** no reliable per-change attribution; adoption confounded with other changes.

## SRC-011 SME interviews

- **Extract:** hidden business rules, fragile areas, historical decisions, single points of failure.
- **Method:** semi-structured, 30-45 min, same core questions per SME; findings cross-checked with data.
- **Pitfalls:** recall bias; strong opinions recorded as HYPOTHESIS, not FACT.
