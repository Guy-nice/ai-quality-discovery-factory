# Hotspot PR Rules - Draft Spec (SO-5)

**Status:** DRAFT, not applied | **Date:** 2026-10-22 | **Evidence:** [so4-so5](../so4-so5-owners-pr-rules.md)

The rules apply to **every** PR that touches a hotspot path, AI or human. Risk depends on size x hotspot, not on who writes the code.

## 1. Hotspot paths

| Repo | Paths |
|---|---|
| inContact/inContact | `Code/C#/Services/VCSvc/Providers/{ACD,Data,Agent}/**`, `Code/C#/Library/AgentHelper/**`, `Code/C#/Library/inContact.InterVCCommWrapper/**`, `Database/InDB_DACPAC/inCode/dbo/StoredProcedures/**` |
| routing-ng-advanced-findmatch | `src/main/java/com/nice/routing/afm/service/**` |
| routing-ng-agent-capacity-service | `src/main/java/com/nice/routing/agentcapacityservice/client/**` |

The path list is reviewed each quarter from the hotspot query (`scripts/db/r3_hotspots.py`).

## 2. Rules

| # | Rule | How (GitHub) | Blocking |
|---|---|---|---|
| H1 | Label `hotspot` is added when changed files match the paths | Action: `actions/labeler` (path config) | No (marker) |
| H2 | Changed lines (adds + dels) in hotspot files <= **400** | Action step: sum `git diff --numstat` of hotspot files vs base; fail above 400 | Yes |
| H3 | Hotspot PR > **1000** changed lines needs label `mechanical-change` (rename, format, generated) approved by a code owner | Same step; exception only with label + owner approval | Yes |
| H4 | 2 approvals, at least 1 from a code owner of the path | Ruleset: required approvals = 2, require code owner review | Yes |
| H5 | Hotspot PR changes or adds at least 1 test file (`*Test*`, `*Tests*`, `test/`, `spec/`), or has label `no-test-justified` with an owner comment | Action step: changed-file pattern check | Yes |
| H6 | PR title or branch names a Jira key | Action step: regex `[A-Z][A-Z0-9]+-\d+` | Yes (supports traceability S6) |
| H7 | Stale approvals dismissed on new push | Ruleset: dismiss stale reviews | Yes |

## 3. Exceptions

- Hotfix during an incident: label `incident-hotfix` + MI number; H2, H3, H5 waived; a follow-up PR with tests is required within 5 working days.
- Bulk mechanical changes: H3 label path only, never for logic changes.

## 4. Measure

Monthly from the research DB: follow-up CFB-fix rate within 30 days for hotspot PRs (baseline: 20.7% at 0-50 lines up to 53.8% above 1000), review threads per 100 lines, Jira-key rate. Goal: the hotspot rate for PRs above 400 lines falls to the rate for PRs at or under 150 lines (~19%).

## 5. Open

- Branch protection / rulesets cannot be read with current access (HTTP 404). The repo admins must confirm the current rules.
- The monolith has no CODEOWNERS today. Code owners need write access.
