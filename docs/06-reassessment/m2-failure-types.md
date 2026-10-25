# M2 - Failure Types and Customer Impact (Q-B, E4)

**Date:** 2026-10-25 | **Scope:** all **valid** CFBs created 2025-01-01..2026-10-22 (n = 1,565; invalid resolutions excluded) | **Data:** `failure_types`, `agg_m2_failure_types` in `quality.sqlite`; `data/aggregates/m2-failure-types.csv` | **Script:** `scripts/db/m2_failure_types.py` + `m2_failure_overrides.csv`

## 1. Taxonomy (13 types)

| Type | Definition | Business correctness |
|---|---|---|
| DATA | Wrong, missing, stale or inconsistent data in reports, real-time dashboards, data share, admin records | Y |
| ROUTING | Contact goes to wrong agent/skill, not routed, wrong priority/order | Y |
| LIFECYCLE | Live contact stuck, lost, dropped, dead air, transfer/hold failure | Y |
| RECQM | Recording missing/wrong, QM evaluation/analytics wrong, AI output (summary, transcript) wrong | Y |
| AGENTSTATE | Agent state/session wrong (status, ACW, logout) | Y |
| WFM | Schedule, forecast, adherence, time-off result wrong | Y |
| BILLING | Usage, billing, license count wrong | Y |
| FUNC | Feature fails with an error; no wrong-data outcome | N |
| UI | Display, layout, localization, usability | N |
| AVAIL | Outage, cannot log in or load, service degradation | N |
| INTEG | API / CRM / Studio-action / third-party contract breaks | N |
| PERF | Slow, latency, timeout | N |
| SECURITY | Permission, access control, data exposure | N |

**Method:**
1. Keyword rules on the summary, then on the RCA text if the summary has no hit.
2. A project rule: in dashboard/reporting projects, "stuck contact" means stale display state, so DATA.
3. **All 1,565 summaries were read**, and 769 labels were corrected by hand.
4. Precision on 40 random final labels: **37-38 / 40 (93-95%)**. The main ambiguity is DATA vs FUNC.

## 2. Impact per type

Impact score = sum over CFBs of max(incidents, 1) × (2 if P1/P2, else 1). It is a ranking aid only. The weights are a choice. Count and incident sum are also shown.

| Type | Valid CFB | 2025* | 2026* | P1/P2 % | Incidents | Avg inc. | 5+ inc. % | Median days | Impact |
|---|---|---|---|---|---|---|---|---|---|
| **DATA** | 399 | 161 | 182 | 66 | 1,239 | 3.1 | 14 | 13 | **2,159** |
| FUNC | 354 | 121 | 190 | 57 | 1,331 | 3.8 | 14 | 8 | 2,048 |
| UI | 208 | 92 | 101 | 38 | 663 | 3.2 | 12 | 8 | 926 |
| AVAIL | 101 | 17 | 75 | 62 | 424 | 4.5 | 31 | 7 | 693 |
| **ROUTING** | 86 | 33 | 46 | **73** | 356 | 4.2 | 20 | 11 | 679 |
| PERF | 50 | 20 | 29 | 60 | 368 | 7.7 | 21 | 7 | 677 |
| **RECQM** | 111 | 43 | 60 | 52 | 322 | 2.9 | 9 | 8 | 468 |
| **LIFECYCLE** | 75 | 24 | 46 | 65 | 278 | 3.7 | 16 | 9.5 | 389 |
| INTEG | 87 | 41 | 36 | 66 | 166 | 1.9 | 9 | 6 | 286 |
| **WFM** | 33 | 15 | 16 | 30 | 164 | 5.1 | 16 | 13 | 282 |
| **AGENTSTATE** | 18 | 8 | 8 | 44 | 198 | **11.0** | 28 | 11.5 | 232 |
| SECURITY | 39 | 10 | 23 | 80 | 62 | 1.6 | 5 | 11 | 117 |
| **BILLING** | 4 | 0 | 4 | 100 | 19 | 4.8 | 25 | 15 | 38 |
| **All correctness** | **726 (46%)** | 284 | 362 | **62.5** | 2,576 | 3.6 | 15 | **12** | 4,247 |
| All other | 839 | 301 | 454 | 55.1 | 3,014 | 3.7 | 15 | 8 | 4,747 |

\* Same window: Jan 1 - Oct 22.

**By R&D VP, correctness share of valid CFBs:** Orchestration Core 63%, A&D 59%, VMS/Recording/QM 58%, LiveVox & Digital 44%, WFM 39%, APQ 36%, AHW 24%.

## 3. Analytics and Data (E4)

398 valid CFBs; 152 -> 187 in the same window (+23%). 59% are correctness failures.

| Sub-theme | n | 2025* | 2026* | P1/P2 % | Avg incidents | 5+ inc. % |
|---|---|---|---|---|---|---|
| A1 Stale/stuck contact state on real-time dashboards | 121 | 61 | 26 | 68 | 1.7 | 7 |
| A2 Wrong or missing metric values in reports/widgets | 85 | 26 | **50** | 72 | **5.8** | 20 |
| A3 Data share / lake / pipeline / feeds | 13 | 4 | 9 | 85 | 2.3 | 15 |
| A4 Report/dashboard fails, slow or unavailable | 121 | 43 | **70** | 66 | 4.3 | 20 |
| A5 UI / display | 22 | 7 | 13 | 59 | 4.8 | 18 |
| Other (INTEG, RECQM, SECURITY, BILLING) | 36 | | | | | |

- **EVIDENCE (Medium):** A1 (stale contacts) **fell** from 61 to 26. A2 (wrong metric values) **doubled**, from 26 to 50, with a high incident load (5.8 per CFB).
- **EVIDENCE (Low, n=41, round-1 RCAs):** A&D escape causes: missing test coverage 11, third-party/integration 7, deployment/release 6, scale/race 5, RIA miss 4.

## 4. Answer to Q-B: business-correctness failures that hurt customers most

| Rank | Failure type | Why (evidence) | Confidence |
|---|---|---|---|
| 1 | **Wrong / missing / stale data in reports and real-time dashboards (DATA)** | Largest volume (399, 25% of valid CFBs), highest impact score, 66% P1/P2, slowest to fix (median 13 days). In A&D, wrong metric values doubled in 2026. | Medium-High |
| 2 | **Routing correctness (ROUTING)** | Highest P1/P2 share of all correctness types (73%); 20% have 5+ incidents; +39% (33 -> 46). | Medium |
| 3 | **Contact lifecycle: stuck, lost, dropped, dead air (LIFECYCLE)** | +92% (24 -> 46); 65% P1/P2. | Medium |
| 4 | **Recording / QM / AI-output correctness (RECQM)** | +40% (43 -> 60); it includes AI summary and transcript errors. | Medium |
| 5 | **Agent state correctness (AGENTSTATE)** | Few (18), but the highest blast radius: 11 incidents per CFB, 28% with 5+. | Low-Medium (small n) |

Business correctness is **46% of valid CFBs**. It has a higher P1/P2 share (62.5% vs 55.1%) and takes longer to fix (median 12 vs 8 days).

## 5. Limits and confounders

- **CFB = customer-reported only.** Silent correctness errors stay invisible. Billing (4 CFBs) is the most likely blind spot: customers may report billing problems through other channels. Not tested.
- **AVAIL rise (17 -> 75) is partly a process change.** 60 of 75 AVAIL CFBs in 2026 are MI-investigation tickets ("MI ...", "Investigatory KI"), vs 1 in 2025. In total, MI-type CFBs went from 3 (2025) to 110 (2026). Do not read the AVAIL growth as a real outage trend without ServiceNow MI data.
- The "Number of Incidents" field is empty on 25 of 1,565. Its exact meaning (linked customer cases vs ServiceNow incidents) is not confirmed.
- Single rater (AI). Labels come mostly from summaries. DATA vs FUNC has the most ambiguity.
- No free text from Jira is stored in committed files.
