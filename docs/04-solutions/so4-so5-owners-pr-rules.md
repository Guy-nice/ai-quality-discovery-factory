# SO-4 Owners + SO-5 Hotspot PR Rules (data-based)

**Date:** 2026-10-22 | **Data:** `so45_owners`, `so45_size_risk` (DB); 203 author logins + 2,568 PR reviews (GitHub API, read-only) | **Script:** `scripts/db/so45_owners.py`
**Drafts (not applied):** [CODEOWNERS.inContact](drafts/CODEOWNERS.inContact), [CODEOWNERS.routing-ng-advanced-findmatch](drafts/CODEOWNERS.routing-ng-advanced-findmatch), [CODEOWNERS.routing-ng-agent-capacity-service](drafts/CODEOWNERS.routing-ng-agent-capacity-service), [hotspot-pr-rules](drafts/hotspot-pr-rules.md)

## Owners (rule: >= 5 commits in 12 mo + active in last 6 mo, or >= 10 human reviews in 6 mo; GitHub account required)

| Hotspot directory | Owners (draft) | Status |
|---|---|---|
| VCSvc/Providers/ACD | NiceLuc, dezgrant, JessePreveyNiceInContact, jmichaelcharles15 | OK (4) |
| VCSvc/Providers/Data | NiceLuc, JigyasaDewani, SiddharthGhogareNice, sambhajigayake | OK (4) |
| VCSvc/Providers/Agent | dezgrant, jmichaelcharles15, rsenthilkumar-nice, ajbobo-nice | OK (4) |
| Library/AgentHelper | hpganesh1, jesse-blanton, dezgrant | OK (3); onkargadekar left out: Confluence account deactivated, commits until 2026-10 - verify |
| AgentHelper/MCH | NiceLuc, hpganesh1, chris-thomsen | **Gap:** 0 qualified committers; owners taken from reviewers + parent dir |
| InterVCCommWrapper (all subdirs) | jmichaelcharles15, NiceLuc, selvarajv3 | **Gap:** 1 qualified committer; NiceLuc by reviews; selvarajv3 "to grow" |
| DB StoredProcedures | JigyasaDewani, SiddharthGhogareNice, gchindheincontact, HemantYadavIncontact | OK (4) |
| AFM afm/service | karthickNiC, jkmuthazhagan, anuja-mehendre-incontact | OK (3); existing `*` owners jpenman51 / hdumaniya are not active in this dir |
| agent-capacity client | ajbobo-nice + team | **Gap:** 1 owner; former main author inactive since 2026-04 |

Existing CODEOWNERS: monolith **none**; AFM `* @jpenman51 @karthickNiC @hdumaniya`; agent-capacity `* @inContact/routing-ng-admins`. Branch protection is not readable (HTTP 404).

## PR size vs follow-up CFB fix within 30 days (merged PRs 2025-01..2026-09; Wilson 95% CI)

| Changed lines | Hotspot PRs | Rate | Non-hotspot rate | Review threads / 100 lines (hotspot) |
|---|---|---|---|---|
| 0-50 | 82 | 20.7% (13.4-30.7) | 3.7% | 3.26 |
| 51-150 | 52 | 17.3% (9.4-29.7) | 3.1% | 0.80 |
| 151-400 | 48 | 27.1% (16.6-41.0) | 4.2% | 0.24 |
| 401-1000 | 57 | 33.3% (22.5-46.3) | 5.1% | 0.30 |
| > 1000 | 130 | **53.8% (45.3-62.2)** | 5.5% | 0.03 |

- **EVIDENCE (Medium):** Outside hotspots the rate is flat (3-6%) at every size. The rise is a hotspot x size effect, so a path-based rule is justified.
- **EVIDENCE (Medium):** In hotspots, review per line drops about 100x from small to large PRs.
- **EVIDENCE (Medium):** Large non-AI PRs are riskier than large AI PRs (> 1000 lines: 39.1% vs 11.2%). So an AI-only rule would target the wrong variable.

## Chosen limits

- **400 changed lines** in hotspot files = blocking limit (split the PR). Risk rises above 400, and review per line is already very low.
- **1000** = hard stop. A larger PR is allowed only as a labelled mechanical change approved by an owner. It is 2.6x the risk of a small hotspot PR, and the CIs do not overlap.
- 2 approvals including 1 code owner; tests changed or justified; Jira key required (rules H1-H7 in the spec).

## Gaps and limits

- 3 directories have fewer than 3 qualified committers (MCH, InterVCCommWrapper, agent-capacity client). The team leads must name or grow owners.
- The follow-up measure counts later CFB fixes on the same files, so larger PRs touch more files. The flat non-hotspot curve suggests this bias is small.
- Reviews are counted per PR, not per line. AI review bots are excluded (user type "Bot").
- Monolith PR history before the TFS migration is missing. 2025 is mostly service PRs.
