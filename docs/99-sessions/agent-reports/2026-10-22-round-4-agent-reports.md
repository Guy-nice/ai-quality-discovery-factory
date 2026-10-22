# Agent Reports - Round 4 (verbatim)

**Date:** 2026-10-22 | **Iteration:** 11 | Synthesis: [findings-round-4](../../02-research/findings-round-4.md).

---

## R3 + R14 - Hotspots and ownership

R3+R14 is done. Nothing is committed (per the directive).

**Rows loaded into `quality.sqlite`:**
- `git_commits` 7,866 (monolith 4,375) and `git_file_changes` 184,464, from 493 authors.
- `r3_commit_flags` 7,866, `r3_dir_hotspots` 404, `r3_file_hotspots` 1,070, `r14_ownership` 404, `r3_test_names` 13.
- Aggregate tables: `agg_r3_hotspots`, `agg_r3_file_hotspots`, `agg_r14_ownership`, `agg_r3_test_names`.
- Clones (blobless, metadata only) are in `data/raw/git/` (gitignored).

**Commits that name a Jira key:** monolith 75.6%; AFM 51%, contact-retry 39%, agent-capacity 30%, Entity Management repos 6-17%. So the defect signal in the services is under-counted.

**Top pilot hotspots (commits that fix a pilot CFB, 24 months):**

| # | Directory | Pilot fixes | Commits that fix or cause a CFB |
|---|---|---|---|
| 1 | VCSvc/Providers/ACD (ACDProvider.cs alone: 17 fixes, 15 causing) | 17 | 22% |
| 2 | Library/AgentHelper | 14 | 21% |
| 3 | AFM afm/service (FindmatchServicePostgreSQL.java) | 14 | 18% |
| 4 | InterVCCommWrapper/SynchronizerMessages | 13 | 44% |
| 5 | VCSvc/Providers/Data | 11 | 7% |
| 6 | DB StoredProcedures | 10 | 10% |
| 7 | AgentHelper/MCH | 10 | 21% |
| 8 | InterVCCommWrapper/Messages | 10 | 55% |
| 9 | VCSvc/Providers/Agent | 9 | 12% |
| 10 | agent-capacity .../client | 8 | 32% |

**Event-boundary hotspots:** the inter-VC gRPC sync layer (InterVCCommWrapper: SynchronizerMessages, Messages, Clients, Interfaces) has the highest defect density: 43-55% of its commits fix or cause a CFB. The monolith-to-services event dirs (EventPub, ProviderEventMessaging, ProviderEntityStateManagement) are moderate, at 12-15%.

**Knowledge concentration:** InterVCCommWrapper: bus factor 1-2; the top author does 44-67% of the work. agent-capacity-service: an author who did 38-56% of the work in 5 dirs has no commits after 2026-04-22. The big ACD, Agent and Data providers have the opposite problem: ownership is spread thin; bus factor is 9-21, and no author has 10% of the commits.

**Tests:** 49-77% of commits in the hotspot dirs also change tests. Concurrency-named tests: monolith pilot dirs 3 of 971 test files; AFM, agent-capacity, contact-retry, blender, match-distributor 0 of 61; Entity Management and state-streams repos 0 of 271; integration-test repo 1 of 46. Legacy VFM had out-of-order tests. The new AFM that replaces it has none.

**Verdicts:** PH-1 supported, narrowed to VC-to-VC state sync plus ACDProvider and AgentHelper (Medium-High). PH-3 weak to moderate: dependency/runtime commits cause CFBs 2.46× more often (CI 1.51-4.00), mixed after control for commit size (Low-Medium). P-05 supported, two-sided pattern (Medium). No secrets were seen.

**Files written:** `scripts/db/r3_git_ingest.py`, `scripts/db/r3_hotspots.py`, `scripts/db/r3.sql`; `data/aggregates/r3-hotspots.csv`, `r3-file-hotspots.csv`, `r14-ownership.csv`, `r3-test-names.csv`; `docs/02-research/r3-r14-hotspots-ownership.md`; `data/db/quality.sqlite` (updated).

---

## R11 - Migration timeline vs CFB

R11 is done: PH-2 (2026 parallel migrations drive pilot CFB growth) is only partly supported, Low-Medium confidence.

**Data limit:** every Atlassian call timed out during R11, so there are no production rollout dates and no migration Epics. All event dates come from Git and are code-start dates, not production dates.

**Events found:** E01 AFM repo created 2022-03-28; E02 MessagePack work in VCSvc starts 2026-01 (14 commits through 2026-05); E03 net10 / multi-TFM work starts 2026-03 (22 commits); E04 Telephony Feature Service repo created 2026-04-08; E05 voltron-agent repo created 2026-04-28; E06 State Streams EKS repos created 2026-05-06; E07-E09 EKS rollback plan, Voltron build tracker, tenant migration assessment (2026-10, Confluence last-modified dates only). RCA text gives two exact step dates: a bulk BU move between AFM and VFM on 2026-06-02, and a manual VFM→AFM move during an MI restore in 2026-09.

**Event study (8 weeks before vs after; control = CFBs of all other VPs):**

| Event | Pilot RR (95% CI) | Control RR |
|---|---|---|
| E02 MessagePack | 1.04 (0.59-1.85) | 0.75 |
| E03 net10 | 1.67 (1.03-2.69) | 1.42 |
| E04 TFS repo | 3.00 (1.89-4.76) | 1.16 |
| E05 voltron-agent | 2.50 (1.68-3.72) | 1.07 |
| E06 EKS repos | 1.93 (1.32-2.81) | 1.08 |

Pilot CFBs step up in 2026-04: about 14/month in 2025, about 32/month April-October 2026. Valid CFBs about double (8.6 → 17/month). Other VPs flat. E04-E06 are within 4 weeks of each other: timing only, not cause.

**Causal path:** 69 of 466 pilot CFBs name a migrating component (tag right in ~17/18 samples), but most are latent defects. Of 45 tagged CFBs (last 12 months), "How was it introduced": 10 migration step, 1 partly, 34 not. So about 11 of 296 pilot CFBs (3.7%) name a migration step as cause (lower bound); 6 of 11 are .NET/library swaps in the monolith (PH-3). About 8 tagged CFBs are legacy VFM failures (shard lease loss, CPU saturation, DynamoDB throttle) during the VFM/AFM dual run (hypothesis, Low-Medium).

**Verdict PH-2:** timing match supported (Medium); direct cause weak (~4%). Most of the 2026-04 step unexplained. Open candidates: Orchestration II team ~2 → 11 CFBs/month from 2026-04 (re-homing possible); a 2026-04 burst of 27 CFBs with only 5 valid; latent faults under new load.

**Gaps:** production dates per cluster/BU (AFM, Voltron, EKS, 26.1, TFS) - questions in R11 doc section 8; re-run Jira/Confluence steps when Atlassian responds; causing items have few stored summaries (4/85); single rater on causal judgments.

**Files:** `scripts/db/r11_migrations.py`; `data/aggregates/r11-migration-events.csv`, `r11-event-study.csv`, `r11-pilot-monthly.csv` (also `agg_r11_*`); DB tables `migration_events` (9), `migration_mentions` (85), `migration_causal` (45); `docs/02-research/r11-migrations-vs-cfb.md`.
