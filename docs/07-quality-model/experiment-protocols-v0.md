# Experiment Protocols v0 (X1-X5)

**Date:** 2026-10-25 | **Data:** `agg_exp_readiness`, `exp_team_archetype` (`scripts/db/exp_readiness.py`) | **Status:** ready to start after management approval; research does not run changes in company systems (D-029)

## 1. Power check (why the first design changed)

One team per arm for one quarter cannot detect a 30% change for most experiments (alpha 0.05, power 0.8):

| Exp | Original design | Quarters needed for 30% | Verdict |
|---|---|---|---|
| X1 Intake fields | 3 teams vs 3 controls | 1-2 (effect 15% -> 80%) | **Viable** |
| X2 Detection | 1 team pre/post | about 33 | Not viable as a significance test |
| X3 Size-scaled review | 2 vs 2 teams | 4 | Viable only pooled or longer |
| X4 Fix-safety review | 2 vs 2 teams | > 12 | Not viable on CFB outcome |
| X5 Expectation gaps | 1 team pre/post | > 12 | Not viable on CFB outcome |

Cause: customer-found bugs are rare per team (C teams: 6-8 valid per month in total). **Rule adopted:** pool teams, and use the measure with the most events that still links to the outcome. Keep the CFB outcome as a slower confirming signal.

## 2. Protocols (revised)

| Exp | Hypothesis | Arms (from data) | Primary measure (high volume) | Confirming outcome (slow) | Duration | Success rule | Stop rule |
|---|---|---|---|---|---|---|---|
| **X1** Intake rule | Required fields make D1-D8 measurable | Dragonfly (A), Better Calls Devs (B), DX-Platform-Sandy (C) vs Orchestration, IN-Agent Copilot, Kepler | Share of new valid CFBs with causing key and detected-by (baseline causing key 15%) | - | 1 quarter | Treated share >= 80% and above control (two-proportion test) | 2 of 3 teams report the fields as a blocker at retro |
| **X2** Detection monitor | Monitoring finds correctness failures before customers | Advanced Omnichannel Routing (A), shadow mode | Monitor alerts that match a later customer case (precision, lead time) | Share of P1 detected by us (needs U-26) | 6 weeks shadow + 1 quarter | Alerts precede >= 1 matching customer case with acceptable false-alarm rate (set in shadow week 2 from observed noise) | No matching case after 6 weeks |
| **X3** Size-scaled review in hotspots | Review depth scaled to size lowers follow-up fixes | Pool all teams with >= 10 hotspot PRs per quarter; stepped start (half now, half next quarter) | 90-day follow-up fix rate per hotspot PR (baseline about 70%, file-overlap proxy) | Valid CFBs in hotspot dirs | 2 quarters (stepped) | Rate lower in treated periods vs not-yet-treated (CI excludes 0) | Merge time doubles with no rate change |
| **X4** Fix-safety review | Extra review for bug-fix PRs lowers fix-caused defects | Same pool as X3, bug-fix PRs only | Follow-up fix rate on **bug-fix PRs** (PR-level, many events) | Fix-caused share of new CFBs (> 12 quarters alone) | 2 quarters (stepped) | As X3, on bug-fix PRs | As X3 |
| **X5** Expectation-gap triage | Triage of "works as designed" closures reduces repeat reports | Pool all archetype-C teams (5) + VMS/QM and WFM (highest WAD rates) | Share of WAD / not-a-bug closures that get a doc or backlog action (process measure) | Repeat WAD reports per topic (slow) | 1 quarter | Action share >= agreed level, set with product owners at start | Product backlog cannot absorb |

## 3. Common protocol rules

- **Pre-register** each experiment in `docs/07-quality-model/` before start: hypothesis, arms, measure, success and stop rules. Changes after start are logged as deviations.
- **Measure** with the same scripts as the baseline (`scripts/db/metrics.py`, `exp_readiness.py`); gap-only data pulls (D-033).
- **Controls** are matched by archetype, volume and P1/P2 share. Check shared services between arms before start (not yet done).
- **Report** effect with confidence interval, not only pass/fail. A practice spreads only when it beats its control (decision rule R2).

## 4. Limits

- X1 "failure_type present" is our derived label (100% everywhere); only causing key carries information.
- X3/X4 follow-up rate is a file-overlap proxy; 510 of 1,663 PRs have no team mapping (U-27).
- X4 baseline rests on 94 bug-type causing links; team ranking is noisy.
- Archetypes and failure types are not human-validated.
