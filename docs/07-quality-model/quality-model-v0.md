# Quality Model v0 (draft)

**Date:** 2026-10-25 | **Status:** draft for review; experiments come before any rollout | **Evidence:** [definition v1](../06-reassessment/quality-definition-v1-draft.md), findings [round 1](../06-reassessment/m2-findings-round-1.md) and [round 2](../06-reassessment/m2-findings-round-2.md), [why numbers changed](../06-reassessment/why-numbers-changed.md)

## 1. Principles

1. **Outcome first.** Quality = customers run their business on the product correctly and without interruption, and do not find our defects for us. Engineering signals explain outcomes; they are not quality.
2. **Risk-based.** Requirements scale with the impact of the failure type and the code area, not with team size or tool choice.
3. **Common where variation adds no value; different where risk differs.** Teams differ strongly in impact (incidents per bug 1.1-10.4) and intake noise (invalid 6-79%), mostly inside the same VP.
4. **No invented thresholds.** Each team is compared with its own 2025 baseline and with control teams. Fixed targets come only after experiments.
5. **Means are open.** Tests, RIA, Sonar, mutation testing, agents and gates are options to compare, not requirements.

## 2. Dimensions, metrics and decisions

Baseline = 2025 Jan-Oct vs 2026 Jan-Oct, MI-investigation tickets excluded (D-032).

| Dim | Metric | Decision it supports | Evidence needed | Baseline 2025 -> 2026 | Limits | Owner |
|---|---|---|---|---|---|---|
| D1 Business correctness | Valid correctness CFBs (DATA, ROUTING, LIFECYCLE, RECQM, AGENTSTATE, WFM, BILLING), severity-weighted | Where to invest first; which areas get risk-based requirements | Jira CFB + failure-type label | 295 -> 325 (+10%); P1/P2 share 52% -> 70% | Customer-reported only; billing rarely reported | Product area owner |
| D2 Availability | P1 / major incidents per quarter, affected customers | Reliability investment; release risk | ServiceNow records (U-26) | P1 customer channel about 150 -> 76 per quarter (C-08 open) | Counts only today | SRE / NOC |
| D3 Performance | Performance-type CFBs; SLO breaches | Capacity and performance work | Jira; SLO data (not accessed) | Jira PERF 50 total | No SLO data | Service owner |
| D4 Detection | Share of impact first found by us (monitoring, tests) vs customers | Monitoring investment; release go/no-go | ServiceNow "detected by", alert links | P1 opened via customer case: 96% | Intake channel is not first observer | SRE + team |
| D5 Recovery | Time to restore (P1/MI); time to fix valid CFB | Response capacity; escalation rules | ServiceNow, Jira | P1 71% < 4 h; CFB fix median 10 days (both years) | Resolve time is not restore time | Team + SRE |
| D6 Change safety | Fix-caused share of known causes; emergency-change share; recent-change share | Review depth for fixes; release policy | causal links, ServiceNow changes | Fix-caused 23.5% -> 27.1%; emergency x2.9 from 2026-06; recent-change 28% -> 41% | Cause known for ~25% of CFBs | Team + release mgmt |
| D7 Non-recurrence | Recurrence after fix; reopen rate | Whether fixes hold | Jira, similarity pairs | Recurrence 3.9% -> 1.2-1.6%; reopen 5.2% -> 5.6% | Similarity model, single rater | Team |
| D8 Expectation fit | Reports closed as works-as-designed / not a bug that are real requirement or documentation gaps | Requirement and documentation work | Jira closures + sample review | About 25% of reports closed this way; 42.5% of them real gaps | n=40 sample | Product manager |

**Data-quality signals (not quality, but needed to trust the metrics):** invalid share per team, MI separation, cause-link rate, Jira key in commits, team-to-service map.

## 3. The model: common baseline, risk-based layer, team adaptation

### 3a. Common baseline (all teams)

These items are common because they make outcomes **measurable and comparable**, or because the practice is already uniform.

| Requirement | Why common (evidence) |
|---|---|
| One intake rule: MI investigations, defects and expectation gaps are separate types | The mix error inflated the headline by 44% of growth (D-032) |
| Each valid CFB records: failure type, detected-by, causing change (when known), affected customers | Cause known for ~25% only; detected-by not recorded; who-affected unknown |
| RCA for valid P1/P2 CFBs | Already 80-100% in every team (no change needed) |
| Team -> service -> repo map, kept current | Does not exist (F20); blocks team comparison |
| Monthly view of D1-D8 per team vs its own baseline | Teams differ too much for one shared target |

### 3b. Risk-based layer (applies by failure type and code area, in any team)

| Risk trigger (evidence) | Requirement level rises for |
|---|---|
| Correctness failure types with high severity: ROUTING (73% P1/P2), DATA, LIFECYCLE, AGENTSTATE (11 incidents per CFB) | Change review, test evidence for the affected behavior, detection before customers |
| Hotspot code (top directories by CFB-fix density) | Change size and review depth (follow-up fixes 21% -> 54% with PR size in hotspots; flat elsewhere) |
| Bug fixes on correctness types | Review and regression evidence (1 in 4 known causes is a fix) |
| Emergency changes | After-the-fact review rate and cause link (x2.9 from 2026-06) |

These apply to **all authors, human or AI**: AI is not riskier per change (matched RR 0.78-0.84, n.s.), but AI PRs are larger and go more into hotspots (5% -> 47%).

### 3c. Team / POD adaptation (by archetype, re-assessed quarterly)

| Archetype (teams) | What varies | Why |
|---|---|---|
| A. High impact (9) | More depth on detection (D4) and recovery (D5) | Incidents per CFB and P1/P2 share above median |
| B. Fast growing (8) | First check re-homing; then intake triage and capacity | Part of growth is team renames and splits |
| C. High noise (5) | Intake and expectation-gap work (D8) before defect work | Invalid share >= 50% |
| D. Stable (18) | Common baseline only | No signal that more control adds value |

Teams choose **how** to meet a requirement (tools, tests, review practice). The model fixes **what** must be true and how it is measured.

## 4. Decision rules

| Rule | Trigger | Action (decision, not a fixed solution) | Decider |
|---|---|---|---|
| R1 | A team's D1 or D2 is outside its own 2025 monthly range for 2 consecutive months | Investigation with RCA sampling | VP quality review |
| R2 | A risk trigger (3b) shows a rise vs control teams in an experiment | Extend the experiment's practice to similar teams | QA architect + VP |
| R3 | Data-quality signal fails (e.g. cause link or detected-by missing) | Fix intake before reading the outcome trend | Team lead |
| R4 | Archetype changes at quarterly review | Change the adaptation set | VP quality review |

## 5. Improvement options (all levers)

| Lever | Option | Evidence for the need | Dims | Strength |
|---|---|---|---|---|
| Requirements | Close expectation and documentation gaps; spec links for risky stories | ~15% of reports are hidden expectation gaps; causing stories link specs less (6.8% vs 31.8%) | D8, D1 | Medium |
| Architecture | Order-tolerant state and data-correctness invariants in routing / lifecycle / reporting data | Correctness = 46% of valid CFBs; state races in pilot | D1, D7 | Medium |
| Knowledge | Owner backups for hotspots; team-service map | Bus factor 1-2 on densest code; no map | D1, D5 | Medium |
| Review | Review depth scaled to change size in hotspots, for all authors | Size-risk curve in hotspots | D6, D1 | Medium |
| Delivery | Fix safety: review and regression evidence for fixes; emergency-change follow-up | 1 in 4 causes is a fix; emergency x2.9 | D6 | Low-Medium |
| Operations | Detection by monitoring for top correctness types | 96% of P1 via customer channel | D4, D5 | Medium (intake proxy) |
| Testing | Trustworthy E2E signal; tests for escaped scenarios | Untested scenarios 28-31%; routing E2E passes 1.2% | D1 | Medium |
| Intake / data | MI and expectation-gap separation; cause and detected-by fields | Headline error D-032; cause known ~25% | all | High |

## 6. Experiments before rollout

> **Revised 2026-10-25 after a power check:** single-team, one-quarter arms cannot detect realistic effects for X2-X5. See [experiment protocols v0](experiment-protocols-v0.md) (pooled teams, high-volume primary measures, stepped start).

Each experiment runs for 1 quarter with a control (similar archetype teams that do not change) or a pre-period, and has a stop rule. Success = a difference vs control whose confidence interval excludes no-effect, or a clear pre/post change with the control flat.

| # | Hypothesis | Where | Metric | Control | Stop rule |
|---|---|---|---|---|---|
| X1 | Intake rule + required fields make D1-D8 trustworthy | 3 teams (one per archetype A, B, C) | Share of valid CFBs with failure type, detected-by, cause | Other teams | 2 of 3 teams report the fields as a blocker at retro |
| X2 | Monitoring for one correctness type finds issues before customers | 1 archetype-A team (routing or lifecycle) | D4 share detected by us; time to detect | Same team pre-period | No detection after 6 weeks of shadow mode |
| X3 | Size-scaled review in hotspots lowers follow-up fixes | 2 teams with hotspot code | 90-day follow-up fix rate per PR (all authors) | 2 matched teams | Merge time doubles with no fix-rate change |
| X4 | Fix-safety review lowers fix-caused defects | 2 teams with high fix-caused share | Fix-caused share of new CFBs | 2 matched teams | No change after 1 quarter |
| X5 | Expectation-gap triage lowers repeat reports | 1 archetype-C team | Repeat "works as designed" reports per topic | Same team pre-period | Product backlog cannot absorb |

## 7. Open before v1

- U-26 ServiceNow record read: who was affected, change -> incident links, D2/D4/D5 per team.
- Human validation (no SMEs so far): failure-type labels and archetypes need a team check.
- C-08: explain the fall in ServiceNow P1s.
- Team -> service -> repo map (U-27) for practice data beyond the pilot.
