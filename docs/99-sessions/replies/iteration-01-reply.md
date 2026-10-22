# Iteration 1 - Research Reply (verbatim)

**Date:** 2026-10-22 | Reply to [initiative brief](../../00-charter/initiative-brief-original.md). Repo was empty at this time.

---

## 1. Mission Understanding

- Goal: find real quality problem before any solution design.
- Product: legacy monolith + newer services + growing AI-assisted dev.
- Core concern: change rate > ability to understand, test, review, release safely.
- Must prove or disprove quality decline with baseline + trend, not perception.
- Must locate risk concentration (code, flow, team, boundary).
- Must separate causes: legacy complexity, architecture, process, test gaps, knowledge gaps, AI use.
- Every claim classified (FACT/HYPOTHESIS/UNKNOWN...), with source, confidence, invalidation criteria.
- Gates 0-4 control progress. No solution design before Gate 4.
- Output = decision-ready research package, not tooling plan.
- This session = discovery only. No code, no integrations.

## 2. Initial Risks and Ambiguities

| # | Type | Item |
|---|---|---|
| 1 | FACT | Repo empty (no README, no docs, no branch). Nothing to read. All context must come from you. |
| 2 | UNKNOWN | Which product/domain? "CXone" too wide. Which monolith? Which services? |
| 3 | UNKNOWN | Who perceives decline? Since when? Compared to what period? |
| 4 | UNKNOWN | Definition of "quality": escaped defects? MIs? CFBs? Regressions? Rollbacks? Customer complaints? No definition = no Gate 2. |
| 5 | HYPOTHESIS risk | AI attribution hard. Git usually does not mark AI-written code. AI adoption likely coincides with other changes (headcount, cadence, reorg). Correlation not cause. |
| 6 | ASSUMPTION | Signals exist: your vault notes CFBs, MIs, OLA, Power BI dashboards, RIA/PIA, XCX Quality Process. Not verified for this scope. |
| 7 | UNKNOWN | Sponsor, decision owner, deadline, what "done" means. |
| 8 | Risk | Data sensitivity. Incident/customer details in GitHub repo (even private) may break policy. Need rule on what may be committed. |
| 9 | Risk | Bias: repo name "factory" + existing agent/mutation tooling push toward automation. Conflicts with "no solution first". Watch it. |
| 10 | Risk | 11 v0 docs without evidence = paperwork theater. Propose thin docs, placeholders, each must enable a decision. |

## 3. What I Need to Inspect

| Source | What | My access (not tested yet) |
|---|---|---|
| Jira | Bug/CFB/MI counts per month 24+ mo, severity, component, escape phase, reopen rate, cycle time | Atlassian MCP available. Need project keys. |
| Confluence | Architecture, ADRs, postmortems/RCAs, QA strategy, XCX process, role page | Atlassian MCP available. Need space keys. |
| Xray | Test-to-requirement trace, automated vs manual ratio, execution trend | Likely via Jira. Not confirmed. |
| Git | Churn hotspots, ownership concentration, PR size, review depth, reverts | gh works for Guy-nice. Org repos unknown. |
| Sonar | Coverage/complexity/duplication/reliability trend | Unknown. No connector. |
| CI/CD | Failure rate, flaky/rerun/skipped tests, deploy freq, rollbacks | Unknown. Which system? |
| Power BI | CFB/OLA/regression dashboards | MCP present, needs auth |
| Observability/incidents | MIs, SLOs, change-linked incidents | Unknown (ServiceNow? Datadog?) |
| AI usage | Tools, teams, since when, adoption data | Unknown. Likely survey or tool admin telemetry. |
| SMEs | Hidden rules, dependencies, "only X knows" areas | Interviews |

## 4. Stakeholder Questions - Round 1

**Blocking (Gate 0):**

| # | Question | Why | Enables |
|---|---|---|---|
| Q1 | Which product/domain/monolith in scope? What is explicitly out? | Without boundary, research unbounded. | Charter scope |
| Q2 | Who is sponsor and decision owner? What decision will they make with output, and by when? | Output format depends on decision. | Success criteria, timeline |
| Q3 | What exact signal triggered this concern (incident, metric, exec remark, customer escalation)? When? | First traceable Observed Signal -> Evidence. | Problem statement v0 |
| Q4 | Data rule for this repo: may it hold Jira keys, incident summaries, customer names? | Compliance gate for all evidence capture. | Evidence handling |
| Q5 | May I run read-only queries against Jira/Confluence now? Which project/space keys? | Gate 1 needs real access check. | Access inventory |

**Useful, not blocking:** Q6 Which metric does leadership trust today (Power BI CFB view?), known defects in it? Q7 Is AI-tool usage tracked (licenses, telemetry, PR labels)? Since when, which teams? Q8 Which 3-5 SMEs know the monolith best? Any single point of failure? Q9 Existing quality initiative this must align with / not duplicate?

## 5. Proposed Discovery Deliverables

Repo has no structure, so use brief structure: `README.md`; `docs/00-charter/` (initiative-charter, problem-statement-v0, glossary); `docs/01-discovery/` (stakeholder-questionnaire, discovery-map, evidence-access-inventory, unknowns-and-assumptions-register); `docs/02-research/` (research-plan-v0, source-analysis-plan); `docs/03-decisions/` (decision-log, research-gates). Rule for all: every unknown has owner, source, action, "blocks decision: Y/N". Source refs as `[SRC-xxx]` placeholders until real evidence. No invented facts.

## 6. Proposed Research Gates

| Gate | Pass criteria | Status |
|---|---|---|
| G0 Charter | Q1-Q4 answered; scope, exclusions, sponsor, outcome documented | OPEN (blocked on Q1-Q4) |
| G1 Access | Each source: available / partial / none, with permissions and limits | OPEN |
| G2 Problem | Quality defined; >= 1 trend metric with 18-24 mo baseline; decline confirmed or rejected with confidence | OPEN |
| G3 Scope | 1 bounded flow/domain selected by defect density + churn + business impact | OPEN |
| G4 Solution ready | Root-cause hypotheses validated; baseline metrics fixed; constraints + success criteria agreed | OPEN |

Minimum evidence before solution design: (1) agreed quality definition; (2) defect/escape trend with baseline; (3) hotspot map for pilot (churn x defects x ownership); (4) test effectiveness for pilot (escaped defects vs existing coverage); (5) AI-usage data or explicit statement that attribution is impossible; (6) >= 2 root-cause hypotheses tested against counter-evidence.

## 7. Recommended First Action

1. You answer Q1-Q5 (closes Gate 0).
2. Then I run read-only Jira query: bug/CFB/MI counts per month, 24 mo, per component, in scoped project. Cheapest test of "has quality declined?" + shows concentration = first pilot candidate.
3. Pilot selection criteria (propose now, pick after data): highest escaped-defect density, high churn, crosses legacy/modern boundary, business-critical.

## 8. Approval Request

Approve:
- **A.** Clone repo to `~/ai-quality-discovery-factory`, create the 12 docs v0 (thin, placeholders), initial commit to `main`. No push without your OK.
- **B.** Read-only Jira/Confluence probes after you give project/space keys (Q5).

Plus answers to Q1-Q5. Highest-value first: **Q1 - which product/domain is in scope?**
