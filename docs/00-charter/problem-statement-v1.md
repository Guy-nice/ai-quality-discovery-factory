> **Superseded** by [v4](problem-statement-v4.md) and [quality model v0](../07-quality-model/quality-model-v0.md).

# Problem Statement v1

**Version:** v1 | **Date:** 2026-10-22 | **Supersedes:** [v0](problem-statement-v0.md) | **Gate 2:** PARTIAL
**Evidence:** [Findings Round 1](../02-research/findings-round-1.md)

## 1. Statement

In 2026, customers find more defects, and more severe ones, than in any year since at least 2021. Customer-found bugs rose 51% (H1 2026 vs H1 2025) and P1/P2 customer-found bugs rose 72%, after five flat years. The rise is concentrated in three R&D domains (Analytics and Data, Orchestration Core, WFM; 60% of volume). It happened at the same time as a 2.4× rise in delivered stories. Defects escape mainly because:
- tested scenarios do not cover real usage (31%);
- recent changes break other consumers and RIA does not catch it (15%);
- production scale, concurrency and environment conditions are not reproduced before release (about 20%).

## 2. Claim status vs v0

| v0 hypothesis | v1 status | Confidence | Evidence |
|---|---|---|---|
| P-01 Quality declined | **Supported for customer impact** (absolute CFB volume and severity). **Not supported per unit of delivery.** See C-01. | Medium-High | F1 |
| P-02 Change rate exceeds validation capacity | **Partly supported.** Throughput ×2.4 while absolute escapes and severity rise. Causal link not shown. | Medium | F1, F3 |
| P-03 Legacy monolith concentrates risk | **Weak support.** 3.8% primary cause, 11% mention. May be under-reported. | Low | F3 |
| P-04 AI-assisted development contributes | **Not testable with current data.** AI labels are rising (9% of CFBs) but their meaning is undefined. RCAs do not ask about AI. | Low | F4 |
| P-05 Knowledge concentrated | **Not tested.** | - | - |

## 3. Quality definition used (interim, D-006)

Primary: valid CFBs per quarter, total and P1/P2. Secondary: CFBs per 100 resolved stories. Both are reported together because they disagree (C-01).

## 4. Open before Gate 2 can pass

- U-13: explain the throughput jumps (stories resolved, all bugs).
- U-14: compute the 2026 trend with invalid CFBs excluded, after triage settles.
- U-15: normalize by customer base or usage.
- U-17: define what the AI labels mean.
- R5b: second-rater check on the RCA classification, and fill the 2026-H1 sample gap.
