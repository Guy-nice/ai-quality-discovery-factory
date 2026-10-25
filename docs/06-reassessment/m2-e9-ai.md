# M2-E9 - AI Role: Facts, Correlations, Causal Hypotheses

**Date:** 2026-10-25 | **Data:** 1,663 merged PRs in 13 pilot repos (590 AI), 2025-01..2026-10; 1,475 valid non-MI CFBs (D-032); 306 CFB-fix commits; 94 reverted PRs; 1,751 PR-linked Jira items | **Script:** `scripts/db/m2_e9_ai.py` | **Tables:** `ai_matched`, `ai_event_study`, `agg_m2_e9_ai`

No assumption that AI caused the decline. Outcome = a later commit that fixes a **valid, non-MI customer-found bug** and touches the same files as the PR ("follow-up fix").

## 1. Stronger designs (window: PRs from 2025-Q4)

| Design | Follow-up fix 90 d (PRs <= 2026-07-25) | Follow-up fix 30 d | Reverted |
|---|---|---|---|
| Matched within repo x size x hotspot x quarter | **RR 0.84** (0.64-1.11) | 0.73 (0.49-1.07) | 1.07 (0.46-2.52) |
| Matched within team x size x quarter | **0.78** (0.55-1.10) | 0.73 (0.42-1.29) | 1.46 (0.65-3.27) |
| Within the same author x size | **1.45** (0.98-2.14) | 0.57 (0.31-1.05) | 1.30 (0.45-3.73) |

- No design shows a significant difference. Within-repo and within-team designs point to fewer follow-up fixes for AI PRs. The within-author design points the other way at 90 days, and the opposite way again at 30 days.
- The within-author design uses only the 82 authors with both AI and non-AI PRs. 39 authors use only AI. If authors who adopt AI work on riskier code, between-author designs favor AI; the within-author design removes that bias but has less power.

**Staggered adoption.** The adoption month is the first month with at least 5 PRs and at least 20% AI PRs. 9 repos adopted between 2025-10 and 2026-08.

| Unit | Before (6 mo) | After (6 mo) | Ratio |
|---|---|---|---|
| Adopting repos: CFB-fix commits per commit | 60 / 1,174 | 57 / 2,323 | 0.48 (0.33-0.69) |
| Not-yet-adopted repos, same months | 480 / 8,401 | 161 / 4,386 | 0.64 (0.54-0.77) |
| Ratio of ratios | | | **0.75** |
| 28 adopting teams: valid non-MI CFBs (count, no workload) | 83 | 79 | 0.95 |
| All valid non-MI CFBs, same calendar span (reference) | 378 | 470 | 1.24 |

- After adoption, fix commits per commit fell more in adopting repos than in control repos. The commit count doubled after adoption, so this ratio is partly a denominator effect.
- Teams that adopted AI kept CFBs flat, while all CFBs rose 24%. There is no workload denominator, so confidence is Low.

**Dose-response: not possible.** The share-of-AI-lines labels are 100% on 253 of 255 tickets, so there is no variation to test.

## 2. Mechanisms (quarterly, AI vs non-AI PRs)

| Measure | 2026-Q2 AI / non-AI | 2026-Q3 AI / non-AI |
|---|---|---|
| Median changed lines | 233 / 57 | 227 / 62 |
| Touch tests | 62% / 35% | 63% / 40% |
| Review threads per 100 lines | 0.23 / 0.02 | 0.13 / 0.15 |
| Median hours to merge | 25 / 14 | 33 / 21 |
| Reverted | 3.9% / 1.5% | 1.2% / 0.3% |
| Touch top-10 hotspot dirs | 15% / 30% | 23% / 32% |
| Author not a code owner (hotspot PRs) | 57% / 81% | 86% / 81% |

- AI share of PRs into the top-10 hotspot dirs: 5% (2025-Q4), 7%, 26%, 38%, 47% (2026-Q4, partial).
- Tests touched: matched RR 1.28 (1.16-1.41) within repo; 1.08 (0.94-1.23) within author. So part of the "AI adds tests" effect is author habit.

## 3. Practices and controls found (Confluence)

| Control | Page | Status |
|---|---|---|
| AI-metrics GitHub Action: label + share of AI lines on the Jira ticket | 3915612323, 4116217881, 4228842028 | Measurement only |
| PgM monthly "AI usage" audit sets "Implemented by AI Agent" | 4011230379 | Measurement only |
| Claude Code hooks run the SonarQube quality gate | 4259546714 (2026-10-17) | Opt-in |
| Pandorian AI code review against engineering guidelines, rollout plan | 4099179080 | Rollout; enforcement timeline |
| CSA PR Reviewer (AI PR review agent) | 4250174279 (live 2026-10-18) | One team |
| Engineering Quality Standard: test levels + AI-assisted test creation | 4008870336 | Standard, one space |
| AI Tool Adoption Tracker; AI Native SDLC Adoption | 4189357554, 4112155050 | Adoption tracking |

No page found that sets review depth or size rules **specific to AI-written code**.

## 4. Claim classification

| # | Claim | Class | Evidence | Confidence | Falsified by |
|---|---|---|---|---|---|
| A1 | AI PRs grew from 0-5% (2025) to 46-60% (2026-Q3/Q4) of pilot PRs | FACT | PR markers | High | Marker misdetection audit |
| A2 | AI share rose in the same months as CFBs | CORRELATION | Timing | High (timing) | - |
| A3 | AI PRs are 3.7x larger and touch tests more | FACT | PR data | High | - |
| A4 | Review per line does not grow with AI PR size | FACT | Threads per 100 lines | Medium | Review bots counted as reviews |
| A5 | AI PRs cause more customer bugs per change | CAUSAL HYPOTHESIS - **not supported** | RR 0.78-0.84 within repo/team; R8 1.03 | Low-Medium | Within-author RR > 1 with CI above 1 in the 2027-Q1 re-test |
| A6 | Authors who use AI have more follow-up fixes on their own AI PRs than on their non-AI PRs | CORRELATION (weak) | Within-author RR 1.45 (0.98-2.14) | Low | Re-test with more exposure |
| A7 | AI adoption reduced defects | CAUSAL HYPOTHESIS - not supported | Ratio 0.75 confounded by commit volume | Low | Normalized team workload data |
| A8 | AI increases change volume, and volume (not per-change risk) drives the rise | CAUSAL HYPOTHESIS | Commits doubled after adoption; per-change ratios ~1 | Low-Medium | Rise persists when normalized per change |

## Limits

- Pilot repos only (13). PRs without an AI marker count as non-AI.
- Follow-up fixes are found through Jira keys in commit messages (EM repos: 6-17% key rate).
- The monolith has no PR history before the TFS migration.
- The window is short: only 2026-Q2 has 90-day exposure.
