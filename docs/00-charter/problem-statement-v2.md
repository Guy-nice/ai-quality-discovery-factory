> **Superseded** by [v4](problem-statement-v4.md) and [quality model v0](../07-quality-model/quality-model-v0.md).

# Problem Statement v2

**Version:** v2 | **Date:** 2026-10-22 | **Supersedes:** [v1](problem-statement-v1.md) | **Gate 2:** PARTIAL
**Evidence:** [Round 1](../02-research/findings-round-1.md), [Round 2](../02-research/findings-round-2.md)

## 1. Statement

In 2026, customers find more, and more severe, defects than in any year since at least 2021: CFB +51% and P1/P2 CFB +72% (H1 YoY), after five flat years. The rise is in three domains (Orchestration Core, Analytics and Data, WFM = 60%). Orchestration Core carries the highest severity and incident load.

The rise happened in the same quarters as two other changes:
- **AI-assisted delivery ramp:** AI-implemented stories went from 0.4% to 31% in three quarters.
- **Non-AI story growth:** +57%.

Defects escape for three main reasons:
- tests do not cover real scenarios (31%);
- changes break other consumers and RIA misses it (15%). RIA is missing at Story level, and when it is done it misses half the time;
- production scale, concurrency and environment conditions are not reproduced (about 20%).

Existing quality controls are mostly policy fields that are not filled. No blocking automated gate was found.

## 2. Claim status

| Hypothesis | Status | Confidence | Evidence |
|---|---|---|---|
| P-01 Quality declined | **Supported** for customer impact and severity. Per-story rate mixed (+38% Q2, -15% Q3, after import correction). | Medium-High | F1, F6 |
| P-02 Change rate exceeds validation capacity | **Supported, indirect.** Throughput up; Story-level RIA 0%; controls not filled; no blocking gate. | Medium | F6, F8 |
| P-03 Legacy monolith concentrates risk | **Weak.** 4% primary cause. | Low | F3 |
| P-04 AI-assisted development contributes | **Open, now testable.** Timing match. Attribution field exists (cf_15229). Pilot sample 33% vs 22% base, n=27. | Low | F7 |
| P-05 Knowledge concentrated | **Not tested.** Needs Git + SME. | - | - |
| P-06 (new) Controls exist on paper only | **Supported.** 9 of ~15 fields under 2% filled. | High | F8 |

## 3. Before Gate 2 can pass

- R8: CFB rate for AI vs non-AI causing changes.
- U-14: trend with invalid CFBs excluded, after triage.
- R5b: second rater + fill the 2026-H1 RCA gap.
- U-15: usage normalization (non-blocking).
