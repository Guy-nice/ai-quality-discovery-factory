# Management Report - Quality Gates for Pods and AI

**Date:** 2026-10-28 | **Evidence:** 40 teams, Jan 2025 - Oct 2026 | **Deck:** [offsite deck](offsite-deck.pptx) | **Status:** proposal for decision

Every claim below links to its evidence file.

## 1. In one line
Customers find our worst bugs before we do. Fix the measuring first, then the gates.

## 2. What happened
- Serious bugs (P1/P2) up 49%. All customer bugs up 13%. [Brief](../00-brief.md), [why numbers changed](../06-reassessment/why-numbers-changed.md)
- Customers find 96% of P1 incidents first. [Impact](../06-reassessment/m2-impact-servicenow.md)
- 46% of valid bugs: the product does the wrong thing (data, routing). [Failure types](../06-reassessment/m2-failure-types.md)

**Simple view:** not more bugs. Worse bugs. And we are blind to them.

## 3. Why
- Almost no gate blocks a change. Go/No-Go pages show "TBD". [Current gates](../06-reassessment/current-gates-2026-10-25.md)
- Routing E2E tests passed 1.2% of runs. Nobody trusts them. [E2E trust](../04-solutions/so3a-e2e-trust.md)
- Teams differ 10 times in incidents per bug. [Teams](../06-reassessment/m2-teams.md)
- Follow-up fixes: 21% (small PR) to 54% (large PR), in hotspot code only. [Hotspots and owners](../02-research/r3-r14-hotspots-ownership.md), [delivery](../06-reassessment/m2-e7-delivery.md)
- AI is not riskier per change. AI makes more and larger changes. [AI vs non-AI](../02-research/r8-ai-vs-non-ai.md), [AI PRs](../02-research/r16-ai-prs.md), [dose-response](../02-research/r15-ai-dose-response.md), [AI in the model](../06-reassessment/m2-e9-ai.md)

## 4. Proposal: 3 layers
1. **Contract (all pods):** same bug types, same bug fields, same 8 metrics, owners.
2. **Risk floor (blocks):** only where data shows risk. Hotspot PR rules, Sonar check, feature toggle, test linked to each escaped bug, Go/No-Go with data.
3. **Free means:** each pod picks structure, tools, agents.

**Rule:** gate checks evidence, not tools. **AI rule:** same gates for human and AI.

**How pods use it:** [pod quality playbook](../08-pod-quality/pod-quality-playbook.md) (policies, pod capabilities, SDLC stages S0-S8), [gate catalog](../08-pod-quality/gate-catalog.md) (every gate, mode now and target), [pod self-assessment](../08-pod-quality/pod-self-assessment.md).

Detail: [quality model v0](../07-quality-model/quality-model-v0.md), [DoD v2](dod-v2-evidence-based.md), [hotspot PR rules](../04-solutions/drafts/hotspot-pr-rules.md), [escape-to-test](../04-solutions/so2-escape-to-test.md), [owners and PR rules](../04-solutions/so4-so5-owners-pr-rules.md)

## 4b. What outside research says (2024-2026)
- AI is an amplifier. Small batches and platform quality decide the payoff (DORA 2025).
- More AI adoption links to lower delivery stability (DORA 2024).
- Experienced developers were 19% slower with AI but felt faster (METR 2025). Measure outcomes, not opinion.
- About 40-45% of AI code samples had security flaws. Keep the security scan blocking.
- Agent-made tests work when tools filter them before a human accepts (Meta).
- No outside data shows that blocking gates beat advisory gates in autonomous teams. So: prove before block.

Detail and trust levels: [outside research](../08-pod-quality/external-research-2024-2026.md).

## 5. Eight metrics (each pod vs its own baseline)
D1 Correctness, D2 Availability, D3 Performance, D4 Detection, D5 Recovery, D6 Change safety, D7 Non-recurrence, D8 Expectation fit.
Definitions and baselines: [quality model v0, section 2](../07-quality-model/quality-model-v0.md). Recurrence: [D7](../06-reassessment/m2-d7-recurrence.md). Expectation gaps: [D8](../06-reassessment/m2-e8-requirements.md).

## 6. Timeline
- **Now:** bug fields, Sonar required, mutation score visible only.
- **Q1 2027:** experiments X1-X5 with control pods.
- **April 2027:** decide what blocks. Then spread to all pods.

Detail: [action plan v1](action-plan-v1.md), [experiment protocols](../07-quality-model/experiment-protocols-v0.md)

## 7. Decisions needed
1. Agree the 3-layer model.
2. Name one owner per pod.
3. Volunteer pods for experiments.
4. Dec 15 mutation gate: visible first, block later (D-040). [Decision log](../03-decisions/decision-log.md)

## 8. Risks and limits
- Owner map missing (U-27).
- No expert check of labels yet.
- ServiceNow data pending (REQ0120210, U-26). [Servicenow request](../01-discovery/servicenow-access-request.md)
- Research covers 40 teams, not all pods.
- Outside sources (DORA 2025 summary, vendor blogs) are opinion, not measured evidence.
