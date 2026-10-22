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

## 2. Assumptions

| ID | Assumption | Risk if false | Validation | Owner | Status |
|---|---|---|---|---|---|
| A-01 | Jira holds defect history for at least 18-24 months with usable fields. | No trend baseline | Count query per month, field completeness check | Guy | Not validated |
| A-02 | Defect classification practice was stable over the period. | False trend | Check workflow / field change history, ask QA leads | Guy | Not validated |
| A-03 | AI-assisted development is in use and increasing. | H-11 moot | Q7, license data | Eng. leadership | Not validated |
| A-04 | A legacy monolith and newer services are separable in repos / components. | Cannot locate risk by architecture | Repo and component mapping | Architecture | Not validated |
| A-05 | Read-only access to core sources is available to the research. | Research blocked | Gate 1 probes | Guy | Not validated |

## 3. Contradictions

| ID | Contradiction | Sources | Status |
|---|---|---|---|
| - | None recorded yet | - | - |
