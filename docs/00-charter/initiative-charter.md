# Initiative Charter

**Version:** v0 (draft) | **Date:** 2026-10-22 | **Gate:** 0 - OPEN | **Owner:** Guy Guterman (QA Architect)

## 1. Purpose

Build an evidence-backed understanding of the software quality problem, and of where risk concentrates, before designing any operating model, tooling, agents, gates, or controls.

## 2. Background

Statements below are from the initiative brief. None is verified with data yet.

| ID | Statement | Class |
|---|---|---|
| C-01 | Product combines a large, old, sensitive legacy monolith with newer services and integrations. | ASSUMPTION (from brief) |
| C-02 | AI-assisted development usage is increasing. | ASSUMPTION (from brief) |
| C-03 | Software quality is perceived to have declined. | HYPOTHESIS |
| C-04 | System knowledge is incomplete, distributed, or concentrated in few people. | HYPOTHESIS |
| C-05 | The organization may change software faster than it can understand, validate, and release it safely. | HYPOTHESIS (central) |

## 3. Research questions

1. What is the quality problem, exactly?
2. Did quality decline? How do we prove or disprove it?
3. Where is risk concentrated?
4. What is the contribution of legacy complexity, architecture, delivery process, test gaps, knowledge gaps, and AI-assisted development?
5. What evidence is missing?
6. What must be investigated before solution design?
7. Later, after Gate 4 only: what operating model, tests, gates, metrics, and controls to propose.

## 4. Scope

| In scope (domains) | Status |
|---|---|
| Business and customer impact | Planned |
| Quality decline and defect patterns | Planned |
| Legacy complexity and architectural debt | Planned |
| Legacy / modern boundaries and dependencies | Planned |
| Requirements quality and traceability | Planned |
| Test coverage, effectiveness, reliability | Planned |
| Delivery workflow, review, release controls | Planned |
| Existing signals: Sonar, Xray, CI/CD | Planned |
| Production reliability, incidents, defect escape | Planned |
| AI-assisted development usage and impact | Planned |
| Ownership and knowledge concentration | Planned |
| Constraints: compliance, privacy, cost, CI duration, readiness | Planned |

**Product / system boundary:** UNKNOWN (U-01). Blocks Gate 0.

## 5. Exclusions (Phase 1)

- Solution design, tool selection, configuration (Sonar, Xray, mutation testing, RIA, agents, dashboards, quality gates).
- Implementation or integration code.
- Changes to production systems or to shared tool configuration.
- Write operations in Jira, Confluence, Git, or CI/CD.

## 6. Stakeholders

| Role | Name | Interest | Status |
|---|---|---|---|
| Initiative lead / QA Architect | Guy Guterman | Owner of research | Confirmed |
| Sponsor / decision owner | UNKNOWN (U-02) | Decision on output | Open |
| Engineering leadership | UNKNOWN | Delivery, code health | Open |
| Product | UNKNOWN | Customer impact, priorities | Open |
| Architecture | UNKNOWN | Boundaries, debt | Open |
| SRE / Operations | UNKNOWN | Incidents, reliability | Open |
| Security / Compliance | UNKNOWN | Data handling, AI policy | Open |
| QA leads | UNKNOWN | Test maturity, process | Open |
| SMEs (monolith) | UNKNOWN (U-08) | Hidden rules, history | Open |

## 7. Expected outcomes

- Decision-ready research package: confirmed problem statement, risk map, baseline metrics, validated root-cause hypotheses, constraints, success criteria.
- Then solution options with trade-offs, after Gate 4.

**Decision the package supports:** UNKNOWN (U-02). Blocks Gate 0.

## 8. Success criteria for the research (draft)

- Quality defined in measurable terms and agreed by the sponsor.
- Decline confirmed or rejected with stated confidence.
- At least one bounded pilot area analyzed end to end.
- Every major conclusion traceable to sources.

## 9. Timeline

UNKNOWN (U-02). To be set after the sponsor confirms the decision date.

## 10. Change history

| Version | Date | Change |
|---|---|---|
| v0 | 2026-10-22 | Initial draft from initiative brief |
