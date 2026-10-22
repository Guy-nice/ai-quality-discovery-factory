# R2b - Pilot candidates (Gate 3 input)

Run date: 2026-10-22. Read-only Jira. Aggregates only.

## JQL
- Base B: `issuetype = Bug and salesforceAssociatedTypes is not EMPTY`
- W_prev: `created >= "2024-10-22" and created < "2025-10-22"`. W_last: `created >= "2025-10-22"`.
- VP: `"R&D VP[Dropdown]" = "<value>"`. Team: `"Team Name[Dropdown]" = "<value>"`. Severity: `priority in (P1, P2)`.
- Stuck/lost theme: `B and (labels in (stuck_contact, LostStuckContacts, LostStuckAgentContacts) or summary ~ "\"stuck contact\"" or summary ~ "\"lost contact\"" or summary ~ "\"stuck contacts\"" or summary ~ "\"stuck agent\"")`. All time 245 (labels 173, summary 175, both 103).
- Routing theme: `B and (labels in (wrong_routing, Race_conditions, Resilience_26) or summary ~ "routing")`.

## Method
- Paged all CFBs of 3 VPs (Orchestration Core, A&D, WFM), 2024-10-22 to 2026-10-22. W_last complete (1,050 = exact VP totals). W_prev sample 549 of 605 (last page, 2024-10-22 to 2024-12-12, not saved).
- Exact W_prev counts by JQL for top teams. Other W_prev team values = sample (marked).
- Score: 1-5 per criterion. Weights: density 3, criticality (P1/P2 share + incident load) 3, growth 2, boundary crossing 2. Max 50.

## Caveats
- `customfield_10068` (Number of Incidents) completeness unknown. Routing theme incident load not measured.
- Team renames / new team names (Agni, Titans, Nexus, ACD Admin Bolivia -> Pune) inflate team growth. Team growth is not quality change by itself.
- Text theme uses summary only. `text ~` times out.
- Invalid-CFB share per VP not removed.
- Label top list covers the 3 VPs only (60% of W_last), not all CFBs.
- Weights are a judgment. Sensitivity: without boundary weight, Orchestration Core stays rank 1 (35 vs A&D 33).
