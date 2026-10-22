# RCA Classification - Method and Limits

**Run date:** 2026-10-22 | **Source:** Jira (read-only) | **Output:** `rca-classification.csv` (one row per issue, labels only, no free text)

## Population and sample

- Population: `issuetype = Bug and salesforceAssociatedTypes is not EMPTY and resolution = Fixed and created >= "2025-10-22"` = 715 issues (count at run time).
- Sample: 4 pages x 40 ordered `created DESC` + 2 pages x 40 ordered `created ASC`. 240 unique issues (34% of population).
- Fields read: Root Cause Analysis (`customfield_10117`), R&D VP (`customfield_14852`), priority, project, created.
- **Sample is not random.** It covers created months 2025-10 to 2025-12 and 2026-07 to 2026-10. **No issues from 2026-01 to 2026-06** are in the sample.

## RCA fill rate (sample)

| State | Count | % |
|---|---|---|
| Filled (has answers) | 213 | 88.8% |
| Template only / empty | 20 | 8.3% |
| "N/A" or blank answers under template headings | 7 | 2.9% |

Rule: "template only" = all template prompt sentences still present and length < 1,100 characters (template alone is ~950-990 characters). Long fields that keep the prompts but add answers count as filled.

Quality note: "filled" does not mean useful. 20 of 213 filled RCAs (9.4%) do not state a cause that could be classified (label `unclear/not stated`). One project (PMSTND, WFM) has many 1-word or "NA" answers.

## Rubric (one primary label per issue)

| Column | Values |
|---|---|
| escape_cause | requirements/spec gap; missing test coverage (scenario not tested); test existed but ineffective; regression from recent change (RIA miss); environment/config/data difference prod vs test; third-party/integration/dependency; scale/performance/concurrency/race; legacy/unknown behavior (no one knew the behavior); deployment/release process; monitoring gap; unclear/not stated |
| introduced_by | specific recent change; long-standing/legacy code; external change; unknown |
| regression | yes / no / unknown (as judged from the RCA text, not a Jira field) |
| legacy_mentioned | yes if the text names monolith / legacy / old code |
| ai_mentioned | yes if the text says AI/LLM-generated code contributed |
| prevention_action_type | test added; process change; code fix only; monitoring/alert; none stated |

Decision rules used:
- A change that broke existing behavior and RIA did not foresee it -> `regression from recent change`, even when tests were also missing.
- Race conditions and load/volume limits -> `scale/performance/concurrency/race`, even when the RCA also says "no test".
- Test data or lower environments that do not reflect production (data shape, region config, FIPS, replication lag) -> `environment/config/data difference`.
- Feature toggles enabled early, missed cherry-picks, provisioning and key rotation errors -> `deployment/release process`.

## Side counts (not columns)

- AI tools named in the RCA as part of **review or remediation** (not as cause): 4 issues (an AI PR review tool flagged a missing test that was not acted on; an AI reviewer missed the gap; AI used to scan for similar defects; an "AI COE review" added to a checklist).
- AI-generated code named as a **cause**: 0.

## Limitations

1. Single rater (one model pass). No inter-rater check. Confidence per label: Medium.
2. Sample is not random and misses 2026-01 to 2026-06.
3. RCAs are self-reported by the owning team. They may under-report process causes and over-report "edge case".
4. Only `resolution = Fixed` is included. Bugs closed as Cannot Reproduce, Won't Do, and so on are excluded.
5. Absence of an AI mention does not show that AI was not used. The RCA template has no question about AI use.
6. RCA text was read but is not stored here (it contains customer and person names).
