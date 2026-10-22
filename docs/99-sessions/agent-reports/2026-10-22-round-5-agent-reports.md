# Agent Reports - Round 5 (verbatim)

**Date:** 2026-10-22 | **Iteration:** 12

## R15 - AI dose-response by team

R15 found no clear link between team AI use and more valid CFBs. The direction is positive, but every confidence interval includes "no effect". Confidence: Low.
- No workload denominator: every Atlassian call timed out (team story counts, 3 tries). So I ran it from the DB only. Team AI adoption = share of each team's 2026 CFB fixes that are AI-made. Outcome = valid CFBs, Jan 1 to Oct 22 of 2026 vs the same window in 2025.
- All 34 teams: Spearman rho 0.13. High-AI teams (median 38%) vs low-AI teams (median 0%): DiD ratio 2.86, 95% CI 0.90-7.55.
- 21 stable teams only: rho 0.37, DiD ratio 1.59, 95% CI 0.65-3.46.
- Severity: valid P1/P2 share, high-AI teams 34% to 54%, low-AI teams 55% to 63%.
- Confounders: team re-homing (Bolivia site closure, team splits, new teams), no workload control, and a possible reverse direction (more CFBs, so more fixes made with AI). The proxy measures fix work, not the change that caused the bug.
- Net: R8 (RR 1.03 per causing change) stays the best evidence. R15 neither contradicts it nor confirms a team-level effect. Re-run when per-team story counts are available.
Files: `scripts/db/r15_ai_teams.py`, `data/aggregates/r15-ai-teams.csv`, `docs/02-research/r15-ai-dose-response.md`. DB tables: `team_quarter` (story columns empty), `team_r15`, `agg_r15_ai_teams`, plus one `jql_counts` row that logs the failed query.

## R16 - AI PRs vs non-AI PRs

R16 is done: AI-authored PRs are not riskier, but per line they get less review.
- AI PR share: 0-5% in 2025-Q1..Q3, then 25% (2026-Q1), 41% (Q2), 46% (Q3), 60% (Q4, partial). In the top-10 hotspot dirs it went from 0% before 2026-Q2 to 20%, 34%, then 51%.
- Data: 6,125 pilot commits mapped to 1,663 merged PRs (590 AI). 1,920 commits have no PR, mostly monolith history before the TFS migration, so 2025 is mostly service PRs.
- Size and review (2026-Q3): AI PRs are about 3.7x larger (median 227 vs 62 lines) and get more reviews (6.7 vs 4.7 per PR). Review threads per 100 lines are not higher (0.13 vs 0.15), so review effort did not scale with size. Median time to merge is 33h vs 21h.
- Tests: AI PRs touch tests more often: 63% vs 40%, RR 1.25 (1.14-1.36) after adjusting for size and hotspot.
- Follow-up CFB fix within 30 days (2026, adjusted for size and hotspot): RR 0.67 (0.47-0.95). AI PRs have fewer follow-up fixes. This agrees with R8 (RR 1.03).
- Named causing change: RR 0.35 (0.13-0.91), but only 5 vs 20 events and AI PRs had less time for CFBs to surface. Not reliable.
- Bias: AI work without a marker counts as non-AI, which pulls results toward "no difference". Reviewer logins are not stored, so AI review bots may inflate the review counts.
- Verdict: no evidence that AI PRs cause more defects. The open risk is larger AI changes going into hotspot code without matching review depth. Confidence: Low-Medium. Next check: a 90-day follow-up window in about 2027-Q1.
Files: `scripts/db/r16_prs.py`, `scripts/db/r16_analysis.py`, `data/aggregates/r16-ai-prs.csv` (`agg_r16_ai_prs`), DB tables `prs` and `pr_commits` (no PR bodies stored), `docs/02-research/r16-ai-prs.md`, stripped cache in `data/raw/r16/` (gitignored).

## R17 - Data-based refutation

- PH-1 survives, narrowed (Medium). 22 of 28 "race" RCAs show race/ordering, 6 are load only, so in-flow ordering is about 23%, still about 2x other VPs. Content search finds concurrency tests (EM state-manager: 4 "out of order" + 15 "concurrent" files; AFM: 4 "concurrent"), so the name-based count was too low.
- PH-2 weakened (Low). No production dates: Atlassian timed out and 0 Epics match "AFM rollout". The direct cause stays at about 4%. Needs a human.
- PH-3 survives as a minor cause (Low-Medium). 4 of the 20 blind RCAs are .NET/JSON/MessagePack swaps.
- PH-4 survives (Medium). The pilot repos have no perf or chaos workflow. Ephemeral E2E passed 7 of its last 30 runs. Integration tests passed 22 of 30.
- PH-5 cannot be tested from data. The RCA template text gives false matches. Needs incident and alert data.
- P-05 survives (Medium). The InterVCComm owners are active but bus factor is 2. The agent-capacity owner left after 2026-03-23.
- Blind second rater: 17/20 escape cause (85%) and 17/20 regression. Stored as `rca_class` round R17 (20 rows).
- Limits: GitHub search rate limit (contact-retry and agent-capacity not searched); Atlassian timeouts.
Files: `docs/02-research/r17-refutation.md`, `data/aggregates/r17-refutation.csv` (`agg_r17_refutation`), DB `rca_class` round R17.
