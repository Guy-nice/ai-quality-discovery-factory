# Quality Definition of Done v2 - Evidence-Based

**Date:** 2026-10-25 | **Revises:** [WIP Quality Definition of Done](https://nice-ce-cxone-prod.atlassian.net/wiki/spaces/CX/pages/4048715783) (Confluence 4048715783) | **Basis:** quality model v0, action plan v1, current gates check | **Status:** proposal; ready to paste into Confluence

## Principle

**A gate blocks only where data proves the risk.** Everything else is a policy or a suggested means, measured and reviewed. Tiers come from evidence (impact, failure type, hotspot code), not from product names.

Why the DoD must change: P1/P2 customer-found bugs +49% (Jan-Sep 2026 vs 2025); customers detect 96% of P1 incidents; today almost every "mandatory" item is policy with no control; teams differ strongly (incidents per bug 1.1-10.4).

## Epic level

| WIP DoD item | v2 verdict | Enforcement | Evidence |
|---|---|---|---|
| G1 PRD / Epic review, acceptance criteria | **Keep, strengthen** for risky Epics: add state / ordering and toggle sections, spec link | Jira flow + monthly sample audit | Causing stories link a spec 6.8% vs 31.8%; ~15% of reports are expectation gaps |
| RIA phase 1 (Epic) | **Change:** aim at bug fixes and hotspot changes, not every Epic | Policy | RIA miss 7-15% of escapes; half of misses had RIA done |
| RIA phase 2 (PR diff) | **Later**, hotspot paths only | Suggested until proven | Same |
| Test plan generation, Playwright generator | **Keep as means** (feed tests) | Suggested | No evidence they reduce escapes yet |
| Test types covered or ruled out | Keep | Policy | - |
| Test plan reviewed with PM / Architect, PO approval | **Keep for high-impact teams only** | Policy | Teams differ; cost where risk is low |
| SonarQube gate passed | **Keep, make blocking everywhere** | Required CI check | Required in 1 of 5 pilot repos today |
| Mutation testing >= 80% (blocking) | **Change:** visible in Sonar first; block per scope after fixes and evidence | Visible -> blocking per scope | Weak tests = 3% of escapes; 2 of 4 pilot fails were false |
| UI automation (Playwright) | Keep | Suggested | - |
| Results in ReportPortal; pipeline stable | **Change to test health:** a suite blocks only while it holds its agreed pass level for 14 days | Blocking when healthy | Routing E2E passed 1.2% of runs; other suites 69-79% |
| Accessibility WCAG 2.2 AA | Keep (frontend) | Policy | Not assessed in this research |
| Component performance test | **Keep for high-impact services** | Release check | Scale / race escapes ~13-23% |
| Local Chaos Runner | **Keep for routing and contact lifecycle** | Release check | Race / ordering escapes ~23% in pilot |
| Exploratory testing | Keep | Go/No-Go criterion | - |
| All tests in Xray, linked to the Epic | **Change:** require links for escape tests and high-risk Epics | Policy + audit | Links today 18-25% |
| Passing in Dev | Keep | Pipeline | - |

## Release level

| WIP DoD item | v2 verdict | Enforcement | Evidence |
|---|---|---|---|
| Feature toggle registered, owner, removal ticket | **Keep, mandatory** | Release check | Monolith cannot roll back |
| Toggle verified on and off | Keep for high-impact changes | Release check | Same |
| Deploy and rollback verified | **Change:** "toggle-off verified + progressive rollout" for the monolith | Release check | Rollback not applicable to the monolith |
| Post-deploy sanity, triggered by toggle | Keep | Release check | - |
| Synthetic monitor for changed customer paths | **Strengthen:** monitors for correctness invariants (routing, contact lifecycle, report data) | Release check for those types | 96% of P1 found by customers; correctness = 46% of valid bugs |
| No open P1, P2 or P3 defects | Keep | Go/No-Go | - |
| Go/No-Go sign-off | **Change:** data-based (8 quality dimensions, test health, open P1-P3) | Human, with data | 26.4 pages mostly "TBD" |

## New items (not in the WIP page)

| Item | Level | Enforcement | Evidence |
|---|---|---|---|
| Bug intake rule: defect vs MI investigation vs expectation gap | All | Jira required fields | MI tickets inflated the 2026 headline |
| Each valid bug records failure type, detected-by, causing change | All | Jira required fields (X1) | Cause known for ~25% only |
| Escape-to-test: a valid customer bug closes with a linked test or a reason | Escape | Jira validator | 38% of RCAs add a test today |
| Hotspot PR rules: size limit, code-owner review, tests | PR | Blocking on hotspot paths | Follow-up fixes 21% (small) to 54% (large) in hotspots only |
| Bug-fix review on correctness types | PR | Policy -> blocking if X4 proves it | 1 in 4 known causes is a fix |
| Emergency-change follow-up review | Release | Policy | Emergency changes x2.9 since June 2026 |
| CODEOWNERS for hotspot code | PR | Required review | No CODEOWNERS in the monolith; bus factor 1 |

## Tiering (replaces product-name tiers)

| Tier | Assigned by | Gets |
|---|---|---|
| High risk | High-impact team type, correctness-critical failure types, hotspot code | All blocking checks + chaos / perf + invariant monitors |
| Standard | Other teams and code | Common baseline + Sonar + test health |

## Harness

Build the orchestration harness **only to run the checks above that block**. Agents stay suggested means until an experiment shows they reduce escapes.

## When

Now: intake fields, Sonar required, mutation visible, Go/No-Go with data, triage routing E2E. Q1 2027: hotspot PR rules and bug-fix review as experiments (X3/X4). April 2027: decide which checks become blocking per scope.
