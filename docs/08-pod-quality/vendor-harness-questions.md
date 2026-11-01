# Vendor Check - Harness.io: Fit to Our Gaps and Questions to Ask

**Date:** 2026-10-29 | **Status:** prep for vendor talks; no contact with Harness yet | **Parent:** [pod quality playbook](pod-quality-playbook.md), [gate catalog](gate-catalog.md)

**Method:** read the [Harness home page](https://www.harness.io/) and [docs index](https://developer.harness.io/docs/) on 2026-10-29. Deep docs and pricing were not read. All Harness capabilities and numbers below are **vendor claims (trust: LOW)** until a POC proves them on our data.

## 1. What Harness sells today

- Harness now presents its platform as "agents": Software Delivery Agent, Security Testing Agent, Runtime Protection Agent, Cost Management Agent.
- **Risk & Governance** sets agent autonomy levels (1-3), with OPA policy-as-code, RBAC, audit trails and human approvals.
- **SDLC Knowledge Graph** learns from builds, deployments, incidents and cost events.
- Several modules have new names (table below).

## 2. Our gaps vs Harness modules

| Our gap (evidence) | Harness name today | Their claim | Our gate |
|---|---|---|---|
| 96% of P1 found by customers | Deployments (Continuous Delivery) | Canary rollout, automatic check against baseline metrics | G6.1, G7.1 |
| Monolith cannot roll back | Feature Management & Experimentation (from Split, 2024) | Feature flags, A/B tests, stale-flag clean-up | G5.2, G6.1 |
| Flaky and slow test signal; routing E2E 1.2% pass | Builds | Agent selects the tests a change needs | G4.5, G4.6 |
| Race and scale escapes 13-23% | Resilience Testing (Chaos Engineering) | Fault injection | G5.3 |
| No metrics per team | AI DLC Insights (was SEI) | Engineering metrics | G8.3 |
| AI code security (40-45% flawed samples) | Security Testing Orchestration, AI SAST, AI SCA | Scans in the pipeline, fewer false positives | G4.3 |
| Go/No-Go pages "TBD" | Risk & Governance | OPA policies, approvals, audit | G5.1 |
| Paved road for pods | Developer Portal, templates | Golden paths, self-service | P-14 |
| No team-service-code map (U-27) | SDLC Knowledge Graph | Shared delivery context | C3 |

## 3. Their claimed results (vendor, LOW trust)

| Customer | Claim |
|---|---|
| United Airlines | 20 templates replaced thousands of pipelines. Deploys 75% faster. 70% less manual effort. |
| Citi | Release time from days to 7 minutes. 20,000 engineers. |
| Morningstar | 50 templates replaced 36,000 scripted pipelines. Builds from hours to minutes. |
| Platform scale | 5.7M deployments and 1.5T+ flag evaluations per month. |

These are speed and scale results. None is a quality result (escaped bugs, incidents, detection).

## 4. Questions to ask Harness

**A. Fit with our setup**
1. Can you deploy our legacy monolith with toggles, not rollback?
2. Must we move off GitHub Actions to use your agents?
3. Can each pod keep its own pipeline and still pass one central policy?
4. Do you support our stacks: C#, Java, PHP, Playwright?

**B. Detection and deployment quality (main gap)**
5. Which monitoring sources does the canary check read?
6. Can the canary check read business signals, such as routing correctness or report data?
7. What false-alarm rate do customers see? Show measured data.
8. Can a failed check stop a canary and switch off a flag automatically?

**C. Gates and policies**
9. Can a gate start as "visible" and become "blocking" per team or code path?
10. Can policies read Sonar, Jira and ReportPortal data?
11. Do you log gate exceptions, with reason and approver?
12. Can a test suite block only while its pass rate stays healthy?

**D. Tests**
13. What is the miss rate of test selection? How do you prove the skipped tests were safe?
14. How do you handle flaky tests: detection, quarantine, owner?

**E. Metrics and data**
15. Can AI DLC Insights show customer-found bugs per team, not only DORA metrics?
16. Can the Knowledge Graph build our team-service-code map? What data does it need?
17. Can we export all raw data to our own database?

**F. AI agents and security**
18. What can an agent do at each autonomy level? Who approves at each level?
19. What data leaves our network? Where is it stored, and for how long?

**G. Proof and cost**
20. Show a customer result for escaped bugs or incidents, not only speed.
21. Give 3 references with a monolith and more than 100 teams.
22. What is the cost per pod and per module?

## 5. Proof to ask for (POC on our data)

| Test | Pass rule (proposed) |
|---|---|
| Replay 6 months of our P1 incidents through the canary check | It flags at least some incidents before the customer case |
| Run our routing E2E suite with test selection and flaky detection | It separates product failures from environment failures |
| One T1 service behind flags and a canary | A bad canary is stopped by the tool, not a person |
| Load our Jira and GitHub data into AI DLC Insights | Our 8 metrics (D1-D8) per pod can be shown |

## 6. Risks

- **Lock-in:** many modules add value only together.
- **Overlap:** we already use GitHub Actions, Sonar, Aikido, Xray and ReportPortal.
- **Tool vs gap:** our main gaps are the test signal and intake data. A tool does not fix a broken signal or missing bug fields.
- **Agent autonomy:** agents that act in the pipeline must follow P-07 (a human is accountable) and P-08 (agent output is untrusted).

## Sources

- [Harness home](https://www.harness.io/)
- [Harness docs](https://developer.harness.io/docs/)
- [Harness acquires Split](https://www.harness.io/press-and-news/harness-acquires-split-software-to-enhance-feature-management)
- [SD Times on Split](https://sdtimes.com/cicd/harness-announces-plans-to-acquire-feature-management-company-split-software/)
