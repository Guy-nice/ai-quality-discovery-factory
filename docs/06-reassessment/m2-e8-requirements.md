# M2-E8 Requirements Quality

**Date:** 2026-10-25 | **Question:** how much customer pain comes from requirement or expectation gaps, not code defects? | **Data:** `req_signals`, `e8_expectation_sample` in `quality.sqlite`; [CSV](../../data/aggregates/m2-e8-requirements.csv); script `scripts/db/m2_e8_requirements.py`
**Scope:** CFBs 2025-01..2026-10-22, MI-investigation tickets excluded (D-032). Investigation only, no solution design.

## Answer

About **1 in 4 customer bug reports is closed as "not a defect"** (Works as Designed, Not a bug, Limitation). In a read sample, **about 4 in 10 of those closures are real requirement or documentation gaps**: the product behaves as built, but not as the customer expects or as documented. Requirement gaps are a large share of customer pain that defect counts hide. The data also shows a **correlation** between weak requirement artifacts and changes that later cause CFBs. It does not prove a cause.

## 1. Expectation closures (EVIDENCE, High)

| Scope | Closed as WAD / Not a bug / Limitation | % (95% CI) |
|---|---|---|
| 2025 Jan-Oct | 306 of 1,107 | 27.6 (25.1-30.4) |
| 2026 Jan-Oct | 280 of 1,162 | 24.1 (21.7-26.6) |
| VMS, Recording, QM & FM | 43 of 121 | 35.5 (27.6-44.4) |
| WFM | 125 of 391 | 32.0 (27.5-36.7) |
| LiveVox & Digital | 83 of 269 | 30.9 (25.6-36.6) |
| Analytics and Data | 181 of 702 | 25.8 (22.7-29.1) |
| Orchestration Core | 74 of 350 | 21.1 (17.2-25.7) |

- These closures are not minor: 52% were P1/P2, with 1.67 incidents on average.
- The share is stable between years. It is a standing problem, not the cause of the 2026 rise.

## 2. What these closures really are (EVIDENCE, Medium; n=40, single AI rater)

Random sample (seed 20261025), classified from summary, Jira comments and RCA.

| Class | n | % (95% CI) |
|---|---|---|
| Expectation gap: built as designed, the design does not meet the customer need (missing capability, design limit, behavior change in a new data model) | 11 | 27.5 (16.1-42.8) |
| Documentation / communication gap: behavior or a deprecation not documented or not told to the customer | 6 | 15.0 (7.1-29.1) |
| **Requirement or documentation gap, combined** | **17** | **42.5 (28.5-57.8)** |
| Real defect closed as "not a defect" (fix later deployed, KI open, change-caused outage) | 6 | 15.0 (7.1-29.1) |
| User / configuration error | 6 | 15.0 |
| Misrouted, process ticket or third party | 6 | 15.0 |
| Not reproducible / unclear | 5 | 12.5 |

- **Estimate (Low-Medium):** about 285 (CI about 190-390) requirement or documentation gaps among the 672 expectation closures of 2025-01..2026-10. That is in addition to the 1,565 valid CFBs, so about 15% of all customer pain reports.
- **Data-quality finding:** about 15% of "not a defect" closures hide real defects. So invalid-closure counts understate defects, and "valid CFB" metrics need a check.
- Several expectation gaps come from **behavior changes in new components**: the NRT data model vs legacy, a new agent app release, a deprecated widget. The behavior changed without the customer expectation or the documentation following.

## 3. Requirement gaps inside fixed defects (EVIDENCE, Medium)

RCA escape cause "requirements/spec gap": 22 of 288 classified fixed CFBs (**7.6%**, CI 5.1-11.3). By VP, WFM is highest (5 of 34, 14.7%) and A&D lowest (2 of 41, 4.9%). Small n per VP, so the CIs overlap.

## 4. Requirement artifacts of changes that caused CFBs (CORRELATION, Low-Medium)

Causing Stories (from RCA "introduced by", resolved 2025+, n=68) vs controls: Stories of the same project, resolved in the same window, that did not cause a CFB (n=44, 31 with the same quarter).

| Signal | Causing | Control | Reading |
|---|---|---|---|
| Story links a spec (Confluence / PRD / Figma) | 6.8% (2.3-18.2) | 31.8% (20.0-46.6) | **CIs do not overlap** |
| Story or its Epic links a spec | 19.1% (11.5-30.0) | 38.6% (25.7-53.4) | Lower, overlapping CIs |
| Story AC has real content (>= 40 chars) | 68.2% (53.4-80.0) | 81.8% (68.0-90.5) | Lower, overlapping CIs |
| Epic AC has real content | 61.8% (49.9-72.4) | 85.4% (71.6-93.1) | Lower, CIs touch |
| Epic description median length | 586 chars | 1,215 chars | Shorter |

- **CORRELATION:** Changes that later caused CFBs had weaker written requirements, mostly fewer spec links and shorter Epics.
- **Not causal:** causing items may also be small tasks (refactors, quick fixes) that naturally have less spec. Item type and size are not controlled.
- AC "presence" is a weak signal. Placeholder AC (".") passes a presence check, so the field-fill rate (R6: 88-100%) overstates AC quality.

## 5. Not measured

- **Requirement churn** (AC or description edits after work started): the Jira changelog is too large per item for this tool at scale. One example shows a Story reopened from Done and edited after a revert. **UNKNOWN.**
- Story points: the real field is `customfield_10038`, not read. Not used.
- PM / customer-facing documentation quality, and release-note coverage of behavior changes.

## Limits

- Single AI rater for the sample (n=40); wide CIs.
- The control match covers 12 of 23 projects; 11 projects had no control pool in the pulled window.
- Spec-link detection uses text patterns in the description and AC; remote links (Confluence page links stored outside the text) are not counted, so both groups are under-counted.
- CFB = customer-reported only. Expectation gaps that customers do not report are not visible.
