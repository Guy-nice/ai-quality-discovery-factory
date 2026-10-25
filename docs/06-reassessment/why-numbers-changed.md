# Why the Numbers Changed (Before vs After)

**Date:** 2026-10-25 | **Decision:** D-032 | **Data:** `data/db/quality.sqlite` (issues + local summaries)

## 1. The headline: +51% -> +29%

| H1 2026 vs H1 2025 | Before | After | Why |
|---|---|---|---|
| Customer-found bugs (CFB) | +51% (574 -> 864) | **+29%** (571 -> 736) | 128 MI-investigation tickets removed from H1 2026 |
| P1/P2 CFBs | +72% (296 -> 509) | **+46%** (293 -> 427) | 82 of those 128 tickets are P1/P2 |
| Valid CFBs | +41% (316 -> 447) | **+28%** (313 -> 400) | 47 of them are closed as fixed (valid) |
| Valid P1/P2 | +63% (168 -> 274) | **+43%** (165 -> 236) | - |

### What happened

In March 2026, a new intake practice started. After a **major incident (MI)**, an investigation ticket is created in Jira as a **Bug** with the customer Salesforce case attached. The CFB query (`issuetype = Bug and salesforceAssociatedTypes is not EMPTY`) cannot tell these apart from product defects.

| Month | MI-investigation tickets |
|---|---|
| 2025 (whole year) | 3 |
| 2026-03 | 6 |
| 2026-04 | 49 |
| 2026-05 .. 2026-09 | 34-48 per month |
| 2026-10 (to the 22nd) | 17 |

### Why the effect is so large

1. **The baseline has almost none.** H1 2025 had 3 such tickets, so all 128 in H1 2026 appear as growth. They are **44% of the added CFBs** (128 of 290).
2. **They are mostly high priority.** 149 of 270 are P2. So they inflate the P1/P2 rise more: **38% of the added P1/P2** (82 of 213).
3. **Many are not defects.** Resolutions: 68 "Not a bug", 46 "Duplicate", 21 "Won't Fix", 52 "Fixed", 23 "Fixed - Config". So the effect on *valid* CFBs is smaller, but still visible.
4. **They concentrate in the pilot.** Orchestration Core has 82, Analytics and Data 49, LiveVox & Digital 30.

### Why it was missed before

- The trend check looked for **bulk imports by project** (it found ENG and CGY). MI tickets are spread across 48 projects at about 40 per month, so no single project spike showed them.
- The CFB definition was taken as given and never checked for **changes in what enters it**.
- They became visible only when every valid CFB was read and classified by failure type: "availability" CFBs jumped from 17 to 75, and 60 of the 75 were MI tickets.

### What still holds

- Customer-reported defects **did rise** in 2026: +29% overall, +46% P1/P2.
- The pilot step is **real**. Without MI tickets, valid in-flow pilot CFBs go from 4.0 per month (Jan-Apr 2026) to 10.2 per month (May-Oct 2026).
- **Not explained yet:** ServiceNow P1 incidents from the customer channel fell by about half in 2026 (C-08). A change in priority rules is possible.

### Remaining uncertainty

- The pattern (`MI ...`, "Investigatory KI", `MI-<number>`, "major incident") may miss variants. A wider pattern finds about 10 more candidate tickets in 2026, so the effect on the numbers is under 2%.

## 2. All earlier corrections (one table)

| # | Claim before | Claim after | Cause of the error | Decision |
|---|---|---|---|---|
| 1 | Pilot CFBs +77% | Valid pilot CFBs +34% | Invalid closures (duplicates, not a bug) counted | D-020 |
| 2 | CFB per story -33% (quality "improved") | -15% (Q3), +38% (Q2) | Bulk imports (projects ENG 2024-01, CGY 2026-Q3) in the story count | D-011 |
| 3 | Monolith not in GitHub (TFS needed) | Monolith in `inContact/inContact` since 2021 | Did not search Confluence for the migration | D-017 |
| 4 | Almost no concurrency tests (4 of 1,349) | Concurrency tests exist in EM and AFM | Counted file names, not file content | R17 |
| 5 | Race / ordering share 29% | About 23% | A blind re-read moved some cases to load-only | R17 |
| 6 | CFB +51%, P1/P2 +72% | +29%, +46% | MI-investigation tickets counted as defects | D-032 |

## 3. Pattern behind the errors

The errors share 3 causes:

1. **The population definition was not audited.** It was not checked over time: imports, intake process changes, and closure types.
2. **A single source was trusted.** The second source (ServiceNow) was available only late, and it now contradicts one claim (C-08).
3. **Proxies were trusted.** File names, a project volume or a label stood in for the thing itself.

## 4. Research checks now applied (to the research, not to the product)

| Check | How |
|---|---|
| Composition audit per period | Before any trend: counts by project, issue type, summary pattern, reporter and resolution, per month |
| Exclusion list in code | MI pattern and invalid set applied in every script (`metrics.py`, mission v2 forks) |
| Two sources before a headline | A trend is reported as High confidence only if a second source agrees |
| Content over proxies | Read samples before trusting a name, label or field |
| Correction log | Every change of a reported number gets a row in section 2 |
