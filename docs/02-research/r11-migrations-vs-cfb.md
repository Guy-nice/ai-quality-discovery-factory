# R11 - 2026 Migrations vs Pilot CFB (PH-2)

**Date:** 2026-10-22 | **Hypothesis:** PH-2 | **Pilot:** Orchestration Core (D-010) | **Rater:** claude-fork-r11 (single rater)
**Data:** `quality.sqlite` tables `migration_events`, `migration_mentions`, `migration_causal`, `agg_r11_*`; script `scripts/db/r11_migrations.py`

## 1. Question

Do the parallel 2026 migrations in the contact lifecycle cause the growth of pilot CFBs? The migrations are VFM -> AFM, Voltron decoupling and cache conversion, State Streams KDA -> EKS, the VCSvc .NET / multi-TFM upgrade, tenant moves and TFS telephony.

## 2. Data limit (important)

- **Atlassian (Jira + Confluence) timed out on every call during R11.** No production rollout dates were pulled. No migration Epics were pulled.
- The event dates below come from **Git**: repo creation and the first commits of the work. They are **code-start dates, not production dates.** Confluence dates are "last modified" dates only.
- Production dates are a question for the SMEs (section 8).

## 3. Migration timeline (what we know)

| Event | Migration | Step | Date | Type | Source | Confidence |
|---|---|---|---|---|---|---|
| E01 | VFM -> AFM | AFM repo created | 2022-03-28 | code start | Git | High (code), Low (rollout) |
| E02 | Voltron / cache | MessagePack serializer work in VCSvc | 2026-01 (14 commits 2026-01..05) | code start | Git | Medium |
| E03 | .NET upgrade | net10 / multi-TFM work in monolith | 2026-03 (22 commits 2026-03..10) | code start | Git | Medium |
| E04 | TFS telephony | Telephony Feature Service repo created | 2026-04-08 | code start | Git | High (code) |
| E05 | Voltron / cache | voltron-agent repo created | 2026-04-28 | code start | Git | High (code) |
| E06 | State Streams KDA -> EKS | EKS transformer repos created | 2026-05-06 | code start | Git | High (code) |
| E07 | State Streams KDA -> EKS | EKS -> KDA rollback plan | 2026-10-16 | doc | Confluence IN 4256694278 | Low |
| E08 | Voltron / cache | Per-cluster build status tracker | 2026-10-21 | doc | Confluence CXONE 4232414340 | Low |
| E09 | Tenant moves | Tenant migration impact assessment | 2026-10-16 | doc | Confluence IN 4228809169 | Low |

RCA text also gives exact dates for single steps: a bulk BU move between AFM and VFM on 2026-06-02 (AOR-13252), and a manual VFM -> AFM move during an MI restore in 2026-09 (AOR-16073).

## 4. Pilot CFB monthly series (`agg_r11_pilot_monthly`)

- **EVIDENCE (High):** Pilot CFBs **step up in 2026-04.** The 2025 average is about 14 per month. 2026-04 to 2026-10 averages about 32 per month (×2.3).
- **EVIDENCE (High):** The step also shows in **valid** CFBs (invalid resolutions removed): about 8.6 per month in 2025, about 17 per month in 2026-05..10 (×2).
- **EVIDENCE (Medium):** 2026-04 has 27 CFBs but only 5 are valid. It is a burst of duplicates and "not a bug", probably around one incident.
- **EVIDENCE (Medium):** The rise is spread across sub-flows. 2026-04..07: stuck/lost contact 30, routing 29, ACD state 22.
- **EVIDENCE (Medium):** The team "Orchestration II" goes from about 2 to 11 CFBs per month starting 2026-04. Re-homing of bugs to this team is not excluded (2026 team transitions, e.g. site moves).

## 5. Event study: 8 weeks before vs 8 weeks after (`agg_r11_event_study`)

Control = CFBs of all other VPs (2025+).

| Event | Date | Pilot before -> after | Pilot RR (95% CI) | Control RR | Pilot vs control |
|---|---|---|---|---|---|
| E02 MessagePack start | 2026-01-15 | 23 -> 24 | 1.04 (0.59-1.85) | 0.75 | 1.40 |
| E03 net10 start | 2026-03-15 | 27 -> 45 | 1.67 (1.03-2.69) | 1.42 | 1.18 |
| E04 TFS repo | 2026-04-08 | 24 -> 72 | **3.00 (1.89-4.76)** | 1.16 | **2.58** |
| E05 voltron-agent repo | 2026-04-28 | 34 -> 85 | **2.50 (1.68-3.72)** | 1.07 | **2.33** |
| E06 EKS repos | 2026-05-06 | 41 -> 79 | **1.93 (1.32-2.81)** | 1.08 | **1.79** |

- **EVIDENCE (Medium):** In 2026-04/05 there is a pilot-specific step (×2-3). Other VPs stay flat (×1.1).
- **Limit:** E04, E05 and E06 fall within 4 weeks of each other, so the study cannot separate them. Code start is not production rollout. This test shows timing only. It does not show cause.

## 6. Causal path: does the RCA name a migration step?

- 69 of 466 pilot CFBs (15%) name a migrating component (AFM/VFM, Voltron/NCache/MessagePack, State Streams/KDA/EKS, .NET/netstandard/Newtonsoft, tenant/BU move). Last 12 months: 45 of 296.
- Tag precision for the component: about 17 of 18 in a sample. **But most tagged CFBs are latent defects in that component, not bugs caused by the migration.**
- Manual reading of "How was it introduced?" for the 45 tagged CFBs from the last 12 months (`migration_causal`):

| Judgment | Count | Examples (migration) |
|---|---|---|
| Caused by a migration step | 10 | .NET / library swaps 5 (System.Web for netstandard2.0, Newtonsoft conversion, MessagePack for NCache, missing DLLs); State Streams Kinesis connector upgrade 2; AFM/VFM moves and AFM DB migration 3 |
| Partly caused | 1 | dynamicjson serialization regression |
| Not caused by a migration | 34 | Latent VFM defects under load (shard lease loss, CPU saturation), original-design gaps, AWS / infra faults, feature changes |

- **EVIDENCE (Medium):** About **11 of 296 (3.7%)** pilot CFBs from the last 12 months name a migration step as the cause. This is a lower bound, because untagged CFBs can also come from migrations and 26% of RCAs name no cause.
- **EVIDENCE (Medium):** 6 of 11 come from the **monolith .NET / library modernization**. This supports PH-3 more than PH-2.
- **EVIDENCE (Medium):** About 8 tagged CFBs are **legacy VFM failures** (Kinesis shard lease, CPU saturation, DynamoDB throttle) while VFM still runs in parallel with AFM. This is an indirect cost of the dual-run period, not a defect of the migration itself.
- R9 RCAs with a component mention (25): introduced by a recent change 15, long-standing code 9. Without a mention (83): 33 recent, 36 long-standing. A recent change is more common when a migrating component is involved (60% vs 40%).

## 7. Verdict on PH-2

| Part | Verdict | Confidence |
|---|---|---|
| Timing: pilot CFBs step up when the 2026 migration work starts (2026-04/05), and the control does not | **Supported** | Medium |
| Direct cause: migration steps named as cause | **Weak**: about 4% of pilot CFBs (lower bound) | Medium |
| Mechanism: monolith library / runtime swaps | **Supported**: 6 of 11 (overlaps with PH-3) | Medium |
| Mechanism: dual-run AFM + VFM exposes latent legacy faults | **HYPOTHESIS** (about 8 CFBs) | Low-Medium |

**Overall: PH-2 is partly supported (Low-Medium).** The parallel migrations match the pilot step in time. RCAs name them as the cause only for a small share. Most of the step is still unexplained: latent races and defects surfacing under new load and topology, team re-homing, or more detection after incidents.

**What could invalidate this:**
- Production rollout dates that do not match the 2026-04/05 step.
- Proof that the "Orchestration II" growth is re-homing of existing bugs.
- RCAs that under-report migration causes. Teams may write "latent" when a migration exposed the defect.

## 8. Questions for SMEs (add to the R12 questionnaire)

1. Production dates per cluster or region: AFM enablement (`afmEnabled` per BU) waves, Voltron Phase 1 per cluster, State Streams EKS cutover per transformer, VCSvc 26.1 (.NET / Newtonsoft / netstandard) release date, TFS telephony first production use.
2. What happened in Orchestration Core in 2026-04: a release (26.1.x / 26.2), team changes, or a large incident?
3. Why did "Orchestration II" CFBs go from about 2 to 11 per month in 2026-04? Was there re-homing or a new ownership area?
4. During the dual-run, which BUs run on VFM and which on AFM? Is the CFB rate different between them?
5. Do RCAs mark "exposed by migration" defects as "latent"? Should the RCA template ask "Did a migration or move expose this?"

## 9. Gaps

- Jira migration Epics and Confluence schedules were not read (Atlassian timeouts). Re-run steps 1 and 4 when Atlassian responds.
- Causing items have no stored summaries (4 of 85), so the causal path uses the RCA text of the CFB only.
- Single rater for the judgments in section 6.
