# R15 - AI adoption by team vs customer-found bugs (2025 vs 2026)

**Date:** 2026-10-22 | **Data:** DB `team_r15`, `team_quarter`, [r15-ai-teams.csv](../../data/aggregates/r15-ai-teams.csv) | **Script:** `scripts/db/r15_ai_teams.py`

**Question:** Do teams that use more AI in 2026 get more valid CFBs than in 2025?

**Answer:** Not shown. The direction is positive, but every confidence interval includes "no effect". The data has strong confounders. Confidence: **Low**.

## Method

- Teams: top 40 by CFB volume (2025-01 to 2026-10). Analysis set: teams with 8 or more CFBs in 2026.
- **AI adoption proxy:** share of the team's 2026 CFBs with an AI indicator (cf_15229 = Yes or an AI label). This measures AI use in fix work, not in feature work.
- **Outcome:** valid CFBs, 2026-01-01..10-22 vs the same window in 2025. Invalid resolutions are excluded (D-020).
- **No workload denominator:** Jira story counts per team timed out on every call. So "CFB per 100 stories" was not possible, and the outcome is a count ratio.

## Result

| Test | Set | Result | 95% CI |
|---|---|---|---|
| Spearman, AI share vs log CFB ratio | 34 teams | rho 0.13 | - |
| High vs low tercile (median AI share 38% vs 0%) | 34 teams | CFB ratio 2.21 vs 0.77; DiD 2.86 | 0.90-7.55 |
| Stable teams only (>= 5 valid CFB each year), upper vs lower half | 21 teams | rho 0.37; DiD 1.59 | 0.65-3.46 |
| Valid P1/P2 share, 2025 -> 2026 | high / low | 34% -> 54% / 55% -> 63% | - |

## Why the confidence is Low

1. **Team re-homing:** Bolivia site closure and team splits (ACD Admin Bolivia -> Pune; Hornet -> Dragonfly / Agni / Titans; new teams Nexus, Orchestration II). The "low AI" group holds shrinking teams, and the "high AI" group holds teams that receive bugs.
2. **No workload control:** teams that ship more (and use AI more) get more CFBs at the same rate.
3. **Reverse direction possible:** teams with more CFBs fix more of them with AI, which raises their AI share.
4. **The proxy is fix work, not the causing change.** R8 measured the causing change and found RR about 1.0.

## Use

- The per-change result (R8: RR 1.03, CI 0.57-1.86) remains the best evidence.
- R15 does not contradict it, and it does not confirm a team-level AI effect.
- Re-run with per-team story counts when Atlassian responds (team x quarter Story total and cf_15229 = Yes, projects CGY and ENG excluded).
