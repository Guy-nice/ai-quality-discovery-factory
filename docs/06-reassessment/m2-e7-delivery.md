# M2-E7 - Delivery and Release Outcomes

**Date:** 2026-10-25 | **Window:** 2025-01..2026-10 (2026-10 partial) | **Exclusion:** MI-investigation tickets (D-032); valid = invalid resolutions excluded
**Data:** `delivery_monthly`, `cfb_fix_channel`, `release_events` in `quality.sqlite`; [m2-e7-delivery.csv](../../data/aggregates/m2-e7-delivery.csv); script `scripts/db/m2_e7_delivery.py`

## Release model (from Jira fix versions)

Quarterly combined / pipeline releases (25.1 ... 26.4, 27.1), cumulative updates (CU, e.g. 26.3.4), breakfix versions (4-part, e.g. 26.3.1.3, "BF"), sprint releases (CX.26.4.196), product versions (Agent, PM, CXWS). GitHub release tags exist only after the TFS migration (2026), so they are not used.

## Findings

| H1 2025 vs H1 2026 | H1 2025 | H1 2026 |
|---|---|---|
| Valid CFB (excl. MI) | 313 | 400 |
| Emergency changes (ServiceNow) | 543 | 854 |
| Fixed CFB shipped via breakfix | 8.8% | 7.6% |
| Fixed CFB shipped via CU | 39.6% | 20.8% |
| CFB with known cause introduced <= 90 days before | 21 of 74 (28%) | 32 of 78 (41%) |

| Jun-Sep | 2025 | 2026 |
|---|---|---|
| Emergency changes | 459 | 1,336 (x2.9) |
| Emergency share of normal + emergency | ~7.5% | 13.5-24.2% by month |
| Valid CFB (excl. MI) | 262 | 327 (+25%) |

- **EVIDENCE (High):** Emergency changes rose sharply from 2026-06 (136 -> 269 -> 366 -> 377 per month). Normal-change failure rate stayed flat to lower (3.9% -> 2.6%, from the ServiceNow fork).
- **CORRELATION (Medium):** Monthly emergency changes and valid CFBs move together (Spearman 0.66, 21 months). The link is slightly stronger from CFB to next-month emergency changes (0.75) than the other way (0.65). This fits "emergency changes are a reaction to defects" better than "emergency changes cause defects". Direction is NOT proven.
- **EVIDENCE (Medium):** Breakfix (out-of-band) share of fixes is flat (~7-9%). The CU share fell by half (40% -> 21%) in 2026. **HYPOTHESIS (Low):** the fix-delivery model changed (more fixes ride sprint / major releases, or urgent fixes move to emergency changes outside Jira versions).
- **EVIDENCE (Low-Medium, small n):** Among CFBs with a known causing change, the share introduced within 90 days rose from 28% to 41%. More escapes now come from recent changes. Right-censoring favors short latencies in 2026, so the true rise is smaller.
- **EVIDENCE (Medium):** Escape latency (causing change resolved -> CFB created) has a median of about 100-200 days by month. Many defects reach customers months after the change.
- **EVIDENCE (Medium):** Median time to fix a breakfix CFB is 6 days, vs 8-13 days overall.

## Change failure proxy

No direct change -> incident link exists (`caused_by` on 0.6% of P1s). Two proxies are used. Both are partial:
1. ServiceNow normal-change failure rate ("failed" outcome): 3.9% -> 2.6%. This is self-reported by the change owner.
2. Share of valid CFBs with a known causing change introduced within 90 days: 28% -> 41% (n about 75 per half-year).

## Limits

- ServiceNow change counts are org-wide (infrastructure and product). They cannot be split by service with the current role.
- Release counts include only versions that a fixed CFB references. They are not a full release calendar.
- The causing change is known for only about 25% of fixed CFBs (RCA text + links).
- ServiceNow record access is missing (U-26). It blocks the change -> incident link.

## Questions this raises (for investigation, not solutions)

- Why did emergency changes almost triple from 2026-06? Which services, and are they fixes for customer defects?
- Did the CU model change in 2026?
