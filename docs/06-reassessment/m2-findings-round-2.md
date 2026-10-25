# Mission v2 - Findings Round 2 (E7, E8, E9, D7)

**Date:** 2026-10-25 | **Exclusion applied:** MI-investigation tickets (D-032) | **Detail:** [E7](m2-e7-delivery.md), [E8](m2-e8-requirements.md), [E9](m2-e9-ai.md), [D7](m2-d7-recurrence.md)

## Summary

| Area | Finding | Class | Confidence |
|---|---|---|---|
| E7 Delivery | Emergency changes x2.9 from 2026-06 (about 100 -> 270-380 per month). Normal-change failure flat to lower (3.9% -> 2.6%). | EVIDENCE | High |
| E7 Delivery | Emergency changes and valid CFBs move together month by month (Spearman 0.66; CFB -> next-month emergency 0.75). | CORRELATION | Medium |
| E7 Delivery | Among CFBs with a known cause, share introduced within 90 days: 28% -> 41%. | EVIDENCE (censoring inflates 2026) | Low-Medium |
| E7 Delivery | Median escape latency 100-200 days from causing change to customer report. | EVIDENCE | Medium |
| E8 Requirements | About 25% of customer bug reports close as works-as-designed / not a bug / limitation; 52% of those are P1/P2. | EVIDENCE | High |
| E8 Requirements | 42.5% of those closures (CI 28.5-57.8) are real requirement or documentation gaps: about 15% of all reports, outside the "valid CFB" count. | EVIDENCE (n=40, AI rater) | Medium |
| E8 Requirements | Causing stories link a spec less often than matched controls (6.8% vs 31.8%). | CORRELATION | Low-Medium |
| E9 AI | Matched follow-up fix rate AI vs non-AI: within repo RR 0.84 (0.64-1.11), within team 0.78 (0.55-1.10). | CORRELATION (no effect found) | Low-Medium |
| E9 AI | Within the same author: RR 1.45 (0.98-2.14). | CORRELATION (weak signal) | Low |
| E9 AI | AI PRs 3.7x larger; review per line does not grow; AI share into hotspots 5% -> 47%. | EVIDENCE | Medium-High |
| E9 AI | No company page sets review or size rules for AI-written code. | EVIDENCE | Medium |
| D7 Recurrence | Recurrence after a fix is low and flat (3.9% -> 1.2-1.6%); reopen flat (5.2% -> 5.6%). | EVIDENCE | Medium |
| D7 Recurrence | About 1 in 4 named causes is a bug fix; fixes of customer bugs as cause 4.6% -> 10.8%. | EVIDENCE | Low-Medium |

## AI: fact, correlation, causal hypothesis

| Claim | Class | Status |
|---|---|---|
| AI use grew from about 0% to 31-47% of work in 2026 | FACT | Confirmed |
| AI labels on bugs mark AI fixes, not AI causes | FACT | Confirmed |
| AI changes cause more customer bugs per change | CAUSAL HYPOTHESIS | **Not supported** (R8, R16, E9 within repo / team) |
| The same author's AI PRs need more follow-up fixes than the same author's non-AI PRs | CORRELATION | Weak signal (RR 1.45, CI touches 1); re-test 2027-Q1 |
| AI adds risk through **size into hotspot code with flat review depth** | CAUSAL HYPOTHESIS | Plausible mechanism; size-risk curve applies to all PRs (SO-5 data) |
| AI adoption caused the 2026 CFB rise | CAUSAL HYPOTHESIS | **Not supported:** adopting teams flat (83 -> 79) while all CFBs +24% (Low) |

## What changed in the picture

1. **Customer pain is larger than "valid CFBs".** Expectation and documentation gaps add about 15% of reports.
2. **Fixing creates risk.** Emergency changes tripled, and 1 in 4 named causes is a bug fix.
3. **Recurrence is not the problem.** Fixed defects rarely come back.
4. **AI is a volume and size factor, not a per-change risk factor** on current evidence.

## Gaps still open

- U-26: ServiceNow record-level read (impact, who affected, change -> incident links).
- Requirement churn (changelog too large for the current tool).
- Human validation (Q-D blocked).
