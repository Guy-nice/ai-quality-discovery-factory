# Brief - AI Quality Discovery (1 page)

**Full summary:** [summary-and-recommendations](05-summary/summary-and-recommendations.md) | **As of:** 2026-10-22 | **Window:** 2025-01 to 2026-10 (2025 = baseline before AI; 2026 = AI ramp) | **Detail:** [README](../README.md)

## Answer

1. **Quality declined for customers.** Customer-found bugs (CFB) rose 51% and P1/P2 CFBs rose 72% (H1 2026 vs H1 2025).
2. **AI is not the cause per change.** AI changes do not produce more defects than other changes. But AI adds a lot of volume.
3. **Controls did not scale with volume.** Most quality fields are empty. There is no Story-level RIA and no blocking gate.
4. **Pilot root cause:** in Orchestration Core, the main cause is state races in the VC-to-VC sync and event code. Tests and ownership are weak there.

## AI in 2026

| Measure | 2025 | 2026 |
|---|---|---|
| AI-implemented stories | 0.2-0.4% | 10% -> 31% -> 23% (Q1-Q3) |
| AI PRs in pilot repos | 0-5% | 25% -> 46% (Q1-Q3) |
| AI PRs in top-10 hotspot code | 0% | 20% -> 51% |

| AI risk test | Result | Confidence |
|---|---|---|
| CFB per causing change, AI vs non-AI (R8) | RR 1.03 (0.57-1.86) | Low-Medium |
| CFB-fix within 30 days of a PR (R16) | RR 0.67 (0.47-0.95): fewer | Low-Medium |
| AI PRs touch tests (R16) | 63% vs 40% | Medium |
| AI PR size (R16) | 3.7x larger; review per line not higher | Medium |
| Team AI share vs valid CFB (R15) | No clear link (CI includes 1) | Low |

**Open AI risk:** large AI changes go into the hotspot code, and review depth does not grow with PR size.

## Pilot hypotheses (data check R17, 2 blind raters 85% agreement)

| ID | Hypothesis | Verdict | Human needed |
|---|---|---|---|
| PH-1 | State races in VC-to-VC sync and event path | Survives (Medium) | No |
| PH-4 | Production conditions not reproduced (no perf/chaos workflow; E2E passed 7 of 30 runs) | Survives (Medium) | No |
| P-05 | Knowledge concentration (bus factor 2; owner left) | Survives (Medium) | No |
| PH-3 | Library / runtime swaps | Minor (Low-Medium) | No |
| PH-2 | Parallel migrations | Weak (Low) | Yes: production dates |
| PH-5 | Customers detect first | Not testable | Yes: alert data |

## Gate status

G0-G3 passed (interim). **G4 passed (interim, data-based)** for PH-1, PH-4, P-05 and the test gap. PH-2 and PH-5 are excluded until a human gives the missing data. Solution options v0: [docs/04-solutions](04-solutions/solution-options-v0.md). **Wave 1 chosen from data:** [wave-1-plan](04-solutions/wave-1-plan.md). Key new fact: the routing E2E pipeline passed 1.2% of runs and fails the same out-of-order scenarios, so the race signal exists but is ignored. Order: E2E trust, ownership, stuck-contact monitor, hotspot PR rules; then escape-to-test and order-tolerant state design.
