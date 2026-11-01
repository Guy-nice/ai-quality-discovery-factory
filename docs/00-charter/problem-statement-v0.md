> **Superseded** by [v4](problem-statement-v4.md) and [quality model v0](../07-quality-model/quality-model-v0.md).

# Problem Statement v0

**Version:** v0 | **Date:** 2026-10-22 | **Status:** Perception only - not evidence-backed | **Gate 2:** OPEN

> v0 records the problem **as perceived**. It is not a confirmed problem. v1 will replace perception with evidence.

## 1. Perceived problem (from brief)

The organization may be changing software faster than it can reliably understand, validate, test, review, and safely release those changes. Quality is perceived to have declined.

## 2. Claim breakdown

| ID | Claim | Class | Evidence | Confidence | Could be invalidated by |
|---|---|---|---|---|---|
| P-01 | Quality has declined. | HYPOTHESIS | None yet | Low | Flat or improving escaped-defect / incident trend over 18-24 months, normalized for change volume |
| P-02 | Change rate exceeds validation capacity. | HYPOTHESIS | None yet | Low | Stable defect escape rate while change volume grows |
| P-03 | Legacy monolith concentrates risk. | HYPOTHESIS | None yet | Low | Defects and incidents spread evenly, or concentrated in new services |
| P-04 | AI-assisted development contributes to decline. | HYPOTHESIS | None yet | Low | No difference in defect/revert rate between AI-heavy and other changes, or decline starts before AI adoption |
| P-05 | Critical knowledge is concentrated in few people. | HYPOTHESIS | None yet | Low | Broad ownership spread in Git and SME interviews |

## 3. Initial observed signal

UNKNOWN (U-03). What triggered this initiative (incident, metric, executive concern, customer escalation) and when.

## 4. Definition of "quality"

UNKNOWN (U-05). Candidate measures, to be agreed with the sponsor:

- Escaped defects (customer-found bugs) per period, normalized per release or per change volume.
- Major incidents linked to changes.
- Change failure rate, rollback / hotfix rate.
- Reopen rate and regression rate.
- Time to restore.

## 5. Known confounders

Factors that can produce a false "decline" or hide a real one:

- Changes in defect reporting or classification practice.
- Growth in customers, usage, or product surface.
- Team changes, reorganizations, headcount.
- Release cadence changes.
- Tool migrations (Jira workflows, CI systems).

## 6. Next version trigger

v1 is written when Gate 1 passes and the first trend data (R1 in [research plan](../02-research/research-plan-v0.md)) exists.
