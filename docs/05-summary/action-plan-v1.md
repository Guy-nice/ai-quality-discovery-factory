# Action Plan v1 - What to Keep, Change, Stop, Start, and When

**Date:** 2026-10-25 | **Basis:** quality model v0 (D-034), experiment protocols (D-038), findings mission v2 | **Status:** recommendation for management decision

## 1. The answer in 4 lines

1. **Quality fell in severity, not volume.** P1/P2 customer-found bugs +49%, all customer-found bugs +13% (Jan-Sep 2026 vs 2025). Customers detect 96% of P1 incidents.
2. **The main gaps are not tools.** Intake and measurement are mixed. The test signal is not trusted. We do not detect correctness failures in routing and data. Teams differ too much for one workflow.
3. **Our gates and quality automation are mostly policy, not control.** They are applied the same way to every team, whatever its risk.
4. **Fix measurement first, then test practices in a few teams, then spread what works.** AI use continues under the same rules as all changes.

## 2. Keep, change, stop, start

| | What | Evidence |
|---|---|---|
| **Keep** | RCA for valid P1/P2 bugs | Already 80-100% in every team |
| **Keep** | Feature toggles for risky changes | Monolith cannot roll back |
| **Keep** | AI-assisted development, under the same rules as other changes | Not riskier per change (matched ratio 0.78-0.84) |
| **Keep** | Xray test management | Heavy use (1.15M executions in 2026) |
| **Change** | Bug intake: separate defect, MI investigation and expectation gap; record failure type, detected-by, cause, customers | MI tickets inflated the headline; cause known for ~25% only |
| **Change** | Go/No-Go: from "TBD" pages to data (8 dimensions, open P1-P3, E2E health) | All 26.4 domain pages show "TBD" |
| **Change** | E2E tests: make the signal trustworthy before it blocks anything | Routing pipeline passed 1.2% of runs; failures ignored |
| **Change** | Review: depth scales with change size in hotspot code, for every author | Follow-up fixes 21% (small) to 54% (large) in hotspots only |
| **Change** | RIA: aim it at bug fixes and hotspot changes, not a blanket field | Story RIA 0%; 1 in 4 known causes is a fix |
| **Change** | Quality reporting (QSU): valid, severity-weighted, per team vs its own baseline | Raw counts misled twice |
| **Stop** | Raw customer-bug count as "the quality number" | 30-51% invalid; MI tickets mixed in |
| **Stop** | One gate set for all teams | Incidents per bug 1.1-10.4 between teams |
| **Stop** | Unused Jira quality fields | 9 of ~15 fields < 2% filled |
| **Stop** | "Mandatory" items with no control behind them | Policy on paper does not change outcomes |
| **Start** | Quality model: 8 outcome dimensions with decisions | Quality definition v1 |
| **Start** | Team -> service -> code map with owners | Does not exist today |
| **Start** | Detection monitors for routing, contact lifecycle and report data | 96% of P1 via customer cases; correctness = 46% of valid bugs |
| **Start** | Expectation-gap triage with product owners | ~15% of reports are real requirement / doc gaps |
| **Start** | Owner backups for hotspot code | Bus factor 1-2 on the densest code |
| **Start** | 5 pre-registered experiments (X1-X5) | Power-checked designs |

## 3. Our gates and quality automation - what the evidence says

| Means | Recommendation now | Why |
|---|---|---|
| Gates (G1-G6, WIP DoD) | Keep a **few blocking checks** where data shows risk: intake fields, hotspot change size and review. Everything else waits for experiment results. | Blocking is justified only where a risk is proven |
| Go/No-Go | Make it data-based | It is the one gate that exists today |
| E2E automation | Repair trust first; then block on suites that stay >= their agreed pass level | A broken signal blocks nothing useful |
| Sonar / dependency scan | Keep as build checks | Low cost; not a main escape cause |
| RIA agents | Later, aimed at fixes and hotspots | RIA misses = 7% of pilot escapes |
| Mutation testing | Planned blocking gate 2026-12-15 (80% on changed code). Recommend: visible, non-blocking in Sonar first; block per scope only after false-negative fixes and evidence ([current gates](../06-reassessment/current-gates-2026-10-25.md)) | Weak tests = 3% of escapes; 2 of 4 pilot fails were false |
| Agent harness | Build only to run the checks that experiments prove | Harness without proven checks adds cost |

## 4. When

| When | What | Who decides / owns |
|---|---|---|
| **Now (Nov 2026)** | Management decisions: sponsor, approve X1-X5, ServiceNow read access, team-map owner. Start X1 (intake) and X2 (detection, shadow mode). QSU switches to valid, severity-weighted, per-team view. Triage the 13 failing routing E2E scenarios. | Management; QA Architect; team leads |
| **Q1 2027** | X3 and X4 step 1 (pooled, hotspot and bug-fix PRs). X5 with product owners. Monthly quality review per team vs own baseline. Re-test the AI effect with a 90-day window. | QA Architect; VP quality review |
| **Q2 2027 (April review)** | X3/X4 step 2. Review all experiments against controls. Quality model v1 with justified targets. Decide which checks become blocking. | Sponsor; VP quality review |
| **H2 2027** | Spread proven practices to Analytics and Data, WFM and the rest. Decide on RIA agents, mutation testing and the agent harness from the evidence. | Sponsor |

## 5. What success looks like by April 2027

- Every valid customer bug records failure type, detected-by and cause (today: cause ~15-25%).
- Each team sees its 8 dimensions against its own baseline every month.
- At least one correctness type is detected by our monitors before customers.
- Experiments X1-X5 have results with confidence intervals; only practices that beat their controls spread.
