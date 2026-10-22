# R3 + R14 - Code Hotspots and Knowledge Concentration (Pilot)

**Date:** 2026-10-22 | **Scope:** pilot D-010 / D-016 (Orchestration Core, contact routing and lifecycle) | **Sources:** GitHub `inContact` org (read-only), Jira data in DB
**DB tables:** `git_commits`, `git_file_changes`, `r3_commit_flags`, `r3_dir_hotspots`, `r3_file_hotspots`, `r14_ownership`, `r3_test_names`, `agg_r3_*`, `agg_r14_ownership`
**Scripts:** `scripts/db/r3_git_ingest.py`, `scripts/db/r3_hotspots.py`, `scripts/db/r3.sql`

## 1. Method

- **Repos (13):** monolith `inContact/inContact` (DEVELOP) + 10 pilot service repos + 2 test repos. Blobless shallow clones (since 2024-10-01) in `data/raw/git/` (gitignored). Only metadata is read: no file content.
- **Window:** 2024-10-22 to 2026-10-22 (24 months). Churn = last 12 months.
- **Stored:** commit sha, date, author name, merge flag, bot flag, **Jira keys from the message** (not the message text), changed paths. No emails.
- **Excluded from counts:** merge commits, bot authors, bulk commits (> 500 files, 13 in the monolith, e.g. 83,486 files on 2026-06-14).
- **Jira link:** a commit is a **CFB fix** when its message names a CFB key (`issues.is_cfb = 1`). It is a **pilot fix** when the key is in pilot flow scope (`flow_tags.in_flow_scope = 1`). It is **causing** when the key is a causing item in `causal_links` (R8).
- **Directory unit:** monolith depth 5 (VCSvc providers depth 6); Java services package depth 8; other depth 3.
- **Hotspot score** = percentile rank of 12-month commits x percentile rank of (CFB-fix + causing commits, 24 months). Only dirs with at least 1 defect signal. Range 0-1.
- **Bus factor (50%)** = the minimum number of authors that cover 50% of the dir's 12-month commits. **Departed owner** = an author with more than 30% of the dir's 24-month commits and no commit in any pilot repo after 2026-04-22.
- **Test touch** = share of the dir's commits that also change a test path.

## 2. Data

| Item | Count |
|---|---|
| Commits ingested (24 mo) | 7,866 (monolith 4,375) |
| File changes | 184,464 |
| Distinct human authors | 493 |
| Directory hotspot rows | 404 (monolith 358, services 31, test repos 15) |
| File hotspot rows | 1,070 (top 300 in CSV) |

**Jira link rate (commits naming any Jira key):** monolith **75.6%**; AFM 51%; contact-retry 39%; agent-capacity 30%; Entity Management repos 6-17%; state-streams-common 64%. **EVIDENCE (High):** service repos link weakly to Jira, so their defect signal is **under-counted**.

| Repo | Commits | CFB-fix commits | Pilot-fix commits | Causing commits |
|---|---|---|---|---|
| inContact (monolith) | 4,099 | 271 | 110 | 65 |
| routing-ng-advanced-findmatch (AFM) | 268 | 15 | 15 | 10 |
| routing-ng-agent-capacity-service | 150 | 12 | 12 | 0 |
| routing-ng-contact-retry | 235 | 9 | 9 | 0 |
| others (9 repos) | 1,606 | 6 | 6 | 5 |

## 3. Pilot hotspots (by pilot-flow CFB-fix commits)

| # | Repo | Directory | Commits 24 mo | Pilot fixes | Causing | Defect share of commits | Test touch |
|---|---|---|---|---|---|---|---|
| 1 | monolith | `Code/C#/Services/VCSvc/Providers/ACD` | 174 | 17 | 17 | 22% | 71% |
| 2 | monolith | `Code/C#/Library/AgentHelper` | 113 | 14 | 7 | 21% | 68% |
| 3 | AFM | `src/main/java/com/nice/routing/afm/service` | 122 | 14 | 8 | 18% | 53% |
| 4 | monolith | `Code/C#/Library/inContact.InterVCCommWrapper/SynchronizerMessages` | 39 | 13 | 4 | **44%** | 67% |
| 5 | monolith | `Code/C#/Services/VCSvc/Providers/Data` | 572 | 11 | 10 | 7% | 49% |
| 6 | monolith | `Database/InDB_DACPAC/inCode/dbo/StoredProcedures` | 571 | 10 | 17 | 10% | 34% |
| 7 | monolith | `Code/C#/Library/AgentHelper/MCH` | 67 | 10 | 2 | 21% | 52% |
| 8 | monolith | `Code/C#/Library/inContact.InterVCCommWrapper/Messages` | 22 | 10 | 2 | **55%** | 77% |
| 9 | monolith | `Code/C#/Services/VCSvc/Providers/Agent` | 169 | 9 | 8 | 12% | 60% |
| 10 | agent-capacity | `src/main/java/com/nice/routing/agentcapacityservice/client` | 25 | 8 | 0 | **32%** | 76% |
| 11 | monolith | `Code/C#/Library/inContact.InterVCCommWrapper/Clients` | 22 | 8 | 3 | **50%** | 73% |
| 12 | monolith | `Code/C#/Library/ScriptHelper/Models` | 61 | 7 | 8 | 25% | 54% |

**Top files (pilot fixes, 24 mo):**
- `VCSvc/Providers/ACD/ACDProvider.cs`: 17 pilot fixes, 15 causing, 57 commits in 12 months.
- AFM `FindmatchServicePostgreSQL.java`: 14 fixes, 8 causing.
- `AgentHelper/Agent.cs`: 14 fixes.
- `InterVCCommWrapper/SynchronizerMessages/SynchronizeMes...`: 13 fixes in 16 commits.
- `MCHAgent.cs`: 8 fixes.
- agent-capacity `QueueDetailsClient.java`: 8 fixes.
- `IVRVCGrpcClient.cs`, `MasterAgentVCGrpcClient.cs`, `AgentVCGrpcClient.cs`, `SlimVCGrpcClient.cs`: 7-8 fixes each.

**Overall score leaders** (all CFBs, not only the pilot): `StoredProcedures` (1.00), `VCSvc/Providers/Data` (0.99), `Post-Deployment` scripts (0.98), `IvrScriptUtil` (0.97), WebApp `Manage` (0.97). The full list is in `r3-hotspots.csv`.

## 4. Boundary hotspots (path names verified)

| Directory | Token | Commits 12 mo | Pilot fixes | Causing |
|---|---|---|---|---|
| `InterVCCommWrapper/SynchronizerMessages` | Messag(e) | 16 | 13 | 4 |
| `InterVCCommWrapper/Messages` | Messag(e) | 9 | 10 | 2 |
| `VCSvc/Providers/ProviderEventMessaging` | Event | 44 | 4 | 3 |
| `VCSvc/Providers/EventPub` | Event | 35 | 5 | 2 |
| `VCSvc/Providers/ProviderEntityStateManagement` | Entity | 35 | 4 | 2 |
| `Library/EventHubProducerLibrary` | Event | 26 | 0 | 5 |
| `contact-retry/.../kafka` | kafka | 21 | 1 | 0 |

- **EVIDENCE (High):** the inter-VC gRPC synchronization layer (`inContact.InterVCCommWrapper`: SynchronizerMessages, Messages, Clients, Interfaces) has the **highest defect density in the pilot**: 43-55% of its commits fix a CFB or cause one, against 7-22% in the large provider dirs.
- This is **state synchronization between VC nodes inside the monolith**. The monolith-to-services event dirs (EventPub, ProviderEventMessaging, ProviderEntityStateManagement) carry a moderate density (12-15%).

## 5. Knowledge concentration (R14)

| Directory | Commits 12 mo | Authors >= 10% | Top author share | Bus factor (50%) | Departed owner > 30% |
|---|---|---|---|---|---|
| VCSvc/Providers/ACD | 84 | 0 | 8% | 9 | - |
| AgentHelper | 65 | 1 | 11% | 10 | - |
| AFM afm/service | 75 | 4 | 20% | 3 | - |
| InterVCCommWrapper/SynchronizerMessages | 16 | 3 | 44% | 2 | - |
| InterVCCommWrapper/Messages | 9 | 3 | 67% | **1** | - |
| InterVCCommWrapper/Clients | 8 | 4 | 63% | **1** | - |
| InterVCCommWrapper/Interfaces | 10 | 5 | 50% | **1** | - |
| agent-capacity .../client | 25 | 2 | 48% | 2 | **Yes (48%)** |
| agent-capacity .../agentcapacityservice | 34 | 3 | 41% | 2 | **Yes (38%)** |
| VCSvc/Providers/Data | 333 | 0 | 4% | 21 | - |

- **EVIDENCE (High): two opposite patterns.**
  - *Diffuse ownership* in the big monolith providers: ACD, Agent and Data have no author with 10% or more, and 9-21 authors cover half of the work. No one owns them.
  - *Concentrated ownership* in the highest-density dirs: InterVCCommWrapper has a bus factor of 1-2, and the top author does 44-67% of the work.
- **EVIDENCE (High):** agent-capacity-service: an author who did 38-56% of the work in 5 dirs has no commits after 2026-04-22 (departed or moved). Agent-capacity has 8 pilot-fix commits in its `client` dir.
- Other departed owners (> 30%) are in non-pilot monolith dirs. See `r14-ownership.csv`.

## 6. Test signal

| Repo / area | Test files | Concurrency-named test files |
|---|---|---|
| Monolith pilot dirs (VCSvc, AgentHelper, InterVCCommWrapper, ScriptHelper) | 971 | **3** (`ScriptManager_WakeupInterruptRaceTests`, `MrmElastiCacheManagerConcurrencyTests`, `LogQueueThreadFactoryIntegrationTests`) |
| AFM, agent-capacity, contact-retry, blender, match-distributor | 61 | **0** |
| Entity Management + state-streams repos | 271 | 0 |
| routing-ng-integration-tests | 46 | 1 (`OutOfOrderStepDefinition`) |
| VFM (app-findmatch, legacy) | 267 | 5 (load + out-of-order specs) |

- Name match only (Concurrency, Race, Parallel, LoadTest, Stress, Chaos, Threading, Contention, Deadlock, OutOfOrder, Ordering). Content not read.
- Test touch in pilot hotspots: **49-77%** of commits also change tests. **EVIDENCE (Medium):** teams do add tests with changes. The gap is the **type** of test: no concurrency or ordering tests where defects concentrate. This matches the Findmatch gap analysis (Confluence 4072866234).
- The new AFM service has no out-of-order tests. Its legacy predecessor VFM had them (`OutOfOrderSpecification.scala`).

## 7. What this says about the hypotheses

| Hypothesis | Verdict | Confidence | Evidence | Could invalidate |
|---|---|---|---|---|
| **PH-1** distributed state races, no concurrency tests | **Supported, refined.** The densest defect area is VC-to-VC state sync (InterVCCommWrapper, 43-55% defect share), plus ACDProvider / AgentHelper. Concurrency-named tests: 3 of 971 in monolith pilot dirs, 0 in routing services. | Medium-High | Sections 3, 4, 6 | Concurrency tests exist under other names, or in another repo or pipeline; fixes in InterVCCommWrapper are not race-related (needs a read of the RCAs of those 13 CFBs) |
| **PH-3** library / runtime swaps break behavior | **Weak-Moderate.** Monolith commits that touch dependency / runtime files (.csproj, .props, packages, config) are "causing" 2.9% vs 1.2% (RR 2.46, 95% CI 1.51-4.00). After stratification by commit size: 1-2 files RR 4.5 (1.6-12.6); 3-9 files 0.85 (0.3-2.3); 10+ files 1.96 (0.8-4.9). Size confounds part of the effect. | Low-Medium | `scripts/db/r3.sql` | The causing items are not runtime swaps; or the commit-size control removes the effect |
| **P-05** knowledge concentration | **Supported, two-sided.** Bus factor 1-2 in the highest-density dirs (InterVCCommWrapper); departed owner in agent-capacity; no owner in the big ACD / Agent / Data providers. | Medium | Section 5 | Ownership is shared through reviews (PR review data not used here); authors moved but still review |

## 8. Limits

- The defect signal depends on Jira keys in commit messages. Link rate is 6-51% in services and 76% in the monolith, so services are under-counted.
- `issues` holds CFBs from 2025 onward (all VPs) plus Orchestration Core CFBs from 2024-10. Older non-pilot CFB fixes are missed.
- Shallow clones from 2024-10-01. Default branch only, so work on release branches is not counted.
- Author names are not merged across aliases. One person with two names lowers the measured concentration.
- Test detection uses file names, not content.
