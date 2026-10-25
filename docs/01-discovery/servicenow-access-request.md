# ServiceNow Access Request (U-26)

**Date:** 2026-10-25 | **Form:** ServiceNow service portal, catalog item "Request access to ServiceNow" | **Submitted by:** Guy Guterman (manual; the connector is read-only)

## Access needed: read-only

| Table | Why |
|---|---|
| `incident` (incl. Major Incident fields) | Who was affected, time to restore, which service, detection source |
| `problem` | Root causes; cross-check with Jira RCAs |
| `change_request` | Changes that caused incidents; emergency-change follow-up |
| `task_sla` | SLA breaches (customer impact) |
| `cmdb_ci_service` / `cmdb_ci` | Map incidents to services and teams |
| `sys_user_group` | Map assignment groups to dev teams |

Role: read-only (`snc_read_only` + read scope of `itil`, or a reporting role). Window: 2025-01 to now. Duration: 12 months.

## Business justification

I am the QA Architect for the CXone product-quality investigation. I need read-only access to incident, problem, change_request, task_sla and CMDB service records, from 2025-01 to now. The goal: measure customer impact, detection and time to restore, and link incidents to the changes that caused them. I need no write access. Data is used only in aggregate, inside NICE.

## After approval

Read-only test -> gap-only pull (D-033) -> closes U-26, C-08, X2 detection baseline.

## Status

- 2026-10-25: submitted via service portal as **REQ0120210** (Request Access to ServiceNow; Standard Production; purpose "To view Change Requests/Ticket data only"; assignment group left empty with a request to advise). Stage: Waiting for Approval (manager).
