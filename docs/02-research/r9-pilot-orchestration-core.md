# R9 - Pilot Deep Dive: Orchestration Core (Contact Routing and Lifecycle)

**Date:** 2026-10-22 | **Decision:** D-010 | **Gate:** input to G4 | **Rater:** claude-fork-r9 (single rater)
**Data:** `data/db/quality.sqlite` (tables `issues`, `flow_tags`, `rca_class` round R9, `confluence_pages`, `git_repos`, `jql_counts`, `agg_r9_*`), `data/aggregates/r9-pilot-*.csv`
**Scripts:** `scripts/db/r9_flow.py`, `r9_rca_show.py`, `r9_rca_load.py`, `r9_metrics.py`, `r9_extra.py`

## 1. Scope and data

| Item | Value |
|---|---|
| Population | CFB (`issuetype = Bug and salesforceAssociatedTypes is not EMPTY`) with R&D VP = Orchestration Core, created >= 2024-10-22 |
| Rows loaded | 466 CFB (W_prev 170, W_last 296), all fields + issue links; RCA/RIA text in `raw_local.sqlite` only |
| Extra rows | 50 Orchestration Core Epics resolved 2026 (Xray link check) |
| RCAs classified | 108 of 113 fixed W_last CFB ("Fixed" + "Fixed - Config"); 5 had no usable RCA |
| Windows | W_prev = 2024-10-22..2025-10-21; W_last = 2025-10-22..2026-10-22 |

## 2. Sub-flow profile (W_last)

Tagger: rules on labels + summary (`r9_flow.py`). Precision on 2 random samples of 30: sub-flow exact 24/30 (80%) both times; in-flow vs out-of-flow 28/30 (93%).

| Sub-flow | W_prev | W_last | Change | P1/P2 | Incidents avg | 5+ incidents | Median days to fix | Invalid |
|---|---|---|---|---|---|---|---|---|
| **All Orchestration Core** | 170 | 296 | +74% | 70% | 3.8 | 19% | 9 | 42% |
| **In-flow scope (routing + lifecycle)** | 123 | 218 | +77% | 71% | 3.7 | 17% | 12 | 44% |
| routing/skill/queue | 39 | 58 | +49% | 67% | **7.1** | **26%** | **28** | 47% |
| stuck/lost contact | 12 | 57 | **+375%** | 70% | 1.9 | 12% | 10 | 49% |
| ACD/contact state | 22 | 40 | +82% | 68% | 3.4 | 18% | 5 | 58% |
| IVR/Studio script | 16 | 27 | +69% | 74% | 1.6 | 7% | 9 | 30% |
| digital routing | 18 | 22 | +22% | 82% | 2.5 | 18% | 11 | 27% |
| dialer/outbound | 8 | 9 | +12% | 67% | 6.2 | 33% | 22.5 | 44% |
| transfer/conference | 8 | 5 | -38% | 100% | 1.2 | 0% | 17.5 | 20% |
| admin/config/API (out of flow) | 36 | 39 | +8% | 59% | 2.1 | 18% | 5 | 28% |
| reporting/dashboard (out of flow) | 4 | 15 | +275% | 67% | 7.3 | 40% | 5 | 27% |
| other (out of flow) | 7 | 24 | +243% | 79% | 4.8 | 25% | 6 | 54% |

Invalid = Duplicate, Not a bug, Cannot Reproduce, Works as Designed.

- **EVIDENCE (High):** Growth is in the flow (+77%), not in admin/config (+8%).
- **EVIDENCE (High):** Routing/skill/queue CFBs carry the most customer impact: 7.1 incidents per CFB, 26% with 5+ incidents, median 28 days to fix.
- **EVIDENCE (High):** Stuck/lost contact CFBs rose 12 -> 57. Confluence shows scheduled cleanup automation and a resolved-swarm log where many root causes are "unknown" (SRC: 3873800676, 4256301562, 4252663877). The response treats the symptom, not the cause.
- **EVIDENCE (High):** 42% of W_last CFBs close as invalid (Duplicate 45, Not a bug 57). This is triage load, and it hides the real defect rate.

## 3. Team profile (W_last, teams with >= 8 CFB)

| Team | W_prev | W_last | Change | P1/P2 | Incidents avg | Invalid |
|---|---|---|---|---|---|---|
| Orchestration II | 18 | 66 | +267% | 48% | 2.5 | 62% |
| Orchestration | 31 | 58 | +87% | 86% | 3.7 | 47% |
| Advanced Omnichannel Routing | 23 | 40 | +74% | 78% | **7.9** | 45% |
| ACD Admin Pune | 3 | 31 | +933% | 71% | 1.8 | 13% |
| Advanced Omnichannel Routing II | 9 | 24 | +167% | 62% | 2.6 | 71% |
| ACD Admin Bolivia | 47 | 12 | -74% | 25% | 3.1 | 17% |
| EM Force | 4 | 13 | +225% | 92% | 2.2 | 23% |

- **EVIDENCE (Medium):** ACD Admin Bolivia -> Pune is a work transfer (rename / re-homing), not a quality change. Combined: 50 -> 43.
- **EVIDENCE (Medium):** Orchestration II and AOR II have 62-71% invalid CFBs. These teams get many tickets that are not defects.

## 4. Escape-cause profile: pilot vs other VPs

| Escape cause | Pilot (n=108) | Pilot in-flow (n=72) | Other VPs, R5 (n=180) |
|---|---|---|---|
| missing test coverage | 27.8% | 29.2% | 27.2% |
| **scale/performance/concurrency/race** | **25.9%** | **29.2%** | 10.6% |
| deployment/release process | 9.3% | 9.7% | 7.8% |
| environment/config/data difference | 9.3% | 6.9% | 7.2% |
| requirements/spec gap | 8.3% | 4.2% | 7.2% |
| regression from recent change (RIA miss) | 7.4% | 11.1% | 16.1% |
| legacy/unknown behavior | 7.4% | 5.6% | 2.2% |
| unclear/not stated | 2.8% | 1.4% | 9.4% |
| third-party/integration/dependency | 0.9% | 1.4% | 6.1% |
| monitoring gap | 0.9% | 1.4% | 2.2% |
| test existed but ineffective | 0.0% | 0.0% | 3.9% |

Other: introduced by a specific recent change 48/108 (44%); regression = yes 35/108 (32%); legacy named 22/108 (20%); AI named as cause 0/108. Prevention: test added 41, process change 36, code fix only 23, none 5, monitoring 3.

- **EVIDENCE (Medium):** Race / ordering / scale escapes are 2.4x more frequent in the pilot (26%) than in other VPs (11%). In-flow: 29%.
- **EVIDENCE (Medium):** Legacy is named in 20% of pilot RCAs vs 11% in round 1. The VC monolith (VCSvc, ScriptHelper, stored procedures) recurs.
- **EVIDENCE (Medium):** Only 3 of 108 prevention actions add monitoring, but 1 of 108 escapes is classified as a monitoring gap. Several MI RCAs say customers detected the problem first (e.g. ORC-52995: "discovered via customer complaint, no internal alert").

## 5. Second-rater check (partial R5b)

33 keys were classified in R5 (round 1) and R9 (independent read, no access to R5 labels during reading).

| Column | Agreement |
|---|---|
| escape_cause | 26/33 = 79% |
| regression | 29/33 = 88% |
| prevention_action_type | 32/33 = 97% |
| introduced_by, legacy_mentioned, ai_mentioned | 33/33 = 100% |

**Limit:** both raters are the same model family. This is not human inter-rater reliability. A human SME check on 20 RCAs is still needed.

## 6. Architecture and components (from Confluence only)

| Component | Type | Source |
|---|---|---|
| VC / VCSvc (Virtual Cluster: COR, IVR, AGM servers, ScriptHelper, WebScripting, stored procedures) | **Legacy monolith** (C#/.NET, T-SQL, NCache). Not found in GitHub; RCAs cite TFS changesets. | RCA text (API-21286, ORC-52345, ORC-53647); SRC 4150689943 |
| VFM (app-findmatch) | **Legacy** matching service (Scala/Akka/Kinesis), still live | SRC 4076208133 |
| AFM (routing-ng-advanced-findmatch) + State Aggregator, Blender, Match Distributor, Contact Retry, Agent Capacity | **New** Routing NG services (Java, Kafka Streams, Aurora) | SRC 1903493964, 1903363038, 4076339502 |
| Entity Management (orch-entity-*) | **New** services (Go) | SRC 4029218838 |
| State Streams transformers | **New** Flink pipeline (EM, VC, DFO events -> dashboards) | SRC 3631251647 |
| Telephony Feature Service (TFS) | **New**, replacing VC telephony features (draft) | SRC 4041444339 |

**Parallel changes in 2026 (EVIDENCE, High):** all of these touch the same contact lifecycle at the same time:
- VFM -> AFM migration (per-BU `afmEnabled` flag);
- Voltron DB decoupling and cache conversion (NCache, MessagePack) cluster by cluster;
- State Streams KDA -> EKS (one-way repo forks; un-ported changes cause silent divergence);
- .NET runtime upgrades of the monolith (.NET 8/10, netstandard2.0) with serializer and library swaps;
- tenant migration between clusters.

**Test evidence (EVIDENCE, High, SRC 4072866234):** Findmatch Testing Gap Analysis (2026-08-27) found 35 gaps (3 critical):
- AFM unit tests are strong, but there is no integration test with a real Kafka broker or DB, and no concurrency test for the optimistic-claim retry;
- of 141 Playwright E2E blocks, 32 are `fixme` and about 38 are conditionally skipped. About half of the suite is not guaranteed to run;
- CI does not report skip counts;
- the AFM chaos plan (32 tests) shows "NOT STARTED" (SRC 4086694457);
- a latency injection of 50 ms for 10 min cut matches by about 60% (SRC 4231365389).

## 7. Xray and Git status

| Item | Result |
|---|---|
| Xray Tests created, pilot projects (ORC, AAD, AOR, EM, VOL, API, ACDWF) | 2025: 4,034; 2026 to 10-22: 5,160 |
| Xray Test Executions, same projects | 2025: 54,131; 2026 to 10-22: 46,804 |
| Orchestration Core Epics resolved 2026 with a direct Test link | **1 of 50** (2%). Tests may link to Stories, not Epics (not checked). |
| Orchestration Core Epics resolved 2026: RIA filled / AI-implemented | 22 of 59 (37%) / 10 of 59 (17%) |
| GitHub org `inContact` | **Read access confirmed.** R3 hotspot analysis is unblocked for the services. |
| Commits last 12 months | AFM 254, agent-capacity 222, contact-retry 182, blender 97, match-distributor 90, resolver 36, VFM 20; E2E repo 1,294; integration-tests 312 |
| VC monolith source | **Not in GitHub.** Probably TFS. R3 for the monolith needs TFS / Azure DevOps access (UNKNOWN). |

Caveat: the pilot project list also holds non-Orchestration-Core work (AAD, EM, API are shared).

## 8. Root-cause hypotheses for the pilot

| ID | Hypothesis | Evidence | Confidence | Could invalidate |
|---|---|---|---|---|
| PH-1 | **Distributed state races.** The contact lifecycle is split across many async producers (VC, EM, State Aggregator, AFM/VFM, Contact Retry) with no ordering guarantees. Out-of-order, dropped or late events leave contacts stuck or misrouted. Tests do not model concurrency. | 26% race/ordering escapes vs 11% elsewhere (29% in-flow); RCAs AOR-13256, AOR-13364, AOR-15089, EM-146033, VOL-8004, VOL-8376, ORC-53647; gap analysis: no concurrency or real-broker tests; stuck CFBs ×4.75 | **Medium-High** | Human SME re-rating moves race cases to other causes; stuck rise explained by a dashboard-only data issue |
| PH-2 | **Parallel migration load.** Five concurrent migrations of the same lifecycle (VFM->AFM, Voltron, KDA->EKS, .NET upgrades, tenant moves) create dual-path states and regressions faster than tests and runbooks cover them. | 2026 migration pages; RCAs AOR-13252 (BU migration left stale state), EM-161952 (wrong runbook step), EM-158368 (connector upgrade), API-19816/21286/21358/21509/22840/22976 (library swaps); 10 of 108 escapes are deployment/runbook | **Medium** | CFB growth timing does not match migration waves per cluster (test with cluster x month) |
| PH-3 | **Monolith modernization without behavior-parity tests.** Library and serializer swaps in the VC monolith (.NET 8/10, netstandard, Newtonsoft, MessagePack) change behavior. There is no side-by-side comparison and few unit tests in legacy code. | 11 RCAs (10%) cite library/runtime swaps; repeated "no side-by-side comparison", "missing unit tests in legacy code"; legacy named in 20% | **Medium** | The modernization escape count stays flat or falls while modernization continues |
| PH-4 | **Production conditions are not reproducible before release.** Scale, real Kinesis/Kafka, failover, customer-specific scripts and large BUs exist only in production. | ENV + SCALE = 35% of pilot escapes; RCAs EM-158368, ORC-51343, SCRX-1394, ORC-54317, ORC-52995; 50 ms latency test: -60% matches | **Medium** | Perf/chaos runs (not started) show that pre-prod catches these classes |
| PH-5 | **Detection is customer-first.** Monitoring prevention is rare (3/108). Stuck contacts are handled by cleanup jobs and swarms, not by alerting on the cause. | Prevention mix; ORC-52995, EM-158691 (synthetic-only alerting); cleanup automation pages | **Medium** | SRE alert data shows internal detection before the customer case for most MIs |

AI-assisted code: 0 of 108 RCAs name AI as a cause. 39 W_last pilot CFBs carry AI labels, which mark AI fixes (F7). The pilot RCAs give no evidence for or against AI as a cause. See R8 for the causal-link comparison.

## 9. Open gaps before Gate 4

1. **R3 hotspots:** use GitHub access (now confirmed) for churn x CFB-linked commits on AFM, contact-retry, agent-capacity, blender. Request TFS access for the VC monolith.
2. **Human SME check:** 20 pilot RCAs, rated by an Orchestration Core architect (real R5b).
3. **PH-2 test:** CFB by cluster x month against the Voltron / AFM migration schedule (SRC 4232414340, afmEnabled history).
4. **Incident data:** MI list for the pilot from the incident system (SRC-008) to check incident load beyond the Jira "Number of Incidents" field.
5. **Xray at Story level:** test links on pilot Stories (the Epic-level link rate is 2%).
6. **Invalid triage cost:** 42% invalid. Measure the time spent on invalid CFBs per team.
7. **Baseline metrics for G4:** in-flow CFB per month, P1/P2 share, incidents per CFB, stuck-contact CFB count, race-class escape share.

> **Correction 2026-10-22:** The VC monolith is in GitHub (`inContact/inContact`, migrated from TFS, history from 2021). Statements above that it is "not in GitHub" are wrong. See [findings-round-3 correction](findings-round-3.md#correction-2026-10-22-iteration-9).
