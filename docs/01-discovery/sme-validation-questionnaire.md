# SME Validation Questionnaire - Pilot (Orchestration Core, contact routing and lifecycle)

**Version:** v0 | **Date:** 2026-10-22 | **Research item:** R12 | **Closes:** U-22 | **Gate:** G4
**Time:** about 45 minutes per person. Async. **Respondents:** see [stakeholder list](../../data/aggregates/r12-stakeholders.csv).

## Why we ask

Customer-found bugs (CFB) in the contact routing and lifecycle flow went up 77% in 12 months (123 -> 218). We have 5 hypotheses from Jira RCAs and Confluence. The RCAs are written by the owning teams, and an AI model classified them. We need an independent human check before we design any solution.

## Part A - Hypotheses (about 20 min)

For each hypothesis, answer: **Agree / Partly / Disagree / Do not know**, then give the reason, and what evidence would prove you right.

| ID | Hypothesis |
|---|---|
| PH-1 | Many CFBs come from **distributed state races**: events between VCSvc, Entity Management and the routing services (AFM/VFM, contact-retry, agent-capacity) arrive out of order or are dropped. There are no tests that model concurrency or real Kafka / Kinesis streams. |
| PH-2 | **Parallel 2026 migrations** change the same contact lifecycle at the same time: VFM -> AFM, Voltron decoupling, State Streams KDA -> EKS, .NET upgrades, tenant moves. Their interaction is not tested. |
| PH-3 | **Library / serializer / runtime swaps** in the VC monolith (.NET 8/10, netstandard, Newtonsoft, MessagePack) change behavior. There are no side-by-side parity tests. |
| PH-4 | **Production conditions cannot be reproduced before release**: scale, real streams, failover, customer Studio scripts, tenant data shape. |
| PH-5 | **Customers detect problems first.** Teams rarely add monitoring or alerts after a CFB (3 of 108 RCAs). |

Questions:
1. Which hypothesis, in your view, explains the **largest** share of CFBs in this flow? Why?
2. Do concurrency, contract or parity tests exist for this flow that we did not find? Where (repo / pipeline / Xray)?
3. Give the **dates** of the main 2026 migration steps (VFM -> AFM cutovers, Voltron, State Streams EKS, .NET upgrades, tenant moves).
4. Which code areas or services do you think are the most fragile? Who knows them best?
5. Is there a cause we missed? Example: on-call load, team changes, site moves, release cadence.

## Part B - Rate 20 RCAs (about 25 min, blind)

Read the RCA field of each Jira issue. Choose **one** primary escape cause. Do not discuss with other raters.

Escape causes: `requirements/spec gap` · `missing test coverage` · `test existed but ineffective` · `regression from recent change (RIA miss)` · `environment/config/data difference` · `third-party/integration` · `scale/performance/concurrency/race` · `legacy/unknown behavior` · `deployment/release process` · `monitoring gap` · `unclear/not stated`

| # | Issue | Your escape cause | Regression? (Y/N/?) | Comment |
|---|---|---|---|---|
| 1 | API-22976 | | | |
| 2 | AAD-50039 | | | |
| 3 | API-21156 | | | |
| 4 | AAD-49124 | | | |
| 5 | AAD-47259 | | | |
| 6 | AAD-38815 | | | |
| 7 | VOL-8004 | | | |
| 8 | AOR-13364 | | | |
| 9 | AAD-41021 | | | |
| 10 | ORC-52995 | | | |
| 11 | ORC-47954 | | | |
| 12 | AOR-13252 | | | |
| 13 | AAD-38750 | | | |
| 14 | AAD-52910 | | | |
| 15 | SCRX-1394 | | | |
| 16 | EM-136404 | | | |
| 17 | AAD-40189 | | | |
| 18 | AAD-51086 | | | |
| 19 | EM-148596 | | | |
| 20 | AAD-51863 | | | |

Sample: stratified random (seed 20261022) from 108 classified pilot RCAs (`rca_class` round R9). The AI labels are kept hidden from raters, and the answer key is in the DB.

## How results are used

- Part A: each hypothesis is marked Confirmed / Weakened / Rejected in the problem statement. Disagreements are recorded as CONTRADICTION.
- Part B: agreement rate (human vs AI) per column. If agreement on escape cause is below 70%, the escape-cause percentages are reported as Low confidence.
- Answers are stored in `docs/01-discovery/sme-answers/` and in the DB (`sme_answers`).
