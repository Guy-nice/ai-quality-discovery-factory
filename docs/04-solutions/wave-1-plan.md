> **Status 2026-10-25: PROVISIONAL HYPOTHESIS (D-030).** Not a recommendation until mission v2 evidence gaps are closed. See [reassessment](../06-reassessment/mission-v2-reassessment.md).

# Wave 1 Plan - Chosen from Data

**Date:** 2026-10-22 | **Pilot:** Orchestration Core, contact routing and lifecycle | **Decision:** D-027 | **Status:** specs ready; applying them in company repos and Jira needs approval (D-028)

All 6 options stay in scope, because each maps to a confirmed cause. The order comes from data: first the broken signals and the cheapest strong controls, then the design change.

| Step | Option | Why first (data) | Spec | Owner (from data) | Measure |
|---|---|---|---|---|---|
| 1 | **SO-3A E2E trust** | The routing E2E pipeline passed 1.2% of runs and fails the same 13 out-of-order / retry scenarios. The PH-1 signal exists but is ignored. Other suites: 69-79%, mostly environment and fixture failures. | [so3a-e2e-trust](so3a-e2e-trust.md) | Routing E2E owners (see spec) | Pass >= 95% over 14 days; flaky <= 2% |
| 2 | **SO-5 Hotspot PR rules** | In hotspot code, the follow-up CFB-fix rate rises with PR size: 21% (0-50 lines) to 54% (> 1000). Outside hotspots it is flat (3-6%). Large non-AI PRs are riskier than large AI PRs. | [so4-so5](so4-so5-owners-pr-rules.md), [rules H1-H7](drafts/hotspot-pr-rules.md) | Code owners per hotspot | S6, follow-up fix rate |
| 3 | **SO-4 Owned hotspots** | The monolith has no CODEOWNERS. InterVCCommWrapper has 1 qualified committer; AgentHelper/MCH has 0. Minimum bus factor on top-10 hotspots = 1. | [CODEOWNERS drafts](drafts/) | Owners named in drafts | S5 >= 3 |
| 4 | **SO-1C Stuck / divergence monitor** | 4 state modes = 21% of valid in-flow CFBs, with 92 incidents. 8 of 13 stuck MIs have no RCA. 5 invariants cover about 30-36% of valid CFBs. | [so1-state-races](so1-state-races.md) | Orchestration Core SRE + EM | S3, S4; PH-5 data |
| 5 | **SO-2 Escape-to-test** | 38% of pilot RCAs add a test today; 30% of fixed CFBs link a test. | [so2-escape-to-test](so2-escape-to-test.md) | Team code owners | >= 90% compliance; S1, S2 |
| 6 | **SO-1A/B Order-tolerant state + tests** | The VC-to-VC proto has 80 RPCs and no per-contact version or sequence. 2 hand-written out-of-order fixes caused new defects. | [so1-state-races](so1-state-races.md) | InterVCComm + EM owners | S1, S2 |
| 7 | **SO-3B Fault / load stage** | No perf or chaos workflow; AFM chaos plan "not started". | after step 1 | Routing QA | S1, S3 |
| - | **SO-6 Real controls** | Steps 1-6 become blocking checks; unused Jira fields are retired. | in each spec | QA Architect | S6, S7 |

## How progress is measured

Monthly S1-S7 from `scripts/db/metrics.py` (table `metrics_monthly`); see [measurement plan](measurement-plan.md). Review after 2 quarters (2027-04). Extend to Analytics and Data and WFM only if S1 and S2 improve.

## Needs approval before apply

1. CI changes in pilot repos (pre-test checks, blocking rules) - step 1.
2. GitHub rulesets / CODEOWNERS PRs in `inContact/inContact` and service repos - steps 2-3.
3. Jira workflow validator + field - step 5.
4. Monitor in production observability - step 4.
