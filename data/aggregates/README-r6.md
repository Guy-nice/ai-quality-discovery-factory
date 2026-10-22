# R6 - Controls Inventory - Method

**Run date:** 2026-10-22 | **Access:** read-only Atlassian MCP | **Files:** `r6-controls.csv`, `r6-ria-regression.csv`

## Scope

- Jira quality fields on Epic, Story, Bug, CFB.
- RIA on the changes that caused regression CFBs.
- Xray usage.
- Confluence pages: gates, go/no-go, Sonar, mutation, XCX.

## Method

| Item | Method |
|---|---|
| Field discovery | `getJiraIssue` with `expand=names` on 1 recent Story (CXDV) + earlier CFB (DAT). Field IDs in CSV. |
| Count fill rate | JQL `cf[ID] is not EMPTY` (or `= Yes`), resolved in 2026 to 2026-10-22. Exact counts. |
| Text fill rate (RIA, RCA, EOR, AC) | Text search on custom fields times out. Sample 40 items per type. Template = all template prompt strings still present. Partial = some removed. Filled = none present. |
| Epic sample | `issuetype = Epic and resolved >= 2026-06-01 and resolution = Done and project in (CXDV, ORC, AAD, DAT, PMSTND, CXWFM)`, newest 40 |
| Story sample | Same projects, Story, resolved >= 2026-09-01, newest 40 |
| CFB sample | CFB, resolution = Fixed, resolved >= 2026-06-01, newest 40 |
| RIA vs regression | First 20 rows with `regression = yes` and `introduced_by = specific recent change` from `rca-classification.csv`. Causing key from RCA "How was it introduced?" text. Causing item RIA classified as above. |
| Confluence | CQL title search: quality gate, definition of done, go/no-go, XCX, mutation, sonar quality, RIA |

## Template prompt strings used

- RIA: "Describe functionality or issue to be fixed", "Identify specific components, files", "Identify and document specific tests".
- EOR Broken?: "What alerts will notify the team?", "Necessary logging added?", "Above allows for prompt notification".
- EOR Mitigation?: "Turn Off Feature Toggle?", "Functionality retested after rollback?", "Above allows for quickly remediating".

## Limitations

- Samples are not random. Newest items only, 6 projects.
- "Partial" RIA may still hold no real analysis.
- Workflow enforcement is not visible in the API. All "enforced" labels are UNKNOWN unless a page states blocking.
- Field value "set" does not mean the review happened. It means someone selected a value.
- Epic count (23,988 resolved in 2026) looks high. Epic usage may differ by project.
- `Implemented by AI Agent` is a team-set field. Meaning on Bugs is assumed to be "fix implemented by AI". Not verified with field owner.
- Out-of-scope note: one sampled Story description holds tenant credentials and API keys in plain text. Key is in session notes only. Report to Security.
