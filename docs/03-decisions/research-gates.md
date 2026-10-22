# Research Gates

**Version:** v0 | **Date:** 2026-10-22

Do not advance without recording gate status here. Solution design starts only after Gate 4 = PASSED.

## Current status

| Gate | Name | Status | Blocking items | Last review |
|---|---|---|---|---|
| G0 | Charter Alignment | PASSED (interim) | Scope set by research (D-005, D-006). Sponsor (U-02) and data rule (U-04) still open, interim rule D-004 applies. | 2026-10-22 |
| G1 | Evidence Access | PARTIAL | Jira, Confluence, Git (`inContact`, incl. monolith) confirmed. Sonar, CI/CD, incidents open (U-09). | 2026-10-22 |
| G2 | Problem Definition | PASSED (interim) | Problem statement v3. Not blocking: U-14, human rater, U-15. | 2026-10-22 |
| G3 | Risk and Scope Selection | PASSED (interim) | Pilot D-010. R3 hotspots (Git) still needed for the deep dive. | 2026-10-22 |
| G4 | Solution Readiness | PASSED (interim, data-based) - [readiness v1](gate-4-readiness-v0.md#update-v1---2026-10-22-iteration-12) | In scope: PH-1, PH-4, P-05, test gap. Out until human data: PH-2 (U-23), PH-5 (U-25). | 2026-10-22 |

## Gate criteria

### G0 - Charter Alignment
- [ ] Product / domain scope and exclusions defined (U-01)
- [ ] Sponsor, decision, and deadline known (U-02)
- [ ] Triggering signal recorded (U-03)
- [ ] Data handling rule confirmed (U-04)
- [ ] Charter v1 reviewed by sponsor

### G1 - Evidence Access
- [ ] Each source marked available / partial / none
- [ ] Permissions confirmed for core sources (Jira, Confluence, Git)
- [ ] Data limits documented (retention, field quality)
- [ ] Missing systems listed with alternative methods

### G2 - Problem Definition
- [ ] Quality definition agreed (U-05)
- [ ] Trend with 18-24 month baseline, normalized (R1)
- [ ] Confounders checked (R4, U-11)
- [ ] Problem statement v1 based on evidence, with confidence level

### G3 - Risk and Scope Selection
- [ ] Defect concentration analysis (R2)
- [ ] Hotspot analysis (R3)
- [ ] Pilot area selected with scoring and rationale (decision log entry)

### G4 - Solution Readiness
- [ ] Minimum evidence set complete (see [research plan](../02-research/research-plan-v0.md#4-minimum-evidence-before-solution-design-gate-4))
- [ ] At least 2 root-cause hypotheses validated against counter-evidence
- [ ] Baseline metrics fixed
- [ ] Constraints documented
- [ ] Success criteria agreed with sponsor

## Gate history

| Date | Gate | Change | By |
|---|---|---|---|
| 2026-10-22 | All | Gates defined, all OPEN | Guy Guterman |
| 2026-10-22 | G0 | PASSED (interim): lead delegated scope (D-005); scope and quality definition set (D-006) | Research |
| 2026-10-22 | G1 | PARTIAL: Jira and Confluence read access confirmed | Research |
| 2026-10-22 | G2 | PARTIAL: findings round 1 + problem statement v1 | Research |
| 2026-10-22 | G2 | PARTIAL: findings round 2 + problem statement v2; U-13, U-17 closed | Research |
| 2026-10-22 | G3 | PASSED (interim): pilot D-010 | Research |
| 2026-10-22 | G2 | PASSED (interim): R8 + R9, problem statement v3 | Research |
| 2026-10-22 | G1 | Git org `inContact` read access confirmed; TFS and CI/CD still open | Research |
| 2026-10-22 | G4 | Readiness package v0: NOT PASSED; 3 blocking items | Research |
| 2026-10-22 | G4 | PASSED (interim, data-based): R17 refutation, D-022, D-023 | Research |
