# Research Plan v0

**Version:** v0 | **Date:** 2026-10-22 | **Status:** Draft, pending Gate 0

## 1. Phases

| Phase | Goal | Main activities | Exit gate |
|---|---|---|---|
| P0 Charter | Shared mission, scope, sponsor | Round 1 questions (Q1-Q9), charter v1 | Gate 0 |
| P1 Access | Know what evidence exists and can be read | Read-only probes per source, field completeness checks, data handling rule | Gate 1 |
| P2 Problem definition | Confirm or reject decline with data | Quality definition; 24-month trend (R1); confounder check; problem statement v1 | Gate 2 |
| P3 Risk and scope | Locate concentration; pick pilot | Defect Pareto by component (R2); churn x defect hotspots (R3); pilot selection | Gate 3 |
| P4 Deep dive (pilot) | Validate root-cause hypotheses in pilot | Escape analysis, test effectiveness, review depth, AI attribution, SME interviews, RCA review | Gate 4 |
| P5 Solution options | Only after Gate 4 | Options with trade-offs, linked to confirmed problems | Decision |

## 2. First research items

| ID | Question | Method | Source | Output | Depends on |
|---|---|---|---|---|---|
| R1 | Did escaped defects / incidents rise? | Monthly counts, 24 months, normalized by release or change volume | SRC-001, SRC-007, SRC-008 | Trend chart + confidence | Q1, Q5, U-05 |
| R2 | Where do defects concentrate? | Pareto by component / module / service | SRC-001 | Pareto table | R1 |
| R3 | Which code areas are hotspots? | Churn x complexity x defect-linked commits | SRC-004, SRC-005 | Hotspot list | Repo access |
| R4 | Is decline a measurement artifact? | Check workflow, field, and severity rule changes over period | SRC-001, interviews | Confounder log | R1 |

## 3. Pilot selection criteria (Gate 3)

Pilot area = one bounded business flow or domain. Score candidates on:

| Criterion | Weight (draft) |
|---|---|
| Escaped-defect / incident density | High |
| Business criticality | High |
| Code churn | Medium |
| Crosses legacy-modern boundary | Medium |
| Evidence availability | Medium |
| SME availability | Low |

Pilot is selected from R2 / R3 data, not in advance.

## 4. Minimum evidence before solution design (Gate 4)

1. Agreed, measurable quality definition.
2. Defect / escape trend with baseline, normalized, confounders checked.
3. Hotspot map for pilot (churn x defects x ownership).
4. Test effectiveness data for pilot: where escaped defects occurred compared with existing coverage.
5. AI-usage data for pilot, or explicit statement that attribution is impossible.
6. At least 2 root-cause hypotheses validated against counter-evidence.
7. Documented constraints (compliance, cost, CI duration) and success criteria.

## 5. Risks to the research

| Risk | Mitigation |
|---|---|
| Access delays | Start with sources already connected (Jira, Confluence). |
| Measurement artifacts | R4 before root-cause work. |
| Confirmation bias toward AI or tooling | Each hypothesis has explicit rejecting evidence. |
| Paperwork without decisions | Each doc must enable a named decision. |
