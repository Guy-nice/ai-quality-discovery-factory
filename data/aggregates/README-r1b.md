# R1b - Throughput jump causes (U-13)

Run: 2026-10-22. Read-only Jira (Atlassian MCP). Aggregates only.

## Method
- Monthly, then weekly / 10-day counts to locate spikes.
- Samples of 100 issues per spike window (fields: project, reporter, labels, created). Tallied locally. Raw files deleted.
- Exact counts per suspect project / label.

## JQL templates
- Bugs: `issuetype = Bug and created >= "<d1>" and created < "<d2>" [and project = <KEY>] [and labels = ado-bug]`
- Stories: `issuetype = Story and resolved >= "<d1>" and resolved < "<d2>" [and project = <KEY> | != CGY]`
- AI labels (stories): `labels in (AGENTIC_AI_CODE, AGENTIC_AI_CODE_100, AGENT_AI_CODE, AI-Assisted, ai-metrics-updated)`
- AI / auto / CI labels (bugs): `labels in (AGENTIC_AI_CODE, AGENTIC_AI_CODE_100, AGENT_AI_CODE, AI-Assisted, mcp-auto-generated, Automation_Generated, CICD_FAIL_BUG, SprintFaliure)`
- CFB: `issuetype = Bug and salesforceAssociatedTypes is not EMPTY and project = CGY` = 0.

## Spike locations (bugs)
- 2024-01-01..07: 5013 bugs (normal week ~400-450). ENG = 4738. Sample: 87% ENG on 2024-01-06, 24 reporters.
- 2026-07-11..20: 6328 bugs. Sample: 66% CGY, label `ado-bug`, 2026-07-13.

## Caveats
- Reporter = human for >=94% of samples. Bulk import keeps human reporters; bot share is not a usable signal.
- Default JQL order clusters by project; samples used ORDER BY created/resolved to reduce bias. Still not random.
- CGY stories before 2026-Q2 assumed 0 (CGY bugs before 2026-Q2 = 0; stories 2026-Q2 = 6).
- Residual 2026-Q3 bug growth (non-CGY, non-AI/auto label): 9284 vs 5866 in 2025-Q3 (+58%). Not explained by one project.
- "Story" size not measured. AI-labeled stories may be smaller units.
