# Summary and Recommendations

**As of:** 2026-10-22 | **Data:** Jira (11,662 CFBs; 3,292+ issues stored), Confluence, GitHub (7,866 commits, 1,663 PRs, 2,837 CI runs) | **DB:** `data/db/quality.sqlite`

## 1. Did quality go down? Yes, for customers.

| Evidence | Value | Confidence |
|---|---|---|
| CFB per year 2021-2025 | flat, about 1,300 | High |
| CFB 2026 (to Oct 22) | 1,428: more than any full year | High |
| H1 2026 vs H1 2025 | CFB +51%, P1/P2 +72% | High |
| P1/P2 share | about 50% -> 68% | High |
| Pilot (Orchestration Core flow), valid CFB | +34%; step from about 4 to 13 per month in 2026-05 | Medium |
| Incidents per pilot CFB | 2.3 -> 3.8 | Medium |

Per unit of delivery the picture is mixed (CFB per story +38% in Q2, -15% in Q3). Delivery volume grew 2.4x.

## 2. Why

| # | Cause | Evidence | Confidence |
|---|---|---|---|
| 1 | **Controls did not scale with change volume.** Policy on paper, no blocking gate. | 9 of ~15 Jira quality fields < 2% filled; Story RIA 0%; release gate human with all 26.4 pages "TBD" | High |
| 2 | **Test signal is broken, so failures are ignored.** | Routing E2E passes 1.2% and fails the same out-of-order scenarios; other E2E 69-79% | High |
| 3 | **Real scenarios are not tested.** | 28-31% of escapes | Medium |
| 4 | **State races** between the VC monolith and new services | 21% of valid pilot CFBs; VC-to-VC protocol has no per-contact version | Medium-High |
| 5 | **Big changes into hotspot code with thin review** | Follow-up fix rate 21% (small PRs) -> 54% (> 1000 lines) in hotspots | Medium |
| 6 | **Knowledge concentration** | Bus factor 1 on VC-to-VC sync; owner left agent-capacity | Medium |
| 7 | **Production conditions not reproduced** | No perf / chaos workflow | Medium |
| - | AI-assisted development as a per-change cause | **Not supported:** RR 1.03; AI PRs have fewer follow-up fixes (0.67) | Low-Medium |

## 3. Gates to add (real controls, in SDLC order)

A gate blocks work when its check fails. Policy without a block is not a gate (from the WIP DoD page, confirmed by data).

| Gate | Where | Check (blocking) | Cause it fixes | Today |
|---|---|---|---|---|
| **G1 Design** | Epic start, Tier-1 flows | Design review with a state / ordering and rollback-or-toggle section; named owners | 4, 6 | Human meeting, not enforced |
| **G2 Pull request** | GitHub, hotspot paths | <= 400 changed lines (1000 hard stop); 2 approvals incl. 1 code owner; test change or reason; Jira key | 5, 6 | None in monolith |
| **G3 Build** | CI | Unit + contract + ordering tests pass; Sonar quality gate; dependency / secret scan | 3, 4 | Opt-in local hooks only |
| **G4 Test health** | CI | A suite blocks merges only when its pass rate is >= 95% over 14 days; otherwise a repair ticket | 2 | Suites fail and are ignored |
| **G5 Pre-release** | Release candidate, Tier-1 | Fault and load stage; data-based Go/No-Go: E2E health, open P1-P3 = 0, valid CFB trend | 7, 1 | Go/No-Go pages "TBD" |
| **G6 Deploy** | Production | Feature toggle per change (no rollback on the monolith); progressive rollout; invariant monitors green before full rollout | 4, 7 | Toggles exist; no staged gate found |
| **G7 Escape** | CFB closure | Valid CFB closes only with a linked automated test or an approved "not testable" reason; RCA filled and reviewed | 3, 1 | RCA 89% filled, 33% reviewed |

**Not now, and why:** RIA agents (RIA misses are 7% of pilot escapes) and mutation testing at >= 80% (weak tests are 3% of escapes). They can come later, if the measures show they are needed.

## 4. What was not asked, but is needed

| Area | Gap found | What to do |
|---|---|---|
| **Governance** | No sponsor or decision owner (U-02); no single quality owner per Tier-1 flow | Name an accountable owner per Tier-1 flow; review S1-S7 monthly in the QSU |
| **Quality data** | Component 88% empty; Bug Type 48% empty; 51% of pilot CFBs invalid (duplicates per incident); only 2.7% of CFBs link the causing change | Make "caused by" and CFB-to-incident links required; dedupe CFBs by incident; retire unused fields |
| **Traceability** | 6-17% of EM commits name a Jira key; Xray links 18-25% | Jira key required in PRs (G2); tests linked to stories |
| **Detection** | Cannot tell if customers or alerts detect first (PH-5); monitoring added in 3% of RCAs | SLOs and alerts per Tier-1 flow; record "detected by" on each CFB |
| **Migration control** | No production rollout dates found for 2026 migrations | Rollout register (what, where, when); parity checks during dual run (VFM / AFM) |
| **AI governance** | 14 AI label variants; AI share 31-46% with no PR size policy; AI review bots not measured | One AI label standard; AI question in RCA template; same hotspot rules for AI PRs; re-test AI effect in 2027-Q1 |
| **Knowledge risk** | Bus factor 1; owner departures; site closure | Owner backup per hotspot; design notes for the VC core |
| **Security in work items** | Plain-text credentials found in a Jira issue | Secret scanning on Jira / Confluence; rotate exposed keys |
| **Quality data platform** | Sonar, CI/CD and incident data were not accessible | Keep this DB as the seed; automate a monthly refresh; add Sonar and incidents |

## 5. End goal and how we will know

Zero bugs in production is not a realistic target. The realistic goal: **escapes become rare, are caught before customers, and do not repeat.**

| Goal | Measure | Target |
|---|---|---|
| Fewer escapes | Valid pilot CFB per month (S1) | <= 9 in 2 quarters, then -50% vs 2025 |
| No repeats | Valid CFBs closed with a regression test | >= 90% |
| Caught before the customer | CFBs first detected by monitoring | Baseline first (data missing), then >= 50% |
| Less impact | Incidents per CFB (S3) | <= 2.5 |
| Trustworthy signal | E2E pass rate (G4) | >= 95% |

**Order:** pilot first (Orchestration Core), measure for 2 quarters (review 2027-04), then extend to Analytics and Data and WFM, which together with the pilot produce 60% of CFBs.
