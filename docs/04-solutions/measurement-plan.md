# Measurement Plan - S1 to S7

**Date:** 2026-10-22 | **Script:** `scripts/db/metrics.py` -> DB table `metrics_monthly` | **Refresh:** monthly, after the data pull

| ID | Measure | Baseline (last 12 mo) | Target | Read as |
|---|---|---|---|---|
| S1 | Valid pilot CFB per month | 8.9 (13 per month in 2026-05..10) | <= 9 within 2 quarters | monthly |
| S2 | Race / ordering share of classified pilot RCAs | about 23% (blind re-read) | < 15% | rolling quarter (monthly n < 15) |
| S3 | Incidents per pilot CFB | 3.8 | <= 2.5 | monthly |
| S4 | Pilot RCAs with a monitoring action | 3% | >= 30% | rolling quarter |
| S5 | Minimum bus factor on top-10 pilot hotspots | **1** (InterVCCommWrapper/Messages) | >= 3 | quarterly (R14 re-run) |
| S6 | Pilot-repo commits that name a Jira key | 51-85% by month | >= 80% every month | monthly |
| S7 | Invalid share of pilot CFBs | 51% | < 35% | monthly |

## Rules

- Same queries as the frozen baseline (D-020: valid = invalid resolutions excluded, case-insensitive).
- New RCAs are classified with the same rubric. Each quarter, a second blind rater checks 20 RCAs (agreement must stay >= 80%).
- A change in a measure counts only when it holds for 2 consecutive periods.
- AI split: S1 and S3 are also reported for AI vs non-AI causing changes (R8 method), and re-tested with a 90-day window in 2027-Q1 (D-025).

## Monthly data (2026)

See `metrics_monthly` in `data/db/quality.sqlite`. The 2026 months show the step: S1 was 2-7 per month in January to April, and 10-17 per month in May to October.
