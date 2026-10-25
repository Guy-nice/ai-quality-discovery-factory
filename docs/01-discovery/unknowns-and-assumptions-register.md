# Unknowns and Assumptions Register

**Version:** v0 | **Date:** 2026-10-22

## 1. Unknowns

| ID | Unknown | Owner (suggested) | Evidence source | Research action | Blocks | Status |
|---|---|---|---|---|---|---|
| U-01 | Product / domain / monolith / services in scope | Guy + sponsor | Stakeholder answer | Q1 | Gate 0 - Yes | Open |
| U-02 | Sponsor, decision owner, decision, deadline | Guy | Stakeholder answer | Q2 | Gate 0 - Yes | Open |
| U-03 | Triggering signal and date | Sponsor | Stakeholder answer, Jira, incident | Q3 | Problem statement v1 - Yes | Open |
| U-04 | Data handling rule for this repo | Security / Guy | Policy | Q4 | Evidence capture - Yes | Open |
| U-05 | Agreed definition of "quality" and baseline period | Sponsor + Guy | Workshop | Round 2 | Gate 2 - Yes | Open |
| U-06 | Jira project keys, Confluence space keys | Guy | Stakeholder answer | Q5 | Gate 1 - Yes | Open |
| U-07 | AI usage attribution method | Engineering leadership | Telemetry, license data, survey | Q7 | H-11 test - Yes | Open |
| U-08 | Key SMEs | Engineering managers | Stakeholder answer, Git ownership | Q8 | Interviews - No | Open |
| U-09 | Sonar, CI/CD, observability systems and access | DevOps / SRE | Stakeholder answer | Access request | Gate 1 - Partial | Open |
| U-10 | Trusted existing metric and its known defects | QA leadership | Power BI, stakeholder | Q6 | Baseline - No | Open |
| U-11 | Confounders: reorgs, tool migrations, cadence changes in period | Engineering leadership | Stakeholder, Jira history | Round 2 | Gate 2 - Yes | Open |
| U-12 | Overlapping initiatives | Guy | Stakeholder answer | Q9 | No | Open |
| U-13 | Cause of step jumps in stories resolved and all bugs (2024-Q1, 2026-Q3) | Jira admin / PMO | Jira by project and creator per quarter | R1b | Gate 2 - Yes | Open |
| U-14 | 2026 CFB trend with invalid resolutions excluded, after triage | Research | Jira | Re-run R1 in 2026-12 | Gate 2 - Yes | Open |
| U-15 | Customer base / usage growth for normalization | Product / Finance | Salesforce, usage telemetry | Request data | Gate 2 - No | Open |
| U-16 | Project re-homing map (AW, DE to CXDV, CSA?) | Jira admin | Jira project history | R2b | Gate 3 - No | Open |
| U-17 | Meaning of AI labels on bugs (AI caused vs AI fixed), who applies them | Eng. leadership / AI platform | Label owners, sample review | R7 | H-11 test - Yes | Open |

| U-18 | Location of XCX Quality Process doc | QA leadership | Confluence | Ask / search | No | Open |
| U-19 | Story size trend (AI work split into smaller stories?) | Research | Jira story points / cycle time | R10 | Gate 2 - No | Open |
| U-20 | Is the CI Sonar quality gate blocking? | DevOps | CI config | Access request | Gate 4 - Yes | Open |
| U-21 | TFS access for VC monolith source (hotspots, churn) | DevOps / Orchestration Core GL | TFS | Access request | Gate 4 - Yes | Open |
| U-23 | Production rollout dates (per cluster / BU) for AFM, Voltron, State Streams EKS, TFS, 26.1 | Orchestration Core / release management | SME, Confluence, Jira (timed out) | Questionnaire Q3; re-run R11 | PH-2 - Yes | Open |
| U-24 | Was the 2026-04 step caused by bug re-homing to Orchestration II? | Orchestration Core GL | Jira team history | Questionnaire Q6 | No | Open |
| U-25 | Detection source of pilot CFBs (alert vs customer) - PH-5 | SRE / NOC | Incident system, alert data | Access request | PH-5 - Yes | Open |
| U-22 | Human SME validation of PH-1..PH-5 and of 20 RCA classifications | Orchestration Core architects / QA lead | Interviews | R12 | Gate 4 - Yes | Open |

Partly closed 2026-10-22: **U-22** (data refutation R17 + blind rater 85%; human still needed for PH-2, PH-5). Closed 2026-10-22: **U-21** (monolith is in GitHub `inContact/inContact`, history from 2021; TFS not needed). **U-13** (imports ENG, CGY - F6). **U-17** (AI label = AI fix; attribution via cf_15229 - F7).

Status updates 2026-10-22: U-01, U-02 (scope part), U-05, U-06 handled by interim decisions D-005, D-006. They stay open for sponsor confirmation.

## 2. Assumptions

| ID | Assumption | Risk if false | Validation | Owner | Status |
|---|---|---|---|---|---|
| A-01 | Jira holds defect history for at least 18-24 months with usable fields. | No trend baseline | Count query per month, field completeness check | Guy | **Validated 2026-10-22:** CFB history from 2017. VP / Team usable; Component and Bug Type not. |
| A-02 | Defect classification practice was stable over the period. | False trend | Check workflow / field change history, ask QA leads | Guy | **Partly refuted:** invalid-CFB share varied 20-44% over time (U-14). |
| A-03 | AI-assisted development is in use and increasing. | H-11 moot | Q7, license data | Eng. leadership | Not validated |
| A-04 | A legacy monolith and newer services are separable in repos / components. | Cannot locate risk by architecture | Repo and component mapping | Architecture | Not validated |
| A-05 | Read-only access to core sources is available to the research. | Research blocked | Gate 1 probes | Guy | Not validated |

## 3. Contradictions

| ID | Contradiction | Sources | Status |
|---|---|---|---|
| C-01 | Absolute CFB and P1/P2 volume up (+51%, +72% H1 YoY) while CFB per resolved story down (-33% Q3 YoY). | SRC-001 | Open: depends on quality definition (U-05) |
| C-02 | Project-level CFB shifts (AW, DE down; CXDV, CSA up) look like re-homing, not quality change. | SRC-001 | Open: U-16 |
| C-03 | Jira EOR template: "Rollback not applicable for monolith". WIP DoD: "Deploy and rollback verified". | SRC-001, SRC-013 | Open |
| C-04 | AI labels on 9% of CFBs vs 0 RCAs naming AI as cause. | SRC-001 | Resolved: labels mark AI fix, not cause (F7) |
| C-05 | Go/No-Go template has 9 mandatory exit criteria; all 26.4 domain pages show "TBD". | SRC-002 | Open |
| C-06 | Jira has ~15 quality fields; 9 are under 2% filled. | SRC-001 | Open: policy vs practice |
| C-07 | Adjusted CFB per story +38% (2026-Q2 YoY), but AI vs non-AI RR about 1.0 in each quarter. | F6, F10 | Open: mix shift or system-level effect (PH-2) |

U-14 update 2026-10-22: pilot invalid share 35% -> 51%; valid in-flow CFB +34% (not +77%). D-020.

C-01 update 2026-10-22: weaker after import correction (F6). Q2 per-story +38%, Q3 -15%.

| C-08 | ServiceNow customer-channel P1 incidents fell ~50% in 2026 while Jira P1/P2 CFBs rose. | ServiceNow, Jira | Open: priority-rule change? |
| C-09 | 2026 CFB rise inflated by MI-investigation tickets (3 -> 128 in H1). | Jira | Resolved by D-032 |

| U-26 | ServiceNow read role (incident, problem, change_request records; service/CI grouping) | Lead / ServiceNow admin | ServiceNow | Access request | E1-E3, E6 - Yes | Open |
| U-27 | Maintained team -> service -> repo map | Engineering leadership | - | None exists (F20) | Team-specific model - Yes | Open |
