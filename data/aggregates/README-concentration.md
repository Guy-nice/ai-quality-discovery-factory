# CFB Concentration - Aggregates

**Run date:** 2026-10-22 | **Source:** Jira (SRC-001), read-only, Atlassian MCP | **Data:** aggregates only, no ticket content

## Definitions

- **CFB (working definition):** `issuetype = Bug and salesforceAssociatedTypes is not EMPTY` (bug linked to a Salesforce customer case). To confirm with QA leadership.
- **W_prev:** `created >= "2024-10-22" and created < "2025-10-22"`
- **W_last:** `created >= "2025-10-22" and created < "2026-10-23"`

## Exact JQL patterns (counts, `searchResultMode=count`)

```
<B> = issuetype = Bug and salesforceAssociatedTypes is not EMPTY
<B> and <W> and "R&D VP[Dropdown]" = "<value>"      (and: is EMPTY)
<B> and <W> and project = <KEY>
<B> and <W> and "Team Name[Dropdown]" = "<value>"   (and: is EMPTY)
<B> and <W> and "Bug Type[Dropdown]" is EMPTY
<B> and <W> and component is EMPTY
<B> and <W> and labels in (AGENTIC_AI_CODE, AGENTIC_AI_CODE_100, AGENT_AI_CODE, AI-Assisted,
    Agentic_AI_Code_100., UseAIAgent, Agentic_AI_Code, ai-assisted, AI-used, copilot, claude-assisted-issue)
```

## Full vs sample

| Item | Basis |
|---|---|
| Totals, R&D VP, top-10 project, top-5 team, AI-label group, empty-field counts | **Exact** (JQL count) |
| Value discovery, team ranking, Bug Type values, Number of Incidents buckets, label inventory | **Sample**: 1,576 of 1,760 W_last CFBs (89.5%). 184 issues from 6 monthly page-2 results not captured to file. |

Team top-5 is ranked from the sample. A team outside the sample top-5 can have a higher exact count.

## Field completeness (W_last, exact, n = 1,760)

| Field | Empty | % empty |
|---|---|---|
| Component | 1,546 | 87.8 |
| Bug Type | 845 | 48.0 |
| R&D VP | 101 | 5.7 |
| Team Name | 30 | 1.7 |

## Sample-only distributions (n = 1,576)

| Number of Incidents | Count | % |
|---|---|---|
| 0 | 96 | 6.1 |
| 1 | 898 | 57.0 |
| 2-4 | 322 | 20.4 |
| 5+ | 229 | 14.5 |
| null | 31 | 2.0 |

Bug Type values (sample): Functional 800, UI 8, Performance 6, Security 2, empty 760.

## Caveats

1. Project counts are confounded by possible project moves (e.g. AW down 43%, CXDV up 53%). Do not read project trends as quality trends until mapping is checked.
2. AI labels: practice started inside W_last (1 in W_prev, 159 in W_last). Meaning is UNKNOWN: label may mark the bug **fix** as AI-made, not the **cause**. 11+ spelling variants, no single standard.
3. "Regression" labels: about 6 issues in sample. No dedicated regression field found in the fields pulled.
4. CFB volume is not normalized by customer count, release count, or change volume.
