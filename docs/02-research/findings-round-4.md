# Research Findings - Round 4

**Date:** 2026-10-22 | **Sources:** GitHub `inContact` (read-only), DB | **Detail:** [R3 + R14](r3-r14-hotspots-ownership.md), [R11](r11-migrations-vs-cfb.md)

## F13 - Correction: valid pilot CFB growth (U-14)

The headline growth (+77%) counts invalid closures. Valid CFBs grew less, and they are more severe.

| Pilot in-flow CFB | 2024-10..2025-10 | 2025-10..2026-10 | Change |
|---|---|---|---|
| All | 123 | 218 | +77% |
| Invalid (not a bug, duplicate, won't fix, works as designed, cannot reproduce) | 43 (35%) | 111 (51%) | +158% |
| **Valid** | **80** | **107** | **+34%** |
| Valid P1/P2 share | 70% | 82% | +12 pt |
| Open now | 0 | 26 | triage lag |

- **EVIDENCE (High):** The invalid share rose from 35% to 51%. Duplicates and "not a bug" closures drive most of the headline rise.
- **EVIDENCE (Medium):** Valid CFBs step up in 2026-04: about 8.6 -> 17 per month (R11). Other VPs stay flat.
- **HYPOTHESIS (Medium):** The invalid rise is a symptom too. One incident produces many duplicate CFBs (incidents per CFB 2.3 -> 3.8), or bugs are re-homed to new teams (Orchestration II 2 -> 11 per month from 2026-04).

## F14 - Code hotspots (R3)

Data: 7,866 commits (monolith 4,375), 184,464 file changes, 493 authors, 24 months. Commits that name a Jira key: monolith 76%, AFM 51%, contact-retry 39%, agent-capacity 30%, EM repos 6-17%. So the CFB signal in the services is under-counted.

| # | Hotspot (directory) | Repo | Pilot CFB-fix commits | Commits that fix or cause a CFB |
|---|---|---|---|---|
| 1 | VCSvc/Providers/ACD (ACDProvider.cs: 17 fix, 15 causing) | monolith | 17 | 22% |
| 2 | Library/AgentHelper | monolith | 14 | 21% |
| 3 | afm/service (FindmatchServicePostgreSQL.java) | AFM | 14 | 18% |
| 4 | InterVCCommWrapper/SynchronizerMessages | monolith | 13 | **44%** |
| 5 | VCSvc/Providers/Data | monolith | 11 | 7% |
| 6 | DB StoredProcedures | monolith | 10 | 10% |
| 7 | AgentHelper/MCH | monolith | 10 | 21% |
| 8 | InterVCCommWrapper/Messages | monolith | 10 | **55%** |
| 9 | VCSvc/Providers/Agent | monolith | 9 | 12% |
| 10 | agent-capacity client | agent-capacity | 8 | 32% |

- **EVIDENCE (Medium-High):** The most defect-dense code is the inter-VC gRPC state sync layer (InterVCCommWrapper): 43-55% of its commits fix or cause a CFB. The monolith-to-services event directories (EventPub, ProviderEventMessaging, ProviderEntityStateManagement) are at 12-15%.
- **EVIDENCE (High):** Tests change often: 49-77% of hotspot commits also touch test files. But concurrency or ordering tests are almost absent: 3 of 971 test files in the monolith pilot directories, 0 of 61 in the routing services, 0 of 271 in the EM / state-streams repos.
- **EVIDENCE (Medium):** Legacy VFM had out-of-order tests. AFM, which replaces it, has none.

## F15 - Knowledge concentration (R14, P-05)

| Pattern | Where | Evidence |
|---|---|---|
| Too concentrated | InterVCCommWrapper | Bus factor 1-2; top author 44-67% of commits |
| Owner left | agent-capacity-service (5 directories) | Author with 38-56% of commits; no commits after 2026-04-22 |
| Too diffuse | VCSvc ACD / Agent / Data providers | Bus factor 9-21; no author >= 10% |

- **EVIDENCE (Medium):** P-05 is supported, in two forms. The most defect-dense code depends on 1-2 people. The biggest monolith providers have no clear owner.

## F16 - Migrations vs CFB (R11, PH-2)

| Event (code start, from Git) | Date | Pilot RR, 8 weeks after vs before (95% CI) | Control RR |
|---|---|---|---|
| MessagePack in VCSvc | 2026-01 | 1.04 (0.59-1.85) | 0.75 |
| net10 / multi-TFM | 2026-03 | 1.67 (1.03-2.69) | 1.42 |
| TFS repo created | 2026-04-08 | 3.00 (1.89-4.76) | 1.16 |
| voltron-agent repo created | 2026-04-28 | 2.50 (1.68-3.72) | 1.07 |
| State Streams EKS repos | 2026-05-06 | 1.93 (1.32-2.81) | 1.08 |

- **EVIDENCE (Medium):** Pilot CFBs step up in 2026-04, when 3 migration programs start. Other VPs stay flat.
- **EVIDENCE (Medium):** Only about 11 of 296 pilot CFBs (3.7%, a lower bound) name a migration step as the cause. 6 of the 11 are .NET or library swaps in the monolith (PH-3).
- **HYPOTHESIS (Low-Medium):** About 8 CFBs are legacy VFM failures during the VFM/AFM dual run.
- **Limit:** the dates are code-start dates, not production rollout dates. Atlassian timed out, so no Jira or Confluence dates were collected (U-23).
- **Verdict PH-2:** timing supported. Direct cause weak (about 4%). Most of the 2026-04 step is unexplained.

## Updated hypothesis status

| ID | Status | Confidence | Change |
|---|---|---|---|
| PH-1 State races | **Supported, narrowed** to VC-to-VC state sync (InterVCCommWrapper) + ACDProvider / AgentHelper; no concurrency tests | Medium-High | Narrowed (F14) |
| PH-2 Parallel migrations | Timing only; direct cause about 4% | Low-Medium | Weakened (F16) |
| PH-3 Library / runtime swaps | Dependency-touching commits cause CFBs 2.46x more often (CI 1.51-4.00), mixed after a size control; 6 migration-caused CFBs | Low-Medium | Unchanged |
| PH-4 Production conditions not reproducible | Not tested further | Medium | - |
| PH-5 Customers detect first | Not tested further | Medium | - |
| P-05 Knowledge concentration | Supported (two-sided) | Medium | New (F15) |

## Correction 2026-10-22 (iteration 12, R17)

- **CORRECTION:** "4 of 1,349 concurrency-named test files" counted file **names** only. A content search finds more: EM state-manager has 4 "out of order" + 15 "concurrent" test files; AFM has 4 "concurrent". The claim "almost no concurrency tests" is too strong. The correct claim: concurrency tests exist in EM and AFM, but they did not stop the in-flow ordering escapes (about 23% after re-read).
- **CORRECTION:** PH-1 race share re-read blind: 22 of 28 "race" RCAs show race / ordering, 6 show load only. In-flow ordering share is about 23% (was 29%), still about 2x other VPs.
