# Pod Quality Playbook - Quality and Gates for Pods in the AI Era

**Date:** 2026-10-28 | **Status:** proposal for management decision (D-042) | **Owner:** QA&RM | **Evidence:** internal research (40 teams, 2025-01..2026-10) + [outside research 2024-2026](external-research-2024-2026.md)

This playbook tells a pod **what must be true** for quality, and **how it is checked** at each SDLC stage. It does not tell a pod how to work. A pod chooses its own structure, process, agents and tools.

| Need | Go to |
|---|---|
| The rules in 1 page | Section 1 |
| What a pod must have | Section 3 |
| Gates per SDLC stage | Section 4 and [gate catalog](gate-catalog.md) |
| AI rules | Section 5 |
| Check your pod | [Pod self-assessment](pod-self-assessment.md) |
| Why (evidence) | [Management report](../05-summary/management-report.md), [outside research](external-research-2024-2026.md) |

## 1. The model in 1 page

**Three layers:**

1. **Contract (same for every pod).** Same bug types, same bug fields, same 8 metrics, named owners. It makes pods comparable.
2. **Risk floor (blocks only where data shows risk).** A small set of required checks. The level rises with the risk of the change and the code area, not with the pod name.
3. **Free means (pod choice).** Structure, process, agents, test tools, review style.

**Why this model (evidence):**

| Finding | Class | So the model |
|---|---|---|
| P1/P2 customer bugs +49%, all customer bugs +13% | EVIDENCE, high | Measure severity and detection, not raw counts |
| 96% of P1 incidents enter via customer cases | EVIDENCE (proxy), medium | Detection (D4) is a first-class metric |
| Teams differ 1.1-10.4 incidents per bug, mostly inside the same VP | EVIDENCE, high | One gate set for all fails; compare each pod with its own baseline |
| Follow-up fixes rise 21% to 54% with PR size, in hotspot code only | CORRELATION, medium | Size and review rules on hotspot paths, for every author |
| AI is not riskier per change (matched ratio 0.78-0.84, not significant) | CORRELATION, medium | No AI-only gate; same bar for all authors |
| AI PRs in hotspot code rose 5% to 47% | EVIDENCE, high | Hotspot rules catch the AI volume effect |
| Almost no gate blocks today; routing E2E passed 1.2% of runs | EVIDENCE, high | Fix the signal before it blocks |

**Outside evidence 2024-2026 ([detail](external-research-2024-2026.md)):**

| Outside finding | Source (trust) | So the model |
|---|---|---|
| AI is an amplifier: it makes strong systems stronger and weak ones weaker. Small batches and platform quality decide the payoff. | DORA 2025 (medium) | Fixed contract + small batches (G3.2) + a good paved road |
| More AI adoption links to lower delivery stability | DORA 2024 (medium) | Gate on change size and risk, not on author |
| High-AI teams: more PRs, much larger PRs, longer reviews, no org-level gain | Faros 2025 (low, vendor) | Same direction as our hotspot size finding |
| Experienced developers were 19% slower with AI but felt faster | METR 2025 RCT (high, small sample) | Measure AI value by outcomes, not by self-report (P-13) |
| About 40-45% of AI code samples had security flaws | Pearce et al. (high); Veracode (low, vendor) | Security scan stays in the blocking floor (G4.3, P-08) |
| Flaky tests hide real failures; mutation testing works at scale on changed code in review | Google (medium / high) | Flake budget and test health before blocking (G4.5); mutation Visible on changed code (G4.4) |
| LLM test generation works when tools filter output (build, pass, add coverage) before a human accepts | Meta TestGen-LLM (high) | Agent output is untrusted until checked (P-08, A6) |
| Stream-aligned teams, platform as a product, enabling teams | Team Topologies (low, framework) | QA&RM as enabling + platform + governance (section 3) |
| No independent data on blocking vs advisory gates in autonomous teams | Gap | Prove before block (gate lifecycle) |

## 2. Policies

| # | Policy |
|---|---|
| P-01 | **Same bar for every author.** Human, AI-assisted or agent-made: the same gates apply. |
| P-02 | **A gate blocks only where evidence shows risk.** All other checks are Visible or Advice first. |
| P-03 | **Gates check evidence, not tools.** A pod can meet a gate with any tool. |
| P-04 | **Every gate has an owner, a metric, a false-block rate, an exception path and a retire rule.** ([gate lifecycle](gate-catalog.md#3-gate-lifecycle)) |
| P-05 | **Each pod is compared with its own baseline and with similar pods.** Never one shared target before experiments set it. |
| P-06 | **No raw bug count as "the quality number."** Use valid, severity-weighted counts with MI tickets removed. |
| P-07 | **A human is accountable for every merged change.** An agent can write and review code. A named person approves it. |
| P-08 | **Agent output is untrusted input.** It passes the same security scan, tests and review as any code. |
| P-09 | **Tools must leave evidence in the common systems** (Jira, Xray, GitHub, Sonar, ReportPortal). If the evidence is not there, the gate counts it as missing. |
| P-10 | **Exceptions are allowed and logged.** A high exception rate starts a talk, not a penalty. |
| P-11 | **A pod outside its own range for 2 months gets an investigation** (rule R1), not a punishment. |
| P-12 | **Gates are reviewed each quarter.** Gates with no value are retired. |
| P-13 | **AI value is measured by outcomes** (follow-up fixes, escapes, lead time), not by developer opinion. |
| P-14 | **The paved road is a product.** QA&RM measures its adoption and fixes what pods avoid. A road that pods avoid is a QA&RM problem. |

## 3. What a pod must have (quality view)

A pod is free in structure. From the quality view, a pod must have these **capabilities**. They are roles, not job titles. One person can hold more than one role.

| # | Capability | What it means | Why (evidence) |
|---|---|---|---|
| C1 | **Quality owner** | One named person. Owns the contract, the monthly metric review and the exception log. Can be a developer. | No owner today for quality fields; 9 of ~15 Jira quality fields filled < 2% |
| C2 | **Release owner** | Brings data to Go/No-Go (G5.1). | 26.4 Go/No-Go pages mostly "TBD" |
| C3 | **Service and code ownership** | Pod -> service -> repo map entry. CODEOWNERS for its paths. At least 2 owners per hotspot path. | No org-wide map (U-27); bus factor 1-2 on hotspot code |
| C4 | **Test strategy (1 page)** | Which test levels, which tools or agents, how an escaped bug becomes a test. | Untested scenarios 28-31% of escapes |
| C5 | **AI working agreement** | Which agents the pod uses, who reviews agent output, how AI use is labeled (G2.2). | AI PRs larger and more in hotspots |
| C6 | **Production link** | Who gets alerts and incidents for the pod's services. Detected-by is recorded. | Incidents do not carry the owning dev team today |
| C7 | **Test-signal care** | A named owner for each failing suite, with a triage date (G4.6). | Routing suite failed every scheduled run for 6 months |

**QA&RM role toward pods (proposed):**

| Role | What QA&RM does | Does not do |
|---|---|---|
| **Enabling** | Coaching on test strategy, risk, hotspot work. Short engagements, then step back. | Own a pod's tests |
| **Platform (paved road)** | Offer agents, pipeline templates, dashboards and the gate checks as ready-to-use parts. | Force a pod to use them |
| **Governance** | Own the contract, the gate catalog, the metrics, the experiments and the Go/No-Go data. | Approve every release by hand |

The paved road must be the easiest way, not the only way. A pod that leaves the paved road keeps the same gates and must still leave the evidence (P-09).

## 4. SDLC stages and gates

Summary below. "Blocks" shows the **target** mode. Most gates start as Visible and block only after evidence. Mode today, IDs and evidence: [gate catalog](gate-catalog.md).

| Stage | What must be true | Blocks (all pods) | Blocks (T1 or hotspot) | Main metric |
|---|---|---|---|---|
| **S0 Intake** | Each report has a type; valid bugs have failure type, detected-by, cause | Report type (G0.1) | - | Cause-link rate; invalid share |
| **S1 Plan** | Acceptance criteria and spec link; state and toggle design for risky Epics | - | - (Audit) | D8 expectation fit |
| **S2 Build** | Tests come with the change; AI use is labeled | - | - | Test-file rate per PR |
| **S3 Review** | Jira key; hotspot size limit, code-owner review, test change | Jira key (G3.1) | Size, owner, test (G3.2-G3.4) | 90-day follow-up fix rate |
| **S4 CI** | Build, unit tests, Sonar, security scan; healthy E2E | Build, Sonar, scan (G4.1-G4.3); E2E when healthy (G4.5) | - | Suite pass rate, flaky rate |
| **S5 Release** | Data-based Go/No-Go; toggle registered | Go/No-Go with data (G5.1); toggle (G5.2) | Perf and chaos (G5.3) | Open P1-P3; D1-D8 trend |
| **S6 Deploy** | Progressive rollout; toggle-off verified; post-deploy sanity | Sanity (G6.2) | Toggle-off, progressive (G6.1) | Change-fail rate; D6 |
| **S7 Operate** | Correctness monitors; SLOs | - | Monitors after X2 (G7.1) | D4 detection; D2; D5 |
| **S8 Learn** | RCA for P1/P2; escaped bug gets a test; monthly review | Test link or reason on close (G8.2) | - | D7 non-recurrence |

**Tiers:**

| Tier | Assigned by | Extra gates |
|---|---|---|
| **T1 High risk** | Correctness-critical failure types (routing, contact lifecycle, report data, agent state); archetype-A pods; release-critical services | G1.2, G1.3, G3.5, G5.3, G6.1, G7.1, G7.2 |
| **T2 Standard** | All other pods and code | Contract + common floor |
| **Hotspot (per change)** | Change touches a hotspot path, in any tier | G3.2, G3.3, G3.4 |

## 5. AI in the SDLC

| Rule | Detail | Evidence |
|---|---|---|
| A1 Same gates for every author | No AI-only gate. | Matched ratio 0.78-0.84, not significant ([E9](../06-reassessment/m2-e9-ai.md)) |
| A2 Size and hotspot rules apply to AI output | AI makes larger changes and more of them in hotspots. | Hotspot share 5% to 47% |
| A3 Label AI-assisted PRs | For measuring only (G2.2). | AI effect could only be measured where AI use was visible |
| A4 Human approver for every merge | An agent can review. It cannot be the only approver. | P-07 |
| A5 Agents are means | Test-plan, Playwright, RIA, mutation and exploratory agents are Advice. They become gates only through the gate lifecycle. | Agents block nothing today; no escape evidence yet ([current gates](../06-reassessment/current-gates-2026-10-25.md)) |
| A6 Generated tests must prove value | An escape test must fail on the pre-fix code (quarterly audit sample). | Low-value tests are a known risk ([SO-2](../04-solutions/so2-escape-to-test.md)) |
| A7 Agent security | Agent output passes the security scan. Agents get least-privilege access to repos and data. | P-08; [outside research](external-research-2024-2026.md) |

## 6. Pods differ: depth by pod type

| Pod type | Pods (of 40 studied) | Focus | Why |
|---|---|---|---|
| A. High impact | 9 | Detection (D4), recovery (D5), T1 gates | Incidents per bug and P1/P2 share above median |
| B. Fast growing | 8 | Check re-homing first; then intake and capacity | Part of growth is renames and splits |
| C. High noise | 5 | Intake and expectation gaps (D8) before defect work | 50%+ of reports invalid |
| D. Stable | 18 | Contract and common floor only | No signal that more control helps |

Pod type is reviewed each quarter (rule R4). Source: [teams](../06-reassessment/m2-teams.md), [quality model 3c](../07-quality-model/quality-model-v0.md).

## 7. Roll-out

| Wave | When | What | Exit rule |
|---|---|---|---|
| 0 Contract | Nov 2026 | Report type and bug fields (X1); Sonar required; mutation Visible; Go/No-Go with data; pod quality owner named; self-assessment done | 80% of pods have C1-C3 |
| 1 Prove | Q1 2027 | X2-X5 with control pods; hotspot rules in X3 pods; monthly pod review | Results with confidence intervals |
| 2 Block | April 2027 | Gates that beat control move to Block per scope; gates with no value retire | Decision per gate, logged |
| 3 Spread | H2 2027 | Proven gates to all pods; paved road updated | Quarterly gate review in place |

## 8. Limits

- Pod-level data covers 40 teams, not all pods (UNKNOWN for the rest).
- No owner map (U-27). Failure types and pod types are not human-validated.
- ServiceNow per-team data is pending (U-26). D2, D4 and D5 per pod are counts only.
- Thresholds in this playbook (400 lines, 14 days, 5% false blocks) are proposed starting values. Experiments and the Visible stage set the final values.
