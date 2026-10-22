# R8 - AI-implemented vs non-AI changes: CFB-causing rate

**Date:** 2026-10-22 | **Tests:** H-11 / P-04 | **Source:** SRC-001 Jira (read-only) | **DB:** `data/db/quality.sqlite` | **Output:** `data/aggregates/r8-ai-vs-nonai.csv` (table `agg_r8_ai_vs_nonai`)

## 1. Question

Do changes implemented by an AI agent cause more customer-found bugs (CFB) per change than other changes?

## 2. Method

1. **Population:** all CFBs created 2025-01-01..2026-10-22. `issuetype = Bug and salesforceAssociatedTypes is not EMPTY and created >= "2025-01-01"`. JQL count 2,811, loaded 2,811. Pulled in monthly / half-month windows (exact JQL per file in `query_log`).
2. **Causing item:**
   - `rca_text`: Jira keys in the RCA section "How was it introduced" of fixed CFBs (`scripts/db/extract_causes.py`).
   - `issuelink:is_caused_by`: Problem/Incident link, inward.
   - `issuelink:created_by`: Defect link, inward. This source is secondary.
3. **AI flag:** "Implemented by AI Agent" (cf_15229) on the causing item. `Yes` = AI. Not-AI = `No` or empty.
4. **Rate:** distinct causing items resolved in a quarter / all items of the same type resolved in that quarter (JQL counts, `project not in (CGY, ENG)` per D-011).
5. **Rate ratio (RR)** AI / not-AI, 95% CI by the log method.
6. **Exposure:** CFBs created up to 2026-10-22. Items resolved in 2026-Q3 have had only a short time to cause CFBs, so the pooled main window is 2026-Q1..Q2.

## 3. Data loaded (DB row counts)

| Table | Rows | Note |
|---|---|---|
| issues (CFB, created 2025+) | 2,811 | = JQL count |
| issues (causing items) | 412 | of 441 distinct causing keys; 18 keys from projects outside the CFB set not pulled; 11 invalid/inaccessible |
| issue_links | 3,229 | all links on pulled issues |
| causal_links | 475 | rca_text 370 (316 CFBs), is_caused_by 23, created_by 82 |
| jql_counts (R8) | 46 | denominators, `scripts/db/r8_counts.sh` |
| query_log (R8) | 45 dumps | 3,308 issue rows loaded (with overlap) |
| raw_local.sqlite issue_text | 3,192 | RCA/RIA/summary text, **local only, gitignored** |

## 4. Extraction quality

- Fixed CFBs: 1,209. RCA has an "introduced" section: 1,088. Section names a key: 316 (26%).
- **Precision, manual check n=20: 19/20 (95%) EVIDENCE (Medium).** One miss: a key that names an earlier patch ticket, not the origin.
- Causing items by type: Epic 122, Story 105, Bug 90, Task 62, Capability 12, Test 10, Test Execution 7, Sub-task 4.

## 5. Results

### 5.1 Story + Bug, per quarter of causing-item resolution

| Quarter | AI causing / resolved | Not-AI causing / resolved | RR | 95% CI |
|---|---|---|---|---|
| 2025-Q1 | 0 / 43 | 10 / 24,477 | - | - |
| 2025-Q2 | 0 / 51 | 18 / 27,673 | - | - |
| 2025-Q3 | 0 / 71 | 10 / 28,804 | - | - |
| 2025-Q4 | 2 / 389 | 16 / 27,444 | 8.82 | 2.03-38.2 |
| 2026-Q1 | 3 / 2,819 | 26 / 28,377 | 1.16 | 0.35-3.84 |
| 2026-Q2 | 10 / 10,041 | 16 / 29,325 | 1.83 | 0.83-4.02 |
| 2026-Q3 (short exposure) | 7 / 10,012 | 14 / 36,010 | 1.80 | 0.73-4.45 |

### 5.2 Pooled and sensitivity

| Scope | AI rate /1000 | Not-AI rate /1000 | RR | 95% CI |
|---|---|---|---|---|
| **Main: Story+Bug, 2026-Q1..Q2** | 1.01 | 0.73 | **1.39** | **0.75-2.59** |
| Story+Bug, primary sources only | 1.01 | 0.73 | 1.39 | 0.75-2.59 |
| Story+Bug, 2026-Q1..Q3 | 0.87 | 0.60 | 1.46 | 0.88-2.44 |
| (a) Reviewed items only (Yes vs No), Q1..Q2 | 1.01 | 1.10 | **0.92** | 0.45-1.88 |
| (a) Reviewed items only, Q1..Q3 | 0.87 | 0.85 | 1.03 | 0.57-1.86 |
| (b) Stories only, Q1..Q2 | 0.80 | 0.50 | 1.61 | 0.74-3.49 |
| (b) Bugs only, Q1..Q2 | 2.54 | 1.50 | 1.69 | 0.58-4.95 |
| Epics, 2026-Q1..Q3 | 1.43 | 1.19 | 1.21 | 0.53-2.73 |
| Epics reviewed only (Yes vs No) | 1.43 | 1.41 | 1.02 | 0.38-2.74 |
| (c) VP AHW, Story+Bug Q1..Q3 | 0.63 | 1.26 | 0.50 | 0.11-2.36 |
| (c) VP APQ | 0.93 | 0.38 | 2.44 | 0.69-8.66 |
| (c) VP Analytics and Data | 1.50 | 1.10 | 1.36 | 0.38-4.95 |
| (c) VP Orchestration Core | 1.72 | 2.02 | 0.85 | 0.27-2.64 |
| (c) VP WFM | 0.88 | 0.81 | 1.08 | 0.36-3.23 |

### 5.3 Bias checks

| Check | Result | Reading |
|---|---|---|
| Detection: share of fixed CFBs whose RCA names a causing key | AI-made fix 27% (45/169) vs other 26% (269/1,020) | No difference in naming by fix type. EVIDENCE (Medium) |
| Detection by VP | AHW 41%, LiveVox 40%, Orch Core 35%, APQ 31%, VMS 32%, WFM 16%, A&D 9% | **Strong VP difference.** A&D and WFM rates are under-counted. EVIDENCE (High) |
| Exposure (median days causing resolved -> CFB created, 2026 items) | AI 28 d (n=22) vs not-AI 42 d (n=63) | AI items are more recent. Short exposure works **against** finding AI CFBs. |
| Reviewed vs unreviewed | Not-AI rate: reviewed (`No`) 1.10 vs all not-AI 0.73 per 1000 | Unreviewed items have fewer causal links. The crude RR 1.39 comes mostly from this mix. |

## 6. Verdict on P-04

- **EVIDENCE (Medium):** With current data, AI-implemented changes do **not** show a higher CFB-causing rate than comparable non-AI changes. Among reviewed items (Yes vs No), RR = 0.92 (2026-Q1..Q2) and 1.03 (2026-Q1..Q3). Epics: RR 1.02.
- **EVIDENCE (Medium):** The crude RR of 1.39-1.46 is not significant (CI includes 1). It drops to about 1.0 when the comparison is limited to items the AI audit reviewed.
- **HYPOTHESIS (Low):** A small effect (RR below about 2) cannot be excluded. Power is low: 13-29 AI causing items.
- **Verdict: P-04 NOT SUPPORTED at the per-change level. Confidence: Low-Medium.** The 2026 CFB rise is not explained by a higher defect rate per AI change. It fits better with **volume**: more changes in total (AI and non-AI), with the same per-change escape rate. This links to P-02.

## 7. Limits and what could invalidate this

- Only 26% of fixed CFBs name a cause. Attribution is a sample, not the full population, and it is biased by VP (A&D 9%).
- The AI flag comes from a monthly audit. Items that were AI-made but not audited count as "not-AI" (misclassification). The reviewed-only analysis addresses this in part.
- Short exposure for 2026-Q2/Q3 items. Their CFBs can still arrive and change the RR.
- The causing item is named by the owning team, so it is self-reported.
- Epic-level AI flag: an Epic can be partly AI-made.
- Would invalidate: the RR among reviewed items rising above 1.5 with a CI above 1 after 2 more quarters of exposure; or a full-population cause attribution (not a 26% sample) showing a different pattern.

## 8. Next data needed

1. RCA template question: "Was the causing change AI-implemented? (Yes / No / Unknown)".
2. Require a "caused by" link on every fixed CFB (now 26% by text, 2.7% by link).
3. Re-run R8 in 2027-01 (more exposure; `scripts/db/r8_analysis.py` re-runs from the DB).
4. Add line-level AI share (`AGENTIC_AI_CODE_<pct>`) as a dose variable.
5. Per-team AI denominators for teams on the metrics workflow.

## 9. Reproduce

```
python3 -I scripts/db/extract_causes.py --sample 20
sh scripts/db/r8_counts.sh            # denominators -> jql_counts
python3 -I scripts/db/r8_analysis.py   # -> data/aggregates/r8-ai-vs-nonai.csv
```
