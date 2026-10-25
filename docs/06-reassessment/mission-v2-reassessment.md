# Mission v2 - Reassessment of Existing Research

**Date:** 2026-10-25 | **Trigger:** mission clarification from lead (iteration 17) | **Status:** assessment only, no new solution design

## 1. Mission restatement

Understand the current state of product quality. Find where and why quality problems happen, and who they affect. Recommend evidence-backed, risk-based actions that fit different teams and PODs. Quality starts from customer outcomes, business correctness and operational impact. Tools (Xray, RIA, Sonar, mutation testing, agents, gates) are possible means, not requirements.

## 2. Assessment of existing research

### Supports the mission (keep)

| Item | Evidence | Confidence |
|---|---|---|
| Customer-found bug trend and severity (F1, F6, F13) | 11,662 CFBs; 2026 rise; import correction; valid vs invalid | High |
| Concentration by domain (F2) | VP level; 3 VPs = 60% | High |
| Escape-cause profile from RCAs (F3, F11, F12) | 321 classifications; Claude raters only | Medium |
| AI analysis (F7, F10, R15, R16) | Label meaning, per-change ratio, PR comparison | Low-Medium |
| Existing controls usage (F8) | Field fill rates, Go/No-Go pages | High |
| Code hotspots, ownership, CI health (F14, F15, SO-3A data) | Git, PRs, CI runs | Medium |
| Research DB with query log | Reproducible base | High |

### Where the work became solution-led (reclassify as provisional)

| Output | Problem |
|---|---|
| G4 "passed (interim, data-based)" | Passed with no human validation. AI raters only; RCAs are self-reported. |
| Solution options SO-1..SO-6, wave 1, gates G1-G7 | Designed from one pilot domain. One gate set for all teams. This conflicts with "one workflow does not fit every team". |
| Numeric thresholds (400 lines, >= 95% E2E, <= 9 CFB/month, >= 50% detection, bus factor >= 3) | Partly invented. Only the PR-size curve has data behind it, and its cut point is still a judgment. |
| Management deck and summary recommendations | Present provisional options as recommendations. |
| Quality definition (D-006) | CFB count = Salesforce-linked bugs. A proxy of customer-reported defects; 30-51% invalid; it misses customer impact, correctness and operations. |

### Still unknown

See section 3.

## 3. Most important evidence gaps

| # | Gap | Why it matters | Source (access) |
|---|---|---|---|
| E1 | **Customer and operational impact**: incidents/MIs, outage minutes, SLA/SLO breaches, affected tenants, escalations | Quality must start from outcomes, not bug counts | ServiceNow CXone (connector exists, needs auth), Salesforce cases, SLO data |
| E2 | **Who was affected**: customers, tiers, regions per failure | "Who was affected" not answered | Salesforce case links, incident records |
| E3 | **Detection and recovery**: who found it, time to detect, time to restore | Why controls did not detect | Incidents, alerts, NOC runbooks |
| E4 | **Business correctness failures** (data, reporting, billing, routing correctness) | A&D is the largest domain (27%) and was not studied | A&D CFBs + RCAs, data-quality incidents |
| E5 | **Team/POD variation**: practices and outcomes per team | Needed to separate common vs team-specific requirements | Team map, Jira workload (timed out), Git/PR/CI per team |
| E6 | **Human validation** of causes and classifications | All causal claims rest on AI classification of self-reported RCAs | 3-5 SME interviews, human rating |
| E7 | **Delivery and release data**: deploy frequency, change failure rate, hotfixes, rollbacks | Change failure rate is a direct outcome signal | CI/CD, release notes, hotfix tracker |
| E8 | **Requirements quality**: acceptance criteria gaps, late changes | Only RCA text so far (7%) | Epic/Story history, PM interviews |
| E9 | **AI causal evidence**: practices, review, exposure time | Current results are correlational, short exposure | Team surveys, 90-day follow-up, matched team comparison |

## 4. Next investigation steps (no solution design)

1. **Quality definition v1 (draft for review):** dimensions from customer outcome, business correctness and operational impact; map each to available evidence. Needs lead and sponsor input.
2. **Impact data:** connect incidents/MIs to CFBs, customers and domains (E1-E3).
3. **Failure case studies:** the 10-15 highest-impact events of 2025-2026 across at least 3 domains: what happened, who was affected, contributing factors, why controls missed it (E1-E4).
4. **Team/POD profiles:** outcomes and practices per team, to see real variation (E5).
5. **AI evidence upgrade:** classify observed facts, correlations and causal hypotheses; matched team comparison; plan the 90-day re-test (E9).
6. **Human validation:** 3-5 SME interviews plus a human rating of a sample (E6).
7. **Reclassify outputs:** mark the solution docs, gates, thresholds and the deck as provisional hypotheses (D-030).

## 5. Focused questions for the lead

| # | Question | Blocks |
|---|---|---|
| Q-A | May the research use incident / MI data (ServiceNow CXone Prod)? Who can grant read access? | E1-E3 |
| Q-B | Which business-correctness failures matter most to customers (for example reporting data, billing, routing)? | E4, quality definition |
| Q-C | Where is the source of truth for teams/PODs and the services they own? | E5 |
| Q-D | Can 3-5 SMEs give 45 minutes each, or should research use only data? | E6 |
