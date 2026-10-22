# Evidence and Access Inventory

**Version:** v0 | **Date:** 2026-10-22 | **Gate 1:** OPEN

Access status is from the research environment (Claude Code session). "Connector available" means a tool exists. It does not mean permissions or data are confirmed.

## 1. Sources

| SRC ID | Source | Evidence wanted | Access status | Permissions | Known limits | Next action |
|---|---|---|---|---|---|---|
| SRC-001 | Jira | Bugs, CFBs, MIs per month (24 mo), severity, component, found-in phase, reopen, links | **Available** (Atlassian MCP, read). Verified 2026-10-22. | Read across CXone projects | Component 88% empty, Bug Type 48% empty; text-search on custom fields times out; no regression field; useful fields: R&D VP (cf_14852), Team Name (cf_10098), Root Cause Analysis (cf_10117), Regression Impact Analysis (cf_12794), Number of Incidents (cf_10068), Impact Rank (cf_10081), EOR fields | In use |
| SRC-002 | Confluence | Architecture, ADRs, RCAs/postmortems, QA strategy, XCX process, runbooks | **Available** (Atlassian MCP, read). Verified 2026-10-22 on CX space. | Read | Staleness UNKNOWN | List RCA / architecture pages for pilot |
| SRC-003 | Xray | Test cases, executions, requirement coverage, manual vs automated | UNKNOWN (likely via Jira) | UNKNOWN | Xray API may need separate token | Confirm with Jira admin |
| SRC-004 | Git (org repos) | Churn, hotspots, ownership, PR size, review, reverts | gh CLI works for personal account. Org repos UNKNOWN. | UNKNOWN | Monolith repo location UNKNOWN; history depth UNKNOWN | Get repo list (Q1) |
| SRC-005 | Sonar | Coverage, complexity, duplication, reliability trends | No connector | UNKNOWN | Trend retention UNKNOWN | Ask DevOps for URL + read token |
| SRC-006 | CI/CD | Failure rate, flaky / skipped tests, reruns, duration, deploys, rollbacks | No connector. System UNKNOWN. | UNKNOWN | - | Ask which system |
| SRC-007 | Power BI | CFB, OLA, regression dashboards | Connector present, needs auth | UNKNOWN | Metric definitions UNKNOWN | Authenticate; get dashboard list (Q6) |
| SRC-008 | Incident / ITSM | MIs, change-linked incidents, time to restore | ServiceNow connectors present, need auth. Which instance is relevant: UNKNOWN. | UNKNOWN | - | Confirm system of record |
| SRC-009 | Observability | Error rates, latency, SLOs, release impact | UNKNOWN | UNKNOWN | - | Ask SRE |
| SRC-010 | AI usage data | Tools, teams, adoption dates, telemetry | UNKNOWN | UNKNOWN | Attribution may be impossible from Git alone | Q7 |
| SRC-011 | SME interviews | Hidden rules, dependencies, history | Requires scheduling | n/a | Subjective; needs cross-check | Q8 |
| SRC-012 | QA Architect role page (Confluence) | Local process terms (CFB, MI, OLA, XCX, RIA/PIA) | Referenced in personal notes. Not re-read for this initiative. | Known to Guy | Role page, not process definition | Use for glossary only |
| SRC-013 | WIP Quality Definition of Done (Confluence CX 4048715783) | Proposed gates, controls inventory | Read 2026-10-22 | Read | WIP, solution-stage | [Review](source-review-quality-dod-wip.md) |
| SRC-014 | Salesforce-to-Jira connector | CFB definition basis (`salesforceAssociatedTypes`) | Indirect via Jira | - | Linking practice changes would distort trend | Confirm with Support Ops |

## 2. Data handling

Rule for what may be stored in this repository: UNKNOWN (U-04). Until confirmed:

- Store aggregates and counts, not raw ticket content.
- No customer names, PII, credentials, or code excerpts from proprietary repos.
- Jira / Confluence references by key or ID only.

## 3. Gate 1 checklist

| Item | Status |
|---|---|
| Each source marked available / partial / none | Partial (draft) |
| Permissions confirmed | Open |
| Data limits documented | Open |
| Missing systems listed with alternatives | Open |
