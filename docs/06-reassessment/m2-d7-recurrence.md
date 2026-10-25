# D7 Non-recurrence - Do the Same Failures Come Back?

**Date:** 2026-10-25 | **Data:** 1,452 valid CFBs 2025-01..2026-10 (MI-investigation tickets excluded, D-032) | **Script:** `scripts/db/m2_d7_recurrence.py` | **DB:** `repeat_pairs`, `recurrence_summary`, `agg_m2_d7_recurrence`

## Method

- **Repeat** = a later valid CFB with the same team and the same failure type, and a summary similar to an earlier valid CFB (TF-IDF cosine), within 180 days.
- **Threshold:** from a read of 40 pairs. Precision by cosine band: >= 0.5: 10/10; 0.4-0.5: about 5/10; 0.3-0.4: about 3/10; 0.2-0.3: about 3/10. Main threshold 0.5 (lower bound); 0.4 as sensitivity.
- **Recurred after fix** = the earlier CFB was resolved Fixed before the later one was created. Else **parallel report** (same open defect, another customer).
- Fair window: only CFBs from 2025-07 on (180-day look-back inside the data).

## Results

| Measure | 2025-H2 | 2026-H1 | 2026-Q3+ | Confidence |
|---|---|---|---|---|
| Repeat rate, cosine >= 0.5 | 14.8% (64/433) | 2.0% (8/400) | 2.0% (6/306) | Medium |
| Repeat rate, cosine >= 0.4 | 18.9% | 3.2% | 5.2% | Low-Medium |
| **Recurred after fix**, >= 0.5 | 3.9% (17/433) | 1.2% (5/400) | 1.6% (5/306) | Medium |
| Duplicate resolution (all non-MI CFBs) | 11.0% | 8.7% | 7.5% (2026-H2) | High |
| Reopened (status changed from Done) | 5.2% (2025, 72/1,382) | 5.6% (2026, 80/1,428) | - | Medium |

- **EVIDENCE (Medium):** Repeats are concentrated in one wave. In 2025-H2, 59 of 64 repeats were Analytics and Data DATA failures: stuck or stale contacts in the CXone Dashboard (ClearView). DATA repeat rate fell from 40.4% (2025-H2) to 4.5% (2026-H1).
- **EVIDENCE (Medium):** 61% of repeat pairs are parallel reports of an open defect. 39% recurred after a fix. So most "repeats" are many customers that hit the same unfixed defect, not fixes that failed.
- **EVIDENCE (Medium):** Recurrence after fix is low and did not grow: 3.9% -> 1.2-1.6%. Reopen rate is flat (5.2% -> 5.6%).

## Fix-caused defects

Of fixed CFBs whose RCA names the causing item (causal_links; about 26% of fixed CFBs):

| Causing item | 2025 | 2026 |
|---|---|---|
| A Bug (a bug fix broke something) | 23.5% (36/153; CI 17.5-30.8) | 27.1% (45/166; CI 20.9-34.3) |
| A CFB fix | 4.6% (7/153; CI 2.2-9.1) | 10.8% (18/166; CI 7.0-16.5) |

- **CORRELATION (Low-Medium):** About 1 in 4 named causes is a bug fix. The share caused by a customer-bug fix rose from 4.6% to 10.8% (the CIs touch). This fits the R9 finding that hand-written fixes caused new defects.
- **Limit:** only about a quarter of RCAs name the causing item. The naming rate differs by VP (A&D 9%, others 31-41%).

## Prevention action vs later repeat

| Earlier RCA prevention | n (with 180-day follow-up) | Later repeat |
|---|---|---|
| Test added | 44 | 0 |
| Process change | 28 | 1 |
| Code fix only | 12 | 0 |
| None stated | 11 | 0 |

- **UNKNOWN:** Too few repeats among classified CFBs (1 of 97). No relation can be shown either way.

## What this says (no solution)

- **D7 is not a main driver of the 2026 rise.** True recurrence after fix is low and flat. The 2025-H2 repeat wave was one known DATA defect reported by many customers.
- **The bigger recurrence signal is fixes that break things:** about a quarter of named causes are earlier bug fixes, and fixes of customer bugs as causes are rising (Low-Medium).
- **Intake noise:** parallel reports and duplicates (7.5-11%) add volume without new defects.

## Limits

- Summary similarity misses repeats with different wording, and team re-homing splits pairs. So the rates are lower bounds.
- "Reopened" counts only the status name "Done", for all CFBs (MI not excluded). Exposure differs between years.
- Single AI reader for the precision check.
- Re-running the script drops the reopen rows. Add them again from `jql_counts` (purpose M2-D7).
