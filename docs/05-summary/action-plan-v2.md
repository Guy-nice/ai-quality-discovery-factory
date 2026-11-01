# Action Plan v2: What to Keep, Change, Stop, Start, and When

| | |
|---|---|
| **Version** | 2.0 (supersedes [v1](archive/action-plan-v1.md) of 2026-10-25) |
| **Date** | 2026-11-01 |
| **Basis** | Quality model v0 (D-034), experiment protocols (D-038), pod quality model (D-042), candidates from the Claude Code review model (D-043) |
| **Status** | Recommendation for management decision. D-042 and D-043 are proposals; D-038 is a draft. |
| **Report** | [Management report v2](management-report.md) |

**What changed from v1:** each action now names its gate ID from the [gate catalog](../08-pod-quality/gate-catalog.md). Pod roles and the QA&RM role are added. The timeline uses the 4 waves of the [pod quality playbook](../08-pod-quality/pod-quality-playbook.md). The new section 4 lists 3 low-effort candidates (D-043).

## 1. The answer in 4 lines

1. **Quality fell in severity, not mainly in volume.** P1/P2 customer-found bugs rose 49%; all customer-found bugs rose 13% (Jan-Sep 2026 vs 2025). Customers detect 96% of P1 incidents.
2. **The main gaps are not tools.** Intake and measurement are mixed. The test signal is not trusted. We do not detect correctness failures in routing and data. Pods differ too much for one workflow.
3. **Our gates are mostly policy, not control.** They apply the same way to every team, whatever its risk.
4. **Fix measurement first. Then prove practices in a few pods. Then spread what works.** AI use continues under the same rules as all changes.

## 2. Keep, change, stop, start

| | What | Gate or item | Evidence |
|---|---|---|---|
| **Keep** | RCA for valid P1/P2 bugs | G8.1 | Already 80-100% in every team |
| **Keep** | Feature toggles for risky changes | G5.2 | Monolith cannot roll back |
| **Keep** | AI-assisted development, under the same rules as other changes | P-01, A1 | No evidence of more risk per change (matched ratio 0.78-0.84, interval includes 1) |
| **Keep** | Security scan as a blocking check | G4.3 | About 40-45% of AI code samples had flaws in outside studies (one is a vendor report) |
| **Keep** | Xray test management | - | 1.15M executions in 2026 ([findings round 2](../02-research/findings-round-2.md)) |
| **Change** | Bug intake: separate defect, MI investigation and expectation gap; record failure type, detected-by, cause | G0.1, G0.2 | MI tickets inflated the headline; cause known for ~25% only |
| **Change** | Go/No-Go: from "TBD" pages to data (8 metrics, open P1-P3, test health) | G5.1 | Most 26.4 pages show "TBD" (master page TBD) |
| **Change** | E2E tests: make the signal trustworthy before it blocks | G4.5, G4.6 | Routing pipeline passed 1.2% of runs |
| **Change** | Review depth scales with change size in hotspot code, for every author | G3.2-G3.4 | Follow-up fixes 21% (small) to 54% (large), in hotspots only ([SO-4/5](../04-solutions/so4-so5-owners-pr-rules.md)) |
| **Change** | Sonar from optional to a required check | G4.2 | Required in 1 of 5 pilot repos |
| **Change** | RIA aimed at bug fixes and hotspot changes, not a blanket field | G1.3 | Story risk impact analysis (RIA) 0%; 1 in 4 known causes is a fix |
| **Change** | Quality reporting: valid, severity-weighted, per pod vs its own baseline | G8.3, P-05 | Raw counts misled twice |
| **Stop** | Raw customer-bug count as "the quality number" | P-06 | 30-51% invalid (org-wide range); MI tickets mixed in |
| **Stop** | One gate set for all teams | Tiers T1, hotspot | Incidents per bug 1.1-10.4 |
| **Stop** | Unused Jira quality fields | - | 9 of ~15 fields filled under 2% |
| **Stop** | "Mandatory" items with no control behind them | P-02 | Policy on paper does not change outcomes |
| **Start** | Quality model: 8 outcome metrics per pod | D1-D8 | Quality definition v1 |
| **Start** | Quality owner and release owner in every pod | Playbook C1, C2 | No owner for quality data today |
| **Start** | Pod -> service -> code map with owners | Playbook C3 | Does not exist (U-27) |
| **Start** | Detection monitors for routing, contact lifecycle and report data | G7.1 | 96% of P1 via customer cases |
| **Start** | Expectation-gap triage with product owners | X5 | About 15% extra reports are requirement or documentation gaps (low-medium confidence) |
| **Start** | Owner backups for hotspot code | G3.3 | Only 1-2 people know the densest code (bus factor 1-2) |
| **Start** | 5 pre-registered experiments (X1-X5) | Gate lifecycle | Power-checked designs |
| **Start** | Quarterly pod self-assessment | [Self-assessment](../08-pod-quality/pod-self-assessment.md) | Shows each pod its next step |

## 3. Gates and quality automation

| Means | Recommendation | Why |
|---|---|---|
| Gates | A **few blocking checks** where data shows risk. Everything else starts Visible and moves through the gate lifecycle. | Blocking is justified only where a risk is proven |
| Go/No-Go | Make it data-based (G5.1) | It is the one release gate that exists today |
| E2E automation | Repair trust first; block only on suites that hold their agreed pass level (G4.5) | A broken signal blocks nothing useful |
| Sonar, security scan | Required checks (G4.2, G4.3) | Low cost; outside evidence on AI security flaws |
| Mutation testing | Visible in Sonar on 2026-12-15; block per scope only after false-negative fixes and evidence (D-040) | Weak tests = 3% of escapes; 2 of 4 pilot fails were false |
| AI agents (test plan, Playwright, RIA, exploratory) | Paved road, not a duty (A5) | Agents block nothing today; no escape evidence yet |
| AI review on PRs | Pilot in X3 pods, Visible first, scored on the escape test set (D-043, C-03) | The Claude Code team claims gains; not yet proven on our code |
| Vendor platforms (e.g. Harness) | Decide only after proof tests on our data ([questions](../08-pod-quality/vendor-harness-questions.md)) | Vendor results are about speed, not escapes |

## 4. Low-effort candidates to start now (D-043, for decision)

| # | Action | Extends | Why |
|---|---|---|---|
| C-04 | PR template asks "How tested", "Risk", "How to revert" | G2.1, G5.2 | Forces toggle thinking where the monolith cannot roll back |
| C-05 | RCA records "which gate should have caught it" | G8.1 | Gives each gate real evidence for its lifecycle |
| C-01 | Escape test set from our DB (306 CFB-fix commits, 94 reverted PRs, causal links) | Gate lifecycle | Scores any reviewer, gate or vendor tool before rollout |

Source: [side-by-side comparison](../08-pod-quality/compare-claude-code-review.md).

## 5. When

| Wave | When | What | Owner |
|---|---|---|---|
| **0 Contract** | Nov-Dec 2026 | Management decisions by 2026-11-30 (sponsor, X1-X5, owners). Start X1 (intake) and X2 (detection, shadow mode). Sonar required. Mutation Visible on 2026-12-15. Self-assessment in every pod. Go/No-Go with data. Quality owners named. Triage the 13 failing routing E2E scenarios. C-01, C-04, C-05 if approved. | Management; QA Architect; pod leads |
| **1 Prove** | Q1 2027 | X3 and X4 step 1 (pooled hotspot and bug-fix PRs). X5 with product owners. AI review pilot (C-03). Monthly pod review vs own baseline. Re-test the AI effect with a 90-day window. | QA Architect; VP quality review |
| **2 Block** | April 2027 | X3/X4 step 2. Review all experiments against controls. Quality model v1 with justified targets. Decide which gates block, per scope. Retire gates with no value. | Sponsor; VP quality review |
| **3 Spread** | H2 2027 | Spread proven gates to all pods. Decide on RIA agents, mutation blocking, AI review and the agent harness from evidence. | Sponsor |

## 6. Success by April 2027

- At least 80% of valid customer bugs record failure type, detected-by and cause (today: cause known for about 25%).
- At least 80% of pods have a quality owner and an owner map entry. Each of them sees its 8 metrics against its own baseline each month.
- At least one correctness type is detected by our monitors before customers.
- Experiments X1-X5 have results with confidence intervals. Only practices that beat their controls spread.
- Every blocking gate has a measured false-block rate and an owner.

## 7. Open before approval

| Item | Why it matters | Owner |
|---|---|---|
| Named sponsor and decision forum | "Sponsor" and "VP quality review" must be named people | Management |
| Effort per wave (pod time, QA&RM time, tooling) | No estimate yet; needed for the decision | QA Architect, with pod leads |
| Control pods for X1-X5 | Control pods change nothing but must share data | VP quality review |
| ServiceNow access (REQ0120210) | Blocks D2, D4, D5 per pod and the X2 outcome | QA Architect |
