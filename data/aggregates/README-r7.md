# R7 - AI label semantics (U-17)

Run date: 2026-10-22. Read-only Jira + Confluence. Aggregates and issue keys only.

## Method
1. Confluence CQL `text ~ "AGENTIC_AI_CODE"` (25 pages) + read 2 defining pages.
2. Jira count queries per label, type, created year.
3. CFB tally: 100 of 163 AI-labeled CFBs (labels, AI fields).
4. Changelog read: 7 AI-labeled CFBs (who/when label added vs created, work start, resolution).
5. Story adoption proxy: stories resolved per quarter with AI indicator.
6. Causal path test: 100 fixed CFBs created 2026, extract Jira keys from RCA "How was it introduced", check AI indicator on causing items.

AI indicator JQL: `labels in ("AGENTIC_AI_CODE","AGENTIC_AI_CODE_100",...,"AGENTIC_AI_CODE_50","AGENT_AI_CODE","mcp-auto-generated","UseAIAgent","ai-fix","AI-Assisted","copilot","claude-assisted-issue") OR cf[15229] = "Yes"`.

## Sources defining the label
| Page | ID | Says |
|---|---|---|
| AI Metrics Automation - GitHub -> Jira Workflow | 3915612323 | GitHub Action adds `AGENTIC_AI_CODE` to the ticket when Claude Code opens the PR for it; on merge replaces with `AGENTIC_AI_CODE_<pct>` (AI share of lines). Ticket = the work item the PR implements. |
| PgM Automations with AI | 4011230379 | Monthly "AI Usage" KPI audit: find Epics/Stories with AI clues (labels, cf[12620], cf[15264]) and set "Implemented by AI Agent" (cf[15229]) = Yes. |
| Jira AI Metrics Publisher Agent | 4042064838 | Stage 14 of SDLC orchestrator publishes AI metrics to Jira. |
| AI Metrics Reporter (AIMR) | 4036330198 | Claude Code hooks compute AI-authored lines from git. |

Jira AI fields: "Implemented by AI Agent" cf[15229]; "AI Model Used" cf[15264]; AI Metrics tab (PR URL, LOC by AI, coverage, reviewer, durations).

## Findings
- On a Bug, the AI label marks that the FIX (the bug's own PR) was made with AI. It does NOT mark the defect as caused by AI code. Confidence: High (definition page + 7/7 changelogs: label and "AI Model Used" set after bug creation, during or after fix).
- Labels are a KPI-driven adoption metric, also applied retroactively (587 issues created before 2025, incl. 2017 epics; 2/7 CFB labels added after resolution).
- No naming standard: 14 variants in CFB sample (e.g. `Agentic_AI_Code_100.`). 15/100 AI-labeled CFBs have cf[15229] = No.
- AI share of resolved stories: 0.2% (2025-Q1) -> 2.0% (2025-Q4) -> 10% (2026-Q1) -> 31% (2026-Q2) -> 23% (2026-Q3).
- Non-AI resolved stories also rose: 23,481 (2025-Q3) -> 33,147 (2026-Q3). Throughput surge is not only AI-labeled work.
- Causal path: Jira links (Defect "created by", "is caused by") on only 3% of CFBs. RCA text names a causing key in 31%. In a test (n=27 causing items resolved 2026), 33% carry AI indicator vs 22% base. Not significant; mixed types (epics, stories, bugs).

## Caveats
- Changelog sample small (7). Author shown as user may be a personal token used by a GitHub Action.
- AI indicator coverage depends on team adoption of the metrics workflow (under-labeling of AI work is likely in teams without it; over-labeling likely via KPI audit).
- Epics labeled if any child is AI; epic-level indicator is coarse.
