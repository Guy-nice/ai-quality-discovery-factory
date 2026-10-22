# CFB Time Series - Method

**Run date:** 2026-10-22 | **Source:** Jira Cloud `nice-ce-cxone-prod` (SRC-001), read-only, count queries only | **Content stored:** counts only

## Definitions

- **CFB (Customer Found Bug), working definition:** `issuetype = Bug and salesforceAssociatedTypes is not EMPTY` (Bug linked to a Salesforce case). Source: initiative lead.
- **Quarter window:** `created >= "<start>" and created < "<next start>"`.

## JQL templates

| Column | JQL |
|---|---|
| cfb_all | `issuetype = Bug and salesforceAssociatedTypes is not EMPTY and created >= "S" and created < "E"` |
| cfb_p1p2 | cfb_all + `and priority in (P1, P2)` |
| bugs_all | `issuetype = Bug and created >= "S" and created < "E"` |
| stories_resolved | `issuetype = Story and resolved >= "S" and resolved < "E"` |
| cfb_invalid | cfb_all + `and resolution in ("Cannot Reproduce", "Not a Bug", "Won't Do", "Duplicate")` |
| cfb_open_now | cfb_all + `and statusCategory != Done` (state at run date) |
| yearly | cfb_all by calendar year; 2017 = all before 2018-01-01 |

## Derived columns

- `cfb_per_100_stories` = cfb_all / stories_resolved x 100 (delivery-volume normalization; proxy only)
- `cfb_share_of_bugs_pct` = cfb_all / bugs_all x 100
- `cfb_valid` = cfb_all - cfb_invalid; `p1p2_share_pct`, `invalid_share_pct` = share of cfb_all

## Caveats

- Priority names P1-P4 verified (11,659 of 11,662 CFBs have P1-P4).
- All 4 resolution names valid (no JQL errors). 4,337 of 11,662 CFBs (37%) are closed with one of them.
- `stories_resolved` counts all Jira projects. A rise can come from new projects or new tooling, not only more delivery.
- `bugs_all` has step changes (2024-Q1: 10,993; 2026-Q3: 18,014). Cause not known. Do not use as a denominator until explained.
- 2026-Q4 is partial (to 2026-10-22). Recent quarters have triage lag: low invalid share, high open count.
- `cfb_open_now` is 0 for all quarters before 2025-Q2. CFBs are closed (or cleaned up) reliably. This does not measure backlog over time.
- Jira migration 2022-11-25: CFB count 3 months before = 394, 3 months after = 367. No step change seen.
- CFB definition depends on the Salesforce connector link. Link practice changes can change counts.
