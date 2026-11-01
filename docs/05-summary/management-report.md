# Management Report: Product Quality, Gates and Pods in the AI Era

| | |
|---|---|
| **Version** | 2.0 (supersedes 1.0 of 2026-10-28) |
| **Date** | 2026-11-01 |
| **Owner** | QA Architecture, QA&RM |
| **Audience** | Directors, VPs, architects, pod leads |
| **Status** | Proposal for management decision. D-042 and D-043 are proposals; D-038 is a draft. Nothing is applied in company systems (D-029). |
| **Evidence** | 40 teams, Jan 2025 - Oct 2026; 1,663 merged PRs in 13 pilot repos; outside research 2024-2026 |
| **Deck** | [Offsite deck, 17 slides](offsite-deck.pptx) |

Every claim links to its evidence. Each finding has a class (EVIDENCE, CORRELATION, HYPOTHESIS, UNKNOWN) and a confidence level.

**Terms:** *pod* = a development team (the data uses Jira team names). *Hotspot* = code directories with the most customer-bug fixes. *T1* = high-risk tier (routing, contact lifecycle, report data, agent state). *CFB* = customer-found bug. *Paved road* = ready-to-use tools and templates that QA&RM offers. Gate modes: *Advice* (not checked), *Visible* (shown on a dashboard), *Audit* (sample check), *Block* (required check).

---

## 1. Executive summary

1. **Quality fell in severity, not mainly in volume.** Severe customer-found bugs (P1/P2) rose 49%. All customer-found bugs rose 13%.
2. **Customer cases open 96% of P1 incidents.** ServiceNow P1 incidents also fell by about half per quarter; the cause is open (C-08).
3. **Today's gates do not protect us.** Almost no check blocks a change. Most 26.4 Go/No-Go pages show "TBD". The routing E2E suite passed 1.2% of runs.
4. **AI changes the load. We found no evidence that it is riskier per change.** AI PRs are about 3.7 times larger. Their share of hotspot PRs rose from 5% to 47%. In hotspot code, large PRs link to more follow-up fixes.
5. **Teams differ too much for one rule set.** Incidents per bug range from 1.1 to 10.4 between teams.

**Proposal:** one quality contract for every pod and a small blocking floor set by risk. Pods choose their own tools and agents. A gate blocks only after evidence shows that it helps.

**Decisions needed now:** see section 7 (5 decisions).

---

## 2. What happened (2025 vs 2026)

| Finding | Value | Class, confidence | Evidence |
|---|---|---|---|
| Severe customer-found bugs (P1/P2) | +49% (Jan-Sep 2026 vs 2025, MI tickets removed) | EVIDENCE, high | [Brief](../00-brief.md), [why numbers changed](../06-reassessment/why-numbers-changed.md) |
| All customer-found bugs | +13% | EVIDENCE, high | Same |
| P1 incidents that enter via customer cases | 96% | EVIDENCE (intake proxy), medium | [Impact](../06-reassessment/m2-impact-servicenow.md) |
| Valid bugs that are business-correctness failures (data, routing, contact lifecycle) | 46% | EVIDENCE, medium (labels not yet validated by experts) | [Failure types](../06-reassessment/m2-failure-types.md) |
| P1/P2 share of correctness bugs | 52% to 70% | EVIDENCE, medium | [Quality model, D1](../07-quality-model/quality-model-v0.md) |

**In plain words:** we do not have many more bugs. We have worse bugs, and we do not see them before our customers do.

---

## 3. Why it happened

| Cause | Evidence | Class, confidence | Source |
|---|---|---|---|
| Almost no gate blocks a change | Only security and PR-format checks block; Sonar is required in 1 of 5 pilot repos | EVIDENCE, high | [Current gates](../06-reassessment/current-gates-2026-10-25.md) |
| Release decisions lack data | Most 26.4 Go/No-Go pages show "TBD" (master page TBD) | EVIDENCE, high | Same |
| The test signal is not trusted | The routing E2E suite (VFM-AFM, 85 runs) passed 1.2% of runs; the same commit failed and passed in 50 of 66 retries | EVIDENCE, high | [E2E trust](../04-solutions/so3a-e2e-trust.md) |
| Large changes in hotspot code fail more | Follow-up fixes rise from 21% (small PR) to 54% (large PR), in hotspot code only | CORRELATION, medium (larger PRs also touch more files) | [Owners and PR rules](../04-solutions/so4-so5-owners-pr-rules.md), [hotspots](../02-research/r3-r14-hotspots-ownership.md) |
| AI changes the load; no evidence of more risk per change | Matched risk ratio 0.78-0.84 (confidence interval includes 1); AI PRs about 3.7x larger; AI share of hotspot PRs 5% (2025-Q4) to 47% (2026-Q4, partial) | CORRELATION, medium | [AI analysis](../06-reassessment/m2-e9-ai.md), [AI PRs](../02-research/r16-ai-prs.md) |
| One rule set for very different teams | Incidents per bug 1.1-10.4; invalid reports 6-79% | EVIDENCE, high | [Teams](../06-reassessment/m2-teams.md) |
| We cannot measure cause | Cause is known for about 25% of bugs; 9 of ~15 Jira quality fields are filled under 2% | EVIDENCE, high | [Quality model](../07-quality-model/quality-model-v0.md) |

---

## 4. What we propose

### 4.1 The model: three layers

| Layer | What | Who decides |
|---|---|---|
| **1. Contract** (every pod) | Same report types, same bug fields, same 8 metrics, named owners | QA&RM sets; every pod keeps |
| **2. Risk floor** (blocks only where data shows risk) | Hotspot PR rules, Sonar, security scan, feature toggles, test linked to each escaped bug, Go/No-Go with data | Level set by the risk of the change and code area, not the pod name |
| **3. Free means** | Structure, process, agents, test tools, review style | Each pod |

**Core rules:**
- A gate checks **evidence**, not the tool that made it.
- The same gates apply to every author: human, AI-assisted or agent.
- A human is accountable for every merged change.
- Every gate follows a lifecycle: Proposed, Visible, Block per scope (only with evidence), quarterly review, Retire.

Detail: [pod quality playbook](../08-pod-quality/pod-quality-playbook.md) (14 policies, 7 pod capabilities, AI rules), [gate catalog](../08-pod-quality/gate-catalog.md) (29 gates, stages S0-S8).

### 4.2 Gates along the SDLC (target mode)

| Stage | Blocks for all pods | Blocks for high-risk (T1) or hotspot changes |
|---|---|---|
| S0 Intake | Report type | - |
| S3 Review | Jira key | Size limit, code-owner review, test change |
| S4 CI | Build, Sonar, security scan, E2E only when healthy | - |
| S5 Release | Go/No-Go with data, feature toggle | Performance and chaos stage |
| S6 Deploy | Post-deploy sanity | Toggle-off verified, progressive rollout |
| S7 Operate | - | Correctness monitors (after experiment X2) |
| S8 Learn | Escaped bug closes with a test or a reason | - |

Most gates start as **Visible** and block only after evidence. Mode today: [gate catalog](../08-pod-quality/gate-catalog.md).

### 4.3 What every pod must have

Each pod needs 7 roles: a quality owner and a release owner. Code owners, with 2 or more per hotspot path. A 1-page test strategy, an AI working agreement and a production link. An owner for each failing test suite. These are roles, not job titles. Each pod checks itself every quarter with the [self-assessment](../08-pod-quality/pod-self-assessment.md).

**QA&RM role:** enabling (coaching), paved road (ready-to-use agents, templates, dashboards), governance (contract, gates, metrics, experiments).

---

## 5. What outside evidence says

### 5.1 Research 2024-2026

| Finding | Source | Trust | What it means for us |
|---|---|---|---|
| AI amplifies the existing system. Small batches and platform quality decide the payoff. | DORA 2025 | Medium | Contract first; a good paved road |
| More AI adoption links to lower delivery stability | DORA 2024 | Medium | Gate on change size and risk, not author |
| Experienced developers were 19% slower with AI but felt faster | METR 2025 (RCT, 16 developers) | High, small sample | Judge AI by outcomes, not opinion |
| About 40-45% of AI code samples had security flaws | Pearce et al. (2021); Veracode (2025) | High (older model); Low (vendor report) | Security scan stays blocking |
| LLM-made tests work when tools filter them before a human accepts | Meta TestGen-LLM | High | Agent output is untrusted until checked |
| No study shows blocking gates beat advisory gates in autonomous teams | Gap | - | Prove before we block |

Detail: [outside research](../08-pod-quality/external-research-2024-2026.md). Some numbers come from secondary sources. Verify them before you quote them in a decision paper.

### 5.2 How the Claude Code team reviews AI-written code (Anthropic, 2026-10-15)

- **Seven review layers:** checks before the PR, AI review, security review, CI, human approval by risk, merge queue with flags, fast rollback.
- **Their claimed result:** merged PRs more than doubled, while the share of reverted PRs fell over 40% (vendor self-report).
- **Agrees with us:** risk is set by the change, not the author. Agent approval never counts as a human approval.
- **Differs from us:** their model needs fast undo and internal detection. We have neither today. So we copy their method, not their goal of "one human per PR".
- **12 candidates, not applied (D-043).** Top 3 are low effort:
  - A PR template that asks how the change was tested, its risk and how to revert it.
  - An RCA field that names the gate that should have caught the escape.
  - A test set of past escapes, used to score any reviewer or vendor tool before rollout.

Detail: [side-by-side comparison](../08-pod-quality/compare-claude-code-review.md).

### 5.3 Vendor check: Harness.io

- Harness offers canary checks, feature flags (Split), test selection, chaos testing and AI agents. All of these are vendor claims.
- Their published customer results are about speed. None is about escaped bugs or incidents.
- **Before any decision:** run 4 proof tests on our own data. One example: replay 6 months of our P1 incidents through their canary check.

Detail: [Harness questions](../08-pod-quality/vendor-harness-questions.md).

---

## 6. How we measure: 8 metrics per pod

Each pod is compared with its own 2025 baseline, never with one shared target.

| # | Metric | Today (2025 to 2026) |
|---|---|---|
| D1 | Business correctness | P1/P2 share 52% to 70% |
| D2 | Availability | P1 via customer channel about 150 to 76 per quarter (cause open, C-08) |
| D3 | Performance | 50 performance bugs; no SLO data |
| D4 | Detection | 96% of P1 via customers |
| D5 | Recovery | 71% of P1 under 4 hours; bug fix median 10 days |
| D6 | Change safety | Fix-caused 23.5% to 27.1%; emergency changes x2.9 since June 2026 |
| D7 | Non-recurrence | Recurrence 3.9% to 1.2-1.6% |
| D8 | Expectation fit | About 25% of reports close as "works as designed"; 42.5% of those are real gaps (low confidence, sample of 40) |

**Rule:** a pod outside its own range for 2 months gets an investigation, not a punishment. Definitions: [quality model, section 2](../07-quality-model/quality-model-v0.md).

---

## 7. Decisions needed

**Who decides (proposed):** the VP R&D quality review, at the offsite. **Decide by (proposed):** 2026-11-30, so wave 0 can start in December.

| # | Decision | Recommendation | Ref |
|---|---|---|---|
| 1 | Adopt the 3-layer model and the gate lifecycle | Yes | D-042 |
| 2 | Name a quality owner per pod, plus an owner for the pod-service-code map | Yes, by end of November 2026 | Playbook C1, C3; U-27 |
| 3 | Approve experiments X1-X5, with volunteer pods and control pods | Yes; start X1 and X2 in November | D-038 |
| 4 | Mutation score on 2026-12-15 | Publish it in Sonar as Visible (non-blocking); block per scope only after evidence | D-040 |
| 5 | Start 3 low-effort items: PR template, "which gate" field in RCA, escape test set | Yes | D-043 |

---

## 8. Plan

| Wave | When | What | Exit rule |
|---|---|---|---|
| 0 Contract | Nov-Dec 2026 | Report type and bug fields (X1); Sonar required; mutation score Visible (2026-12-15); Go/No-Go with data; quality owners named; self-assessment done | 80% of pods have a quality owner, release owner and owner map entry |
| 1 Prove | Q1 2027 | Experiments X2-X5 with control pods; hotspot rules in X3 pods; monthly pod review | Results with confidence intervals |
| 2 Block | April 2027 | Gates that beat their control move to Block per scope; gates with no value retire | One logged decision per gate |
| 3 Spread | H2 2027 | Proven gates to all pods; paved road updated | Quarterly gate review in place |

Detail: [action plan v2](action-plan-v2.md), [experiment protocols](../07-quality-model/experiment-protocols-v0.md).

---

## 9. Risks and limits

| Risk or limit | Effect | Mitigation |
|---|---|---|
| Pod data covers 40 teams, not all pods | Results may not hold for every pod | Self-assessment and X1 extend coverage |
| No team-service-code map (U-27) | Weak per-pod comparison | Decision 2 |
| Failure types and pod types not validated by experts | Labels may be wrong | 3-4 expert reviews before wave 2 |
| ServiceNow per-team data pending (REQ0120210, U-26) | D2, D4, D5 per pod are counts only; X2 cannot confirm its outcome | QA Architect follows up the request ([request](../01-discovery/servicenow-access-request.md)); fallback: X2 uses alert-to-customer-case matching only |
| Proposed thresholds (400 lines, 14 days, 5% false blocks) | May be wrong for some pods | Set final values at the Visible stage and in experiments |
| Outside sources partly secondary or vendor | Overconfidence | Trust levels shown; verify before quoting |

---

## 10. Document map

| Need | Document |
|---|---|
| 1-page answer | [Brief](../00-brief.md) |
| What to do and when | [Action plan v2](action-plan-v2.md) |
| How pods work with quality | [Pod quality playbook](../08-pod-quality/pod-quality-playbook.md) |
| Every gate | [Gate catalog](../08-pod-quality/gate-catalog.md) |
| WIP DoD items, verdict by evidence | [DoD v2](dod-v2-evidence-based.md) |
| Quality model and experiments | [Model v0](../07-quality-model/quality-model-v0.md), [experiments](../07-quality-model/experiment-protocols-v0.md) |
| All decisions | [Decision log](../03-decisions/decision-log.md) |
| All summary files | [05-summary index](README.md) |

## Change log

| Version | Date | Change |
|---|---|---|
| 2.0 | 2026-11-01 | Review fixes (sources, overclaims, terms, dates); executive summary; class and confidence per claim; SDLC gate table; pod capabilities; outside research, Claude Code comparison and Harness check; 5 decisions; plan waves; risk table; document map |
| 1.0 | 2026-10-28 | First 1-page report with evidence links |
