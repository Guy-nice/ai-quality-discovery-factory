# Agent Reports - Round 3 (verbatim)

**Date:** 2026-10-22 | **Iteration:** 7 | Final reports of research forks, as returned. Synthesis: [findings-round-3](../../02-research/findings-round-3.md).

---

## R8 - AI vs non-AI defect rate

R8 found no higher bug rate per change for AI-implemented work. Among items the AI audit reviewed, the rate ratio (RR) is about 1.0. Confidence is Low-Medium, because only 13-29 AI items cause CFBs.

**Rows loaded (`data/db/quality.sqlite`):**

| Table | Rows |
|---|---|
| issues | 3,292 total: 2,811 CFBs created 2025+ (equals the JQL count), plus 412 causing items |
| issue_links | 3,229 |
| causal_links | 475: rca_text 370, is_caused_by 23, created_by 82 |
| jql_counts | 46 for R8 |
| query_log | 45 R8 dumps |
| raw_local.sqlite (gitignored) | 3,192 issue_text rows |

The raw JSON dumps are in `data/raw/r8/` (gitignored).

**Causal extraction:**
- 316 of 1,209 fixed CFBs (26%) name a causing key in the RCA text.
- Precision on a manual check: 19/20 (95%).

**Rate table (Story+Bug, AI vs not-AI causing items / items resolved):**

| Quarter | AI | Not-AI | RR |
|---|---|---|---|
| 2025-Q4 | 2/389 | 16/27,444 | 8.82 (n tiny) |
| 2026-Q1 | 3/2,819 | 26/28,377 | 1.16 |
| 2026-Q2 | 10/10,041 | 16/29,325 | 1.83 |
| 2026-Q3 | 7/10,012 | 14/36,010 | 1.80 (short exposure) |

**Pooled RR, 2026-Q1..Q2:** 1.39 (95% CI 0.75-2.59). Not significant.

**Sensitivity:**

| Scope | RR | 95% CI |
|---|---|---|
| (a) Reviewed items only (Yes vs No), Q1..Q2 | 0.92 | 0.45-1.88 |
| (a) Reviewed items only, Q1..Q3 | 1.03 | 0.57-1.86 |
| (b) Stories only | 1.61 | 0.74-3.49 |
| (b) Bugs only | 1.69 | 0.58-4.95 |
| Epics | 1.21 | 0.53-2.73 |
| Epics, reviewed only | 1.02 | 0.38-2.74 |
| (c) Per VP | 0.50 to 2.44 | all CIs include 1 |

**Biases:**
- How often a fixed CFB names its cause depends on the VP: A&D 9%, WFM 16%, others 31-41%.
- AI-made fixes name a cause at the same rate as other fixes: 27% vs 26%.
- AI causing items are more recent (median 28 vs 42 days from resolution to CFB). Shorter exposure works against finding AI CFBs.
- The crude RR of 1.39 comes mostly from mixing items the AI audit reviewed with unreviewed ones.

**Verdict:** P-04 (AI-assisted development contributes to the decline) is not supported at the per-change level. Confidence Low-Medium. A small effect (RR below 2) cannot be excluded. The 2026 CFB rise fits more change volume at the same per-change escape rate, which supports P-02.

**Files written (not committed):**
- `scripts/db/extract_causes.py`, `scripts/db/r8.sql`, `scripts/db/r8_analysis.py`, `scripts/db/r8_counts.sh`, `scripts/db/ingest_monthly.py`, `scripts/db/ingest_page.sh`
- `scripts/db/load.py` (patched to handle ADF rich-text fields)
- `data/aggregates/r8-ai-vs-nonai.csv` (also in the DB as table `agg_r8_ai_vs_nonai`)
- `docs/02-research/r8-ai-vs-non-ai.md`

No secrets seen.

---

## R9 - Orchestration Core deep dive

R9 is done: the deep dive of the Orchestration Core pilot (contact routing and lifecycle), with all pulled data in the DB. Nothing is committed. The DB holds no secrets: I scanned the new files and saw no credentials in the RCA text I read.

**Rows loaded into `quality.sqlite`:**
- 466 Orchestration Core CFBs (W_prev 170, W_last 296) and 50 epics resolved in 2026.
- 4 Xray counts and 6 R9 query_log entries.
- 108 RCAs classified (`rca_class`, round R9).
- 466 sub-flow tags (`flow_tags`).
- 30 Confluence pages and 13 Git repos.
- RCA and RIA text is in `raw_local.sqlite` only. Raw dumps are in `data/raw/r9/` (gitignored).

**Sub-flows (W_last).** The routing and lifecycle flow went from 123 to 218 CFBs (+77%). Admin/config grew only 8%.

| Sub-flow | Prev → Last | Note |
|---|---|---|
| Routing/skill/queue | 39 → 58 | Highest impact: 7.1 incidents per CFB, 26% with 5+ incidents, median 28 days to fix |
| Stuck/lost contact | 12 → 57 (+375%) | Teams clear stuck contacts with cleanup jobs; many root causes are recorded as "unknown" |
| ACD/contact state | 22 → 40 | 58% of CFBs closed as not a real defect |
| IVR/Studio | 16 → 27 | |

- **Invalid share:** 42% of all W_last CFBs close as invalid (duplicate, not a bug and similar).
- **Tagger precision:** the sub-flow tag is right in 80% of sampled CFBs. The in-flow vs out-of-flow split is right in 93%.

**Escape causes (pilot n=108 vs other VPs n=180):**

| Cause | Pilot | Other VPs |
|---|---|---|
| Missing test coverage | 28% | 27% |
| Scale/race/event ordering | 26% (29% in-flow) | 11% |
| RIA miss | 7% | 16% |
| Legacy behavior | 7% | 2% |

- Legacy code is named in 20% of pilot RCAs. 3 of 108 prevention actions add monitoring. 0 RCAs name AI-written code as a cause.

**Second-rater check (33 RCAs rated in both R5 and R9):** escape cause agreed 79%, regression 88%, prevention 97%, the other columns 100%. Both raters are Claude, so this is not an independent check. A human SME still needs to rate about 20 RCAs.

**Pilot root-cause hypotheses:**
- **PH-1, Medium-High:** distributed state races. Out-of-order or dropped events pass between the VC monolith, Entity Management and the routing services (AFM/VFM, Contact Retry), and tests do not model concurrency.
- **PH-2, Medium:** 5 parallel 2026 migrations change the same contact lifecycle at the same time: VFM→AFM, Voltron decoupling, State Streams KDA→EKS, .NET upgrades and tenant moves.
- **PH-3, Medium:** library and serializer swaps in the monolith break behavior, with no side-by-side parity tests. 11 RCAs show this.
- **PH-4, Medium:** production scale, real streams, failover and customer scripts cannot be reproduced before release. Environment and scale causes together are 35%.
- **PH-5, Medium:** customers detect problems first. Monitoring is rarely added as a prevention action.

**Confluence:**
- The Findmatch Testing Gap Analysis (page 4072866234) lists 35 test gaps, 3 critical. It found no integration test with a real Kafka broker or database and no concurrency test. About half of the Playwright E2E suite is marked fixme or skipped.
- The AFM chaos test plan has status "not started".
- A 50 ms latency injection cut matches by about 60%.
- Component map: the VC monolith and VFM are legacy. AFM, Entity Management, State Streams and TFS are new.

**Xray:**
- The pilot projects created 4,034 Tests in 2025 and 5,160 in 2026. They ran 54,131 Test Executions in 2025 and 46,804 in 2026.
- 1 of 50 Orchestration Core epics resolved in 2026 has a direct Test link. Tests may link to stories, which I did not check.
- RIA is filled on 22 of 59 of these epics. 10 of 59 are AI-implemented.

**Git:**
- **Access:** I have read access to the `inContact` org. R3 hotspot analysis is unblocked for the services.
- **Commits in the last 12 months:** AFM 254, agent-capacity 222, contact-retry 182, VFM 20.
- **Monolith:** the VC monolith is not in GitHub. It is probably in TFS, so the monolith needs TFS access.

**Out of scope:** ORC-52929 is a cross-tenant (cross-BU) authorization security defect. It is already a CFB, not a secret leak.

Files written:
- `scripts/db/r9_flow.py`, `r9_rca_show.py`, `r9_rca_load.py`, `r9_metrics.py`, `r9_extra.py`
- `data/aggregates/r9-pilot-subflow.csv`, `-team.csv`, `-escape-profile.csv`, `-escape-x-introduced.csv`, `-confluence-pages.csv`, `-git-repos.csv` (also imported as `agg_r9_*`)
- `docs/02-research/r9-pilot-orchestration-core.md`
- `data/db/quality.sqlite` (updated); local only: `data/db/raw_local.sqlite`, `data/raw/r9/*`

---

## R12a - SME candidates (iteration 9)

I found 16 candidates. The top 8 are ranked below, and 3 are recommended. No job titles were confirmed except Kevin Pyles: the other roles are guesses from Git and Confluence activity, and the ADR architect fields say "TBD".

| # | Name | Role (guess) | Area | Why | Evidence |
|---|---|---|---|---|---|
| 1 | Kevin Pyles | Lead QA Architect (title confirmed) | Orchestration Core QA, E2E, Go/No-Go | Named QA lead for the domain | CX 4213801473; acd-playwright-e2e 281 commits |
| 2 | Karthick Chandrasekaran | Tech lead / architect | AFM, contact-retry, agent-capacity, match-distributor | Top reviewer in 3 routing repos; covers the most services | PR reviews 37/33/43; commits 61/49/34/27 |
| 3 | Kacie Mayberry | Tech lead | VCSvc monolith + State Streams | Top human reviewer of VCSvc PRs; also works on State Streams | 99 VCSvc reviews; state-streams commits |
| 4 | Dez Grant | Senior engineer | VCSvc .NET modernization | Wrote the multi-TFM strategy page, which is direct evidence for PH-3 | IN 3696164975; 27 VCSvc commits |
| 5 | Anshul Agarwal | Observability focal point | VCSvc resilience, EOR gaps | Directly relevant to PH-4 and PH-5 | CX 3893887461, 3894051323, 3893887439 |
| 6 | Puneet Kumar | Architect | EM-TFS boundary, SLOs | Wrote the EM integration and SLO standard pages (PH-1, PH-2) | IN 4041444339, 4112547862 |
| 7 | Nichole Proestakis | QA automation lead | Routing integration and E2E tests | Top committer in both test repos (PH-1, PH-4) | 142 + 684 commits |
| 8 | Guy Law | Test-gap focal point | AFM tests | Wrote the Findmatch test-gap analysis | IN 4072866234 |

Other candidates (ranks 9-14): Jayakesavan Muthazhagan, Jesse Blanton, Shuchivrat Mayenkar (State Streams, PH-2), Derick Walburger, Rogerio Valenca da Cruz, Austin Wernli. Sponsor contacts, not SMEs: Namitha Nayak (VP) and Steve Gordon (program manager).

**Recommended 3:** Monolith / VC: Kacie Mayberry (backup for PH-3: Dez Grant). Services / EM / AFM: Karthick Chandrasekaran (backup for the EM boundary: Puneet Kumar). QA lead: Kevin Pyles.

**Gaps:** Jira assignee and reviewer data for the top 30 pilot CFBs was not pulled, because every Atlassian call after the first one timed out. Architecture and RACI searches in Confluence also timed out, so no named architects were found. Active status is assumed for people seen only in Confluence. Out of scope: the VCSvc Git history starts in 2021-01, so TFS is not needed for R3.

**Files written (not committed):** `scripts/db/r12_stakeholders.py`, `data/aggregates/r12-stakeholders.csv`, `quality.sqlite` tables `stakeholders` and `agg_r12_stakeholders` (16 rows each).
