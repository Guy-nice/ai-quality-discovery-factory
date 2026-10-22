# Agent Reports - Round 2 (verbatim)

**Date:** 2026-10-22 | **Iteration:** 5 | Final reports of research forks, as returned. One security detail redacted (D-013). Synthesis: [findings-round-2](../../02-research/findings-round-2.md).

---

## R1b - Throughput jump causes

Files: `data/aggregates/r1b-throughput.csv`, `README-r1b.md`. Raw samples in /tmp deleted.

| Jump | Raw | Cause | Removed | Adjusted |
|---|---|---|---|---|
| Bugs 2024-Q1 | 10,993 | Project ENG bulk load: 4,738 bugs on 2024-01-01..07, 0 before | 5,088 | 5,905 (fits 2023-Q4 4,587, 2024-Q2 6,155) |
| Bugs 2026-Q3 | 18,014 | New project CGY, Azure DevOps import (5,441 labeled `ado-bug`), 0 before 2026-Q2 | 6,363 | 11,651 |
| Stories 2026-Q3 | 42,960 | CGY import of done items | 8,967 | 33,993 |

Other story growth drivers 2026-Q3 vs 2024-Q3: AI-labeled stories 5,898 vs 13 (17% of adjusted); new projects CXCA + CXIFW 1,386 vs 0; remaining growth ~+57% (28,095 vs 17,949), broad, no bot pattern.

| CFB/100 stories | Raw | Adjusted (CGY CFB = 0) |
|---|---|---|
| 2024-Q3 | 1.97 | 1.97 |
| 2025-Q2 | 1.22 | 1.22 |
| 2025-Q3 | 1.62 | 1.62 |
| 2026-Q2 | 1.68 | 1.68 |
| 2026-Q3 | 1.09 | 1.38 |

- EVIDENCE (High): both all-bug spikes are data-load artifacts (ENG 2024-01, CGY 2026-07). Do not use raw all-bugs as denominator.
- EVIDENCE (High): CGY inflates 2026-Q3 stories by 26%. Raw per-story drop -33% (2025-Q3 -> 2026-Q3) becomes -15%.
- EVIDENCE (High): 2026-Q2 per-story 1.68 vs 2025-Q2 1.22 = +38%. C-01 weaker than reported.
- EVIDENCE (High): AI/auto/CI labels on bugs 70 (2025-Q3) -> 2,367 (2026-Q3, without CGY). AI-labeled stories 13 -> 5,898. Main new volume source.
- HYPOTHESIS (Medium): AI work splits into more, smaller stories; inflates denominator. Story size not measured.
- HYPOTHESIS (Low): non-CGY bugs without these labels still +58% YoY (9,284 vs 5,866). No single project explains. More internal testing or more defects. Needs by-project count.
- Caveat: reporters human in >= 94% of samples (bulk import keeps original reporter); bot share does not show import.

---

## R2b - Pilot short-list

Recommended pilot: Orchestration Core VP, bounded to contact routing and lifecycle flow (routing bugs + stuck/lost contacts). Files: `data/aggregates/r2b-pilot-candidates.csv`, `README-r2b.md`. Scratch in /tmp deleted.

**Teams (CFB W_prev -> W_last)**. W_last complete (1,050 = exact VP totals). W_prev "s" = sample (549 of 605), others exact.

| VP | Team | W_prev | W_last | Change |
|---|---|---|---|---|
| Orchestration Core | Orchestration II | 18 | 66 | +267% |
| Orchestration Core | Orchestration | 31 | 58 | +87% |
| Orchestration Core | Advanced Omnichannel Routing | 23 | 40 | +74% |
| Orchestration Core | ACD Admin Pune + Bolivia | 50 | 43 | -14% (team renamed) |
| A&D | Hornet | 85 | 74 | -13% |
| A&D | Data-Sandy | 14 | 56 | +300% |
| A&D | Dragonfly / Waves | 3s / 2s | 39 / 32 | new load |
| A&D | Agni / Titans | 0s / 0s | 38 / 32 | new team names |
| A&D | Reporting-CBBA + Pune | 89 | 65 | -27% |
| WFM | Better Calls Devs | 22 | 71 | +223% |
| WFM | Nexus | 0s | 38 | new team name |
| WFM | Bugcide Squad | 24 | 28 | +17% |

| VP | P1/P2 prev -> last | Avg incidents/CFB | CFB with 5+ incidents |
|---|---|---|---|
| Orchestration Core | 58% -> 70% | 3.8 | 19% |
| A&D | 61% -> 68% | 3.1 | 17% |
| WFM | 43% -> 65% | 2.0 | 5% |

**Themes**
- Stuck/lost contacts: 245 CFB all time; W_prev 92 -> W_last 127 (+38%); 69% P1/P2 last 12 mo. By year: before 2024: 23; 2024: 3; 2025: 153; 2026 YTD: 66. Waves (Aug-Sep 2025, Dec 2025); falling in 2026. Last 12 mo: A&D 61%, Orch Core 31%. Avg 1.8 incidents/CFB (low). Label vs summary overlap: 173 label, 175 summary, 103 both.
- Routing: W_prev 40 -> W_last 106 (+165%), 62% P1/P2; spans 3 VPs (Orch Core 58, AHW 18, A&D 9).
- Reporting/data: 341 -> 534 (+57%); summary keywords too wide for a bounded flow.
- Other theme labels (last 12 mo, 3 VPs): WFM_QM_PARITY 12, wrong_routing 6, Race_conditions 4, Resilience_26 4.
- AI labels: 106 of 159 AI-labeled CFBs in these 3 VPs.

**Scoring (/50; weights density 3, criticality 3, growth 2, boundary 2)**

| Candidate | Density | Criticality | Growth | Boundary | Total |
|---|---|---|---|---|---|
| Orchestration Core | 4 | 5 | 4 | 1 | 37 |
| A&D | 5 | 4 | 3 | 1 | 35 |
| Routing flow | 2 | 3 | 5 | 5 | 35 |
| WFM | 4 | 3 | 5 | 1 | 33 |
| Stuck/lost flow | 2 | 3 | 2 | 5 | 29 |

**Why Orchestration Core + routing/lifecycle flow:** highest severity (70% P1/P2) and incident load (19% with 5+); holds 55% of routing CFBs and 31% of stuck/lost; bounded flow that crosses into AHW and A&D; matches round-1 RCA profile (most scale/race escapes, 9/33); rank 1 also without boundary weight (35 vs A&D 33). Changes D-009: stuck/lost is part of the flow, not main pilot (waves, falling in 2026, low incident load).

**Could make pick wrong:** routing theme is summary keyword (over/under count); team renames inflate growth; invalid share per VP not removed; incident-count field completeness unknown, routing incident load not measured; weights are judgment (A&D 35 close).

---

## R6 - Controls inventory

Files: `data/aggregates/r6-controls.csv`, `r6-ria-regression.csv`, `README-r6.md`. Raw dumps deleted.

| Control | Where | Fill | Class |
|---|---|---|---|
| Acceptance Criteria | Epic / Story | 100% / 88% (sample 40) | Policy, enforcement UNKNOWN |
| RIA real content | Epic | 58% (17 filled + 6 partial / 40) | Policy, not blocking |
| RIA real content | Story | 0% (39/40 template) | Policy, not used |
| RIA real content | CFB fix | 88% (35/40) | Policy, not blocking |
| RCA real content | CFB fix | 89% (n=240, R5) | Policy |
| RCA Review Status set | CFB | 33% (483/1,464) | Policy review |
| EOR Broken? / Mitigation? | Epic, CFB | 0% real | Not used |
| Quality Review Status | Epic / Story | 1.6% / 0.4% | Rare |
| Architecture Review Status | Epic | 2.0% | Rare |
| Code Review Status | Story | 0.3% | Not used in Jira |
| QPlan, Escape Analysis, Test Stage found, Gating, Reopen Counter | Epic / CFB | 0-0.6% | Not used |
| Automated = Yes | CFB fix | 0.8% | Rare |
| Xray Test link | Epic / Story / CFB fix | 25% / 18% / 30% (sample) | Suggested |
| Domain Go/No-Go (9 exit criteria) | Confluence, 26.4 per domain | Status TBD on all 26.4 pages | Policy, human release gate |
| SonarQube pre-push hook + Claude Code hook | Confluence IN 4260561248, 4259546714 (2026-10-17) | Opt-in | Real control only if installed; CI Sonar gate exists, enforcement UNKNOWN |
| Aikido pre-push hook | IN 4260495956 | Opt-in | Real control if installed (dependency security) |
| Mutation Testing Agent program | CX 4201808311 | Rollout | Suggested, enforcement planned |
| SRE/NOC/Capacity Go/No-Go | IN 4266983661 | Template | Policy |

**RIA done-but-missed vs not done (n=20 regression CFBs):** 14/20 name causing item in RCA text; only 2/20 have formal "is caused by" link. Of 14: RIA done but missed 7, RIA not done 7. By type: Epic 5/5 RIA content, Story 0/7, Bug 1/5. 5/17 causing items Implemented by AI Agent = Yes.

**Xray:** Tests created 2024 89,063; 2025 73,738; 2026 137,018 (to 10-22). Test Executions 2025 608,375; 2026 1,147,557. Heavy use; test links to Epics/Stories weak.

**AI fields:** "Implemented by AI Agent" (cf_15229) exists. Stories Yes: 2025 523; 2026 21,518 (19.7%). 2026 by quarter: Q1 9.3%, Q2 28.4%, Q3 19.5%. Bugs resolved 2026: 10.2%; CFB resolved 2026: 12.0%. Other AI fields (AI Model Used, Lines Added by AI, PR URL) ~2.6% of stories. Non-AI stories also grew Q3 (34.6k vs 23.6k 2025-Q3).

**Confluence pages:** Domain Go/No-Go 26.4 pages all status TBD: WFM 4213637494, APQ 4213768850, Orchestration Core 4213801473, A&D 4213801452, AHW 4213768829, LiveVox 4213310045, VMS 4213637473 (+ A&D sub-domains). TEMPLATE Domain Go/No-Go 4213702945 (2026-10-20): 9 exit criteria (feature toggles, regression, exploratory, unified performance gate, P1-P3 closed, synthetics, deploy/rollback, infra prerequisites, high-risk items). CXone Usage Model Tracker RISK items 4263837969 (21 risk rows). Mutation Agent Testing 4201808311. Sonar/Aikido hooks as table. XCX project pages (PUB1075, AT&T Redaction, CXAI Hybrid Data Model) are per-initiative trackers; no XCX Quality Process page found.

**Observations**
1. EVIDENCE (High): most Jira quality fields exist but are not used (9 of ~15 under 2%). Policy on paper, not controls.
2. EVIDENCE (Medium): RIA at Epic level and CFB fixes, not at Story level (0/40). Regressions come from Stories/Bugs as much as Epics.
3. EVIDENCE (Medium, n=14): half of regressions had RIA that missed, half had none. "Enforce RIA" alone covers at most half.
4. EVIDENCE (High): release Go/No-Go is human gate with 9 criteria. Only blocking automated controls found are opt-in local hooks (Sonar, Aikido).
5. EVIDENCE (High): AI attribution field filled on ~20% of 2026 stories; AI-vs-non-AI defect comparison possible. Resolves part of U-17.
6. HYPOTHESIS (Low): some RIA text on AI-implemented Epics reads AI-generated; quality untested.

**Out of scope:** one Jira issue holds plain-text credentials. [REDACTED - reported to lead, D-013.]

---

## R7 - AI label semantics

Files: `data/aggregates/r7-ai-labels.csv`, `README-r7.md`.

**Verdict:** AI label on a bug = AI made the fix, not AI code caused the bug. Confidence High.

**Evidence:**
- Confluence 3915612323 (AI Metrics Automation): GitHub Action adds `AGENTIC_AI_CODE` when Claude Code opens the PR; on merge changes to `AGENTIC_AI_CODE_<pct>` (share of AI-written lines).
- Confluence 4011230379 (PgM Automations): monthly "AI Usage" KPI audit sets "Implemented by AI Agent" (cf[15229]) = Yes on Epics/Stories with AI clues.
- Changelogs 7/7 CFBs: label and "AI Model Used" set after bug creation, during/after fix; 2/7 after resolution.

**Data problems:** labels are KPI adoption metric, also back-added (587 issues created before 2025 have the label, some 2017 epics); 14 label variants in CFB sample, no standard; 15/100 AI-labeled CFBs have Implemented by AI Agent = No.

**Adoption proxy (resolved stories with AI indicator):**

| Quarter | AI stories | All stories | AI % |
|---|---|---|---|
| 2025-Q1 | 43 | 19,883 | 0.2 |
| 2025-Q2 | 58 | 22,676 | 0.3 |
| 2025-Q3 | 92 | 23,573 | 0.4 |
| 2025-Q4 | 454 | 22,847 | 2.0 |
| 2026-Q1 | 2,587 | 25,472 | 10.2 |
| 2026-Q2 | 9,900 | 31,595 | 31.3 |
| 2026-Q3 | 9,813 | 42,960 | 22.8 |

Non-AI stories also grew 23,481 (2025-Q3) -> 33,147 (2026-Q3). Surge is not only AI.

**AI vs non-AI defect comparison:** not via Jira links (only 2.7% of CFBs, 47/1,760, have "created by"/"is caused by"). RCA text better: "How was it introduced" names a Jira key in 31/100 fixed 2026 CFBs. Pilot: 9/27 causing items resolved 2026 (33%) have AI indicator vs base 22%. Too small, mixes types. Confidence Low.

**How to make it possible:** (1) extract causing keys from RCA text of all fixed CFBs (~700/yr); (2) keep causing Stories and Bugs; (3) compare CFB rate per AI vs non-AI story by quarter and team, control for teams that under-label (not on metrics workflow); (4) better data: RCA question "Was causing change AI-implemented?" + require Defect "created by" link.
