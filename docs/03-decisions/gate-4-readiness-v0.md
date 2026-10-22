# Gate 4 Readiness Package v0 (R13)

**Date:** 2026-10-22 | **Scope:** pilot = Orchestration Core, contact routing and lifecycle flow (D-010, D-016) | **Gate 4 status:** **NOT PASSED**

The evidence is close to ready for solution design, but 3 blocking items remain: SME validation, production migration dates, and sponsor sign-off on the success criteria.

## 1. Root-cause hypotheses, ranked

| Rank | ID | Root cause | Evidence | Confidence | Validated by SME |
|---|---|---|---|---|---|
| 1 | PH-1 | Distributed state races in VC-to-VC sync (InterVCCommWrapper) and on the monolith-to-services event path. No concurrency or ordering tests. | 29% race escapes in-flow vs 11% elsewhere; 43-55% defect density; 4 / 1,349 test files concurrency-named; Findmatch gap analysis | Medium-High | No |
| 2 | Test gap | Real scenarios are not tested (all domains, 28-31%) | R5, R9 RCA classes | Medium | No |
| 3 | P-05 | Knowledge concentration: bus factor 1-2 on the densest code; an owner left agent-capacity; no owner on the big providers | R14 | Medium | No |
| 4 | PH-3 | Library / runtime swaps in the monolith without parity tests | 2.46x CFB-cause rate on dependency commits (mixed after size control); 6 CFBs | Low-Medium | No |
| 5 | PH-4 / PH-5 | Production conditions not reproduced; customers detect first (3/108 monitoring actions) | R9 | Medium | No |
| - | PH-2 | Parallel migrations | Timing only; about 4% direct | Low-Medium | No |
| - | P-04 | AI-assisted changes riskier per change | RR 1.03 (0.57-1.86) | Not supported | - |

## 2. Baseline metrics (frozen 2026-10-22, pilot in-flow, 12 months to 2026-10-22)

| Metric | Prior 12 mo | Baseline (last 12 mo) | Source |
|---|---|---|---|
| Valid CFB per month | 6.7 | **8.9** (step to about 17 since 2026-04) | DB `issues` + `flow_tags`; R11 monthly |
| All CFB per month | 10.2 | 18.2 | same |
| Invalid share | 35% | 51% | same |
| Valid P1/P2 share | 70% | 82% | same |
| Incidents per CFB (avg) | 2.25 | 3.8 | `incidents` field |
| CFB with 5+ incidents | 9.8% | 17.7% | same |
| Median days to fix (Fixed) | 12.5 | 12.0 | created -> resolved |
| Race / ordering escape share | - | 29% (n=72) | `rca_class` R9 |
| RCAs with a monitoring action | - | 3% (3/108) | `rca_class` R9 |
| Concurrency-named test files | - | 4 of 1,349 | R3 |
| Story-level RIA filled (all domains) | - | 0% (0/40) | R6 |
| Commits with a Jira key (AFM / EM) | - | 51% / 6-17% | R3 |

## 3. Constraints

| Constraint | Status | Source / owner |
|---|---|---|
| Data handling: no customer data in shared artifacts | Interim rule D-004 | Security (U-04) |
| CI duration and cost limits | UNKNOWN | DevOps |
| Sonar quality gate: blocking or not | UNKNOWN (U-20) | DevOps |
| Release cadence and Go/No-Go process | Human gate, 9 exit criteria | Confluence Go/No-Go template |
| Monolith: rollback not applicable (EOR template) | FACT | Jira EOR field |
| Team capacity during 2026 migrations | UNKNOWN | Orchestration Core GLs |
| Sponsor and decision owner | UNKNOWN (U-02) | Lead |

## 4. Success criteria (PROPOSED - sponsor to approve)

| # | Criterion | Target (proposal) | Measured by |
|---|---|---|---|
| S1 | Valid pilot CFB per month | Back to <= 9 within 2 quarters after the solution starts | Same query as the baseline |
| S2 | Race / ordering escape share | < 15% of classified pilot RCAs | `rca_class`, same rubric, human-checked sample |
| S3 | Incidents per pilot CFB | <= 2.5 | `incidents` field |
| S4 | Detection | >= 30% of pilot RCAs add a monitoring or alert action | `rca_class` prevention type |
| S5 | Ownership | Bus factor >= 3 on every top-10 hotspot | R14 method |
| S6 | Traceability | >= 80% of commits in pilot repos name a Jira key | R3 method |
| S7 | Data quality | Invalid CFB share < 35% | Baseline query |

## 5. Minimum evidence checklist (from research plan)

| # | Item | Status |
|---|---|---|
| 1 | Agreed quality definition | Interim (D-006); sponsor sign-off open |
| 2 | Trend with baseline, normalized, confounders checked | Done (F1, F6, F13) |
| 3 | Hotspot map for pilot (churn x defects x ownership) | Done (F14, F15) |
| 4 | Test effectiveness for pilot | Partial: test-touch rate + concurrency test absence; no mutation or coverage data |
| 5 | AI usage data or attribution statement | Done (F10) |
| 6 | >= 2 root-cause hypotheses validated against counter-evidence | **Open: needs SME validation (U-22)** |
| 7 | Constraints and success criteria | **Draft (this page); sponsor approval open** |

## 6. To pass Gate 4

1. **SME validation** (questionnaire ready; D-018 candidates). Blocking.
2. **Production rollout dates** for AFM, Voltron, State Streams EKS, TFS, 26.1 (U-23). They are needed to confirm or reject PH-2. Ask in the SME questionnaire. Blocking for PH-2 only.
3. **Sponsor approval** of the success criteria S1-S7 and of the quality definition. Blocking.
4. Non-blocking: Sonar / CI access (U-20), the Orchestration II re-homing check (U-24), and a re-run of Atlassian steps that timed out.

## Update v1 - 2026-10-22 (iteration 12)

**Gate 4: PASSED (interim, data-based)** for PH-1, PH-4, P-05 and the test gap. Lead delegated validation to data (D-022).

| Blocker (v0) | Resolution |
|---|---|
| SME validation | Replaced by data refutation R17 + blind second rater (85% agreement). PH-1, PH-4, P-05 survive. |
| Production migration dates | Still missing. Only PH-2 depends on them; PH-2 is excluded from solution scope. |
| Sponsor approval of S1-S7 | Set by research under D-005 (D-023). Lead may change. |

Corrections: concurrency tests exist in EM and AFM (content search); in-flow ordering share about 23% (S2 target stays < 15%).
New evidence for PH-4: no perf or chaos workflow in pilot repos; ephemeral E2E passed 7 of last 30 runs; integration tests 22 of 30.
