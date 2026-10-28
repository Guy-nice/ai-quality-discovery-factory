# Gate Catalog - SDLC Stages S0-S8

**Date:** 2026-10-28 | **Status:** proposal (D-042) | **Parent:** [pod quality playbook](pod-quality-playbook.md) | **Revises:** [DoD v2](../05-summary/dod-v2-evidence-based.md) into one list per stage

Each gate has an ID, a stage, a mode, a scope and its evidence. A gate checks **evidence**, not the tool that made it. A pod can use our agents or its own tools.

## 1. Modes

| Mode | Meaning | Who sees a fail |
|---|---|---|
| **Advice** | A suggested means (agent, tool, practice). Not checked. | Pod only |
| **Visible** | Measured and shown on the pod dashboard. Does not stop work. | Pod + QA&RM |
| **Audit** | Checked on a sample each month or quarter. | Pod + QA&RM + VP review |
| **Block** | A required check. Work cannot continue until it passes or an exception is logged. | Everyone |

## 2. Scope

| Scope | Applies to |
|---|---|
| **All** | Every pod, every change |
| **T1** | High-risk tier: correctness-critical failure types (routing, contact lifecycle, report data, agent state), archetype-A pods, release-critical services |
| **Hotspot** | Any change that touches a hotspot path (top directories by customer-bug-fix density), in any pod, by any author |

Risk sits in the **change and the code area**, not only in the pod. A standard pod that edits a hotspot path gets the hotspot gates for that change.

## 3. Gate lifecycle

A gate moves only forward with evidence, and it can be retired.

`Proposed -> Visible (1 quarter of data) -> Block per scope (evidence it helps) -> Review each quarter -> Retire (no value)`

- **To Block:** an experiment or a before/after check shows it lowers escapes or follow-up fixes vs control, **and** false blocks stay under 5% of runs (proposed level, set per gate at Visible stage).
- **To Retire:** no catch and no outcome change for 2 quarters, or false blocks above the agreed level for 1 quarter.
- **Every gate has** an owner, a metric, a false-block rate and an exception path.

## 4. Catalog

| ID | Stage | Gate (what must be true) | Mode now | Target mode | Scope | Evidence |
|---|---|---|---|---|---|---|
| G0.1 | S0 Intake | Each report has a type: defect, MI investigation or expectation gap | Visible | Block (Jira field) | All | MI tickets inflated the 2026 rise ([why numbers changed](../06-reassessment/why-numbers-changed.md)) |
| G0.2 | S0 Intake | Each valid customer bug records failure type, detected-by and causing change | Visible | Block on close (after X1) | All | Cause known for ~25% only ([X1](../07-quality-model/experiment-protocols-v0.md)) |
| G1.1 | S1 Plan | Acceptance criteria and a spec link exist | Audit | Audit | All | Causing stories link a spec 6.8% vs 31.8% ([E8](../06-reassessment/m2-e8-requirements.md)) |
| G1.2 | S1 Plan | Risky Epic has a state, ordering and toggle section | Advice | Audit | T1 | Race and ordering escapes ~23% ([SO-1](../04-solutions/so1-state-races.md)) |
| G1.3 | S1 Plan | Risk impact analysis (RIA) for bug fixes and hotspot changes | Advice | Visible | T1, Hotspot | RIA miss 7-15% of escapes ([DoD v2](../05-summary/dod-v2-evidence-based.md)) |
| G2.1 | S2 Build | Tests come with the change (unit, contract or E2E, pod choice) | Advice | Advice | All | Untested scenarios 28-31% of escapes ([SO-2](../04-solutions/so2-escape-to-test.md)) |
| G2.2 | S2 Build | AI-assisted PRs carry a label or commit trailer (for measuring, not for gating) | Advice | Visible | All | AI effect could only be measured where AI use was visible ([E9](../06-reassessment/m2-e9-ai.md)) |
| G3.1 | S3 Review | PR names a Jira key | Block | Block | All | Exists today; enables traceability ([current gates](../06-reassessment/current-gates-2026-10-25.md)) |
| G3.2 | S3 Review | Hotspot PR <= 400 changed lines, or a `mechanical-change` label approved by an owner | Visible | Block (after X3) | Hotspot | Follow-up fixes 21% (small) to 54% (large) in hotspots only ([R3](../02-research/r3-r14-hotspots-ownership.md)) |
| G3.3 | S3 Review | Code-owner review on hotspot paths; 2 approvals | Visible | Block | Hotspot | No CODEOWNERS in the monolith; bus factor 1-2 ([SO-4/5](../04-solutions/so4-so5-owners-pr-rules.md)) |
| G3.4 | S3 Review | Hotspot PR changes a test, or has an owner-approved `no-test-justified` reason | Visible | Block (after X3) | Hotspot | [Hotspot PR rules](../04-solutions/drafts/hotspot-pr-rules.md) |
| G3.5 | S3 Review | Bug-fix PR on a correctness type gets a second reviewer | Advice | Block if X4 proves it | T1 | 1 in 4 known causes is a fix ([D6](../07-quality-model/quality-model-v0.md)) |
| G4.1 | S4 CI | Build and unit tests pass | Block | Block | All | Exists today |
| G4.2 | S4 CI | Sonar quality gate is a required check | Visible | Block | All | Required in 1 of 5 pilot repos ([current gates](../06-reassessment/current-gates-2026-10-25.md)) |
| G4.3 | S4 CI | Security and dependency scan (Aikido) passes | Block | Block | All | Exists today |
| G4.4 | S4 CI | Mutation score on changed code is shown in Sonar | Advice | Visible; Block per scope only with evidence | All | Weak tests = 3% of escapes; 2 of 4 pilot fails were false (D-040) |
| G4.5 | S4 CI | An E2E suite blocks only while it holds its agreed pass level for 14 days | Visible | Block when healthy | All | Routing E2E passed 1.2% of runs; 50 of 66 retried commits flaky ([SO-3A](../04-solutions/so3a-e2e-trust.md)) |
| G4.6 | S4 CI | A failing suite has a named owner and a triage date | Advice | Audit | All | Failures ignored for 6 months ([SO-3A](../04-solutions/so3a-e2e-trust.md)) |
| G5.1 | S5 Release | Go/No-Go uses data: open P1-P3, test health, D1-D8 trend | Advice | Block (human decision with data) | All | 26.4 pages mostly "TBD" ([current gates](../06-reassessment/current-gates-2026-10-25.md)) |
| G5.2 | S5 Release | Feature toggle registered, with owner and removal ticket | Audit | Block | All monolith changes with behavior risk | Monolith cannot roll back ([DoD v2](../05-summary/dod-v2-evidence-based.md)) |
| G5.3 | S5 Release | Performance and chaos stage passed | Advice | Block | T1 | Scale and race escapes 13-23% ([DoD v2](../05-summary/dod-v2-evidence-based.md)) |
| G6.1 | S6 Deploy | Toggle-off verified and progressive rollout used | Audit | Block | T1 | Rollback not possible on the monolith |
| G6.2 | S6 Deploy | Post-deploy sanity runs, triggered by the toggle | Audit | Block | All | WIP DoD item, kept |
| G6.3 | S6 Deploy | Emergency change gets a follow-up review within 5 working days | Advice | Audit | All | Emergency changes x2.9 since June 2026 ([D6](../07-quality-model/quality-model-v0.md)) |
| G7.1 | S7 Operate | Monitors check correctness invariants (routing, contact lifecycle, report data) | Advice | Visible (shadow, X2), then Block release for T1 | T1 | 96% of P1 enter via customer cases ([impact](../06-reassessment/m2-impact-servicenow.md)) |
| G7.2 | S7 Operate | Each T1 service has an SLO and an error budget | Advice | Visible | T1 | No SLO data today (D3 gap) |
| G8.1 | S8 Learn | RCA for every valid P1/P2 bug | Audit | Audit | All | Already 80-100% in every team |
| G8.2 | S8 Learn | Valid customer bug closes with a linked test or a reason | Visible | Block on close | All | 38% of RCAs add a test today ([SO-2](../04-solutions/so2-escape-to-test.md)) |
| G8.3 | S8 Learn | Monthly pod review of D1-D8 vs own baseline | Visible | Audit | All | Teams differ 1.1-10.4 incidents per bug ([teams](../06-reassessment/m2-teams.md)) |

## 5. Exceptions

- **Incident hotfix:** label `incident-hotfix` + MI number. G3.2, G3.4 and G4.5 are waived. A follow-up PR with tests is due within 5 working days (G6.3).
- **Mechanical change:** G3.2 waived with label `mechanical-change` and owner approval. Never for logic changes.
- Every exception is logged. QA&RM reviews the exception rate per pod each month. A high rate is a signal, not a fault.

## 6. What is not a gate

Agents and tools are **means**: test-plan generation, Playwright generator, exploratory agent, RIA agent, mutation agent. A pod can use them, replace them or skip them. The gate asks only for the evidence (G2.1, G3.4, G8.2), never for the tool.
