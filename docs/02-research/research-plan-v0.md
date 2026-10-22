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

### Status 2026-10-22 and next items

| ID | Status / next item | Output |
|---|---|---|
| R1 | Done (round 1) | [Findings F1](findings-round-1.md#f1---trend-has-quality-declined-r1) |
| R1b | Explain throughput jumps (U-13): stories and bugs by project and creator for 2024-Q1, 2026-Q3 | Confounder log |
| R2 | Done (round 1) | [Findings F2](findings-round-1.md#f2---concentration-where-is-the-risk-r2) |
| R2b | Pilot short-list: CFB trend per team inside Orchestration Core and A&D; size of "stuck / lost contacts" theme across all years | Gate 3 input |
| R3 | Blocked: needs Git org access (U-09) | Hotspot list |
| R5 | Done (round 1, n=213) | [Findings F3](findings-round-1.md#f3---escape-causes-why-do-defects-reach-customers-r5) |
| R5b | Second-rater check on 40 RCAs; fill the 2026-01 to 2026-06 sample gap | Agreement rate |
| R6 | Controls inventory: for each check (RIA field, RCA field, EOR, Sonar, CI gates), record Suggested / Policy / Real control and fill rate | Controls map |
| R7 | AI attribution: sample 50 AI-labeled CFBs, find who applies the labels and what they mean (U-17) | AI label semantics |

### Status update 2026-10-22 (round 2)

| ID | Status / next | Output |
|---|---|---|
| R1b | Done | [F6](findings-round-2.md) |
| R2b | Done; pilot D-010 | [F9](findings-round-2.md) |
| R6 | Done | [F8](findings-round-2.md) |
| R7 | Done | [F7](findings-round-2.md) |
| R8 | **Next.** Extract causing keys from RCA of all fixed CFBs 2025-2026; CFB rate AI vs non-AI stories, by quarter and team | Gate 2 |
| R9 | **Next.** Pilot deep dive: all Orchestration Core CFB RCAs (W_last), escape-cause profile, routing flow components, incidents | Gate 4 input |
| R5b | Second rater on 40 RCAs + 2026-H1 sample | Agreement rate |
| R3 | Blocked: Git org access (pilot repos) | Hotspots |
| R10 | Story size / cycle time trend (U-19) | Denominator quality |

### Status update 2026-10-22 (round 3)

| ID | Status / next | Output |
|---|---|---|
| R8 | Done: RR about 1.0 | [F10](findings-round-3.md), [R8](r8-ai-vs-non-ai.md) |
| R9 | Done | [F11](findings-round-3.md), [R9](r9-pilot-orchestration-core.md) |
| R5b | Partial (Claude vs Claude 79%); human rater open (U-22) | F12 |
| R3 | **Next (unblocked, incl. monolith).** Churn x CFB hotspots for VCSvc (`inContact/inContact`), AFM, VFM, contact-retry, agent-capacity | Hotspot map |
| R11 | **Next.** Test PH-2: CFB timeline vs migration dates (VFM->AFM, Voltron, State Streams, .NET) | Migration impact |
| R12 | **Ready.** Candidates found (R12a, D-018); [questionnaire](../01-discovery/sme-validation-questionnaire.md) ready; needs lead to send | Gate 4 |
| R13 | **Next.** Gate 4 package: baseline metrics, constraints, success criteria draft | Gate 4 |
| R14 | Knowledge concentration (P-05) from Git ownership in pilot repos | Bus factor |

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

### Status update 2026-10-22 (round 4)

| ID | Status | Output |
|---|---|---|
| R3 | Done | [F14](findings-round-4.md), [R3+R14](r3-r14-hotspots-ownership.md) |
| R14 | Done | [F15](findings-round-4.md) |
| R11 | Done (Git dates only; Atlassian timed out) | [F16](findings-round-4.md), [R11](r11-migrations-vs-cfb.md) |
| R13 | Done v0: G4 NOT PASSED | [gate-4-readiness-v0](../03-decisions/gate-4-readiness-v0.md) |
| R12 | Waiting: lead to approve SMEs + send questionnaire | U-22 |
| R11b | Re-run Jira / Confluence migration dates when Atlassian responds | U-23 |
