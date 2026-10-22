# Agent Reports - Round 6 (verbatim)

**Date:** 2026-10-22 | **Iteration:** 14 | Synthesis: [wave-1-plan](../../04-solutions/wave-1-plan.md).

## SO-1 - State races specs

SO-1 specs are done: the failure-mode catalog, the monitor, the state design and the tests. Nothing is committed.
- Catalog: 51 race, stuck and ACD-state CFBs (valid, in-flow, last 12 months). They split into M1 out-of-order or stale event (7), M2 concurrent in-memory update in VC (7), M3 lost event (6), M4 flag not cleared after reject (3), M5 capacity (6), M6 non-race bug (9) and M7 RCA not filled (13).
- State modes M1-M4: 23 of 107 valid in-flow CFBs (21%), with 92 incidents.
- Stuck MIs: 13 of 51 are MIs, and 8 of those 13 have no filled RCA.
- Fix-caused defects: two out-of-order fixes, hand-written per service, caused new defects (EM-146033 caused EM-148596; AOR-13256).
- Monitor (SO-1C): 5 invariants: stuck too long, VC vs EM divergence, delivery flag, event gap, saturation. Thresholds are proposals for 30 days of shadow mode. Coverage: about 30% of valid in-flow CFBs, or 36% with the saturation check. It also gives the detection data PH-5 needs.
- Design (SO-1B): the InterVCCommWrapper proto has 80 RPCs and no per-contact version or sequence field (only `createdAt` on 3 messages). The proposal is one shared library: per-contact version, idempotent apply, stale reject with a metric, outbox on the VC, and flags cleared on reject. Rollout: EM consumers first, then the VC behind a toggle.
- Tests (SO-1A): an M1-M4 ordering test matrix. EM state-manager and AFM have tests; none for OBMS, Contact Retry, EventPub, or the M4 reject path. The M1-M4 tests block merge on 5 hotspot paths.
- Not done: Confluence was not queried; the R9 component map was used instead.
Files: `docs/04-solutions/so1-state-races.md`, `data/aggregates/so1-failure-modes.csv` (`agg_so1_failure_modes`), `scripts/db/so1_modes.py`, DB table `failure_modes`.

## SO-4/5 - Owners and PR rules

Task: data-based CODEOWNERS drafts (SO-4) and hotspot PR rules (SO-5) for the 10 pilot hotspot directories. Drafts in the research repo only; nothing applied to company repos.
- Owners: 6 of the 10 directories have 3-4 owners who qualify on commits or reviews. Logins come from 203 GitHub commit lookups and 2,568 PR reviews.
- Owner gaps: AgentHelper/MCH has 0 qualified committers. InterVCCommWrapper has 1 (jmichaelcharles15); NiceLuc is added from reviews, and selvarajv3 is marked "to grow". agent-capacity client has 1 (ajbobo-nice), and its former main author has made no commits since 2026-04.
- Existing CODEOWNERS: the monolith has none. AFM uses `*` owners, 2 of 3 not active in the hotspot directory. Agent-capacity has a team-only rule. Branch protection not readable (404).
- Size risk: follow-up CFB-fix rate in hotspot PRs is 20.7% at 0-50 lines, 27% at 151-400, 33% at 401-1000 and 53.8% above 1000. Outside hotspots it stays flat at 3-6%.
- Review per line: in hotspots it drops from 3.26 to 0.03 review threads per 100 lines as PRs get bigger.
- AI vs non-AI: large non-AI PRs are riskier than large AI PRs (39% vs 11% above 1000 lines). So the rule should be path-based for all PRs, not AI-only.
- Limits chosen: a 400-line blocking limit in hotspot files, and a 1000-line hard stop with a mechanical-change exception that an owner approves. Every hotspot PR also needs 2 approvals including 1 code owner, a test change or a stated reason, and a Jira key. Full rules H1-H7 are in the spec.
- Data limits: the follow-up measure may favour bigger PRs (more files touched); the flat non-hotspot curve suggests this effect is small. Monolith PR history before the TFS migration is missing. One account shows as deactivated in Confluence but committed until 2026-10; left out, verify.
Files: `docs/04-solutions/so4-so5-owners-pr-rules.md`, `docs/04-solutions/drafts/` (3 CODEOWNERS drafts, `hotspot-pr-rules.md`), `scripts/db/so45_owners.py`, `data/aggregates/so45-owners.csv`, `so45-size-risk.csv`; DB `so45_owners`, `so45_size_risk`, `agg_*`; raw in `data/raw/so45/` (gitignored).

## SO-3A - E2E trust

Most E2E failures come from the test environment, not the product. The one suite that tests routing behavior has failed every scheduled run since 2026-05.
- Data: 2,837 runs from 13 workflows (2026-04-25 to 2026-10-22), 495 job results, and 1,544 failed-test rows from 135 failed-run logs. Test names only.

| Suite | Pass rate | Main failures |
|---|---|---|
| VFM-AFM routing pipeline | 1.2% | assertion 50%, waits for routing state 23% |
| BU Profiles integration | 31.5% (rising to 86% in October) | no logs for 25 of 30 failed runs |
| Run test suites (E2E) | 78.6% | environment, setup, fixtures, timeouts: 70% |
| E2E cluster run | 69% (rising to 92%) | credentials 39%, fixtures 28% |
| Service unit tests | 90-94% | - |

- Flaky: in Run test suites, 50 of 66 re-run commits both failed and passed.
- Quarantine does not help: 465 different tests fail across 29 runs, so muting the top 10 adds 0%.
- Hidden product signal: the VFM-AFM pipeline fails the same 13 routing scenarios (out-of-order, contact-retry, "match not published"). They match PH-1: triage, do not mute.
- Expected pass rate if environment, setup and fixture failures are fixed: Run test suites 89% (94% with timeouts fixed), E2E cluster run 90%, BU Profiles 93% (Low confidence).
- Plan: (1) triage the 13 VFM-AFM scenarios; (2) credential and fixture check before tests, own test data per run; (3) keep reports 90 days; (4) target >= 95% pass over 14 days, <= 2% same-commit flaky; (5) a suite blocks merges only while it meets target; under 80% for 2 weeks -> non-blocking + repair ticket.
Files: `docs/04-solutions/so3a-e2e-trust.md`, `data/aggregates/so3a-e2e.csv`, `scripts/db/so3a_ci.py`, `scripts/db/so3a_analysis.py`; DB `ci_runs`, `ci_jobs`, `test_failures`, `agg_so3a_e2e`.
