# R17 - Adversarial Check of Pilot Hypotheses (data only)

**Date:** 2026-10-22 | **Why:** no SME answers yet; the lead asks to decide from data. | **Data:** `agg_r17_refutation`, `rca_class` round R17

Method: try to disprove each hypothesis using the RCA text, GitHub code search (test files), workflow runs, Git ownership and Jira/Confluence (Atlassian timed out). Blind second rating of the 20 questionnaire RCAs.

| ID | Strongest counter-evidence found | Verdict | Confidence | Human still required? |
|---|---|---|---|---|
| PH-1 State races | The "race" class mixes load cases: 6 of 28 are load-only, and 22 of 28 have a race or ordering signal. Concurrency tests exist by content: EM state-manager has 4 "out of order" and 15 "concurrent" test files, AFM has 4 "concurrent" test files. So the earlier count (by file name only) understated tests. | **Survives, narrowed** (ordering share about 23% in-flow, still about 2x other VPs) | Medium | No (an SME helps to size the test gap) |
| PH-2 Parallel migrations | No production rollout dates found (Atlassian timeouts; 0 Epics "AFM rollout"). Direct cause about 4%. | **Weakened** | Low | **Yes**: only people know the production dates |
| PH-3 Library / runtime swaps | Effect mixed after commit-size control. 4 of the 20 blind RCAs are .NET / JSON / MessagePack swaps. | **Survives (minor cause)** | Low-Medium | No |
| PH-4 Production not reproducible | No perf or chaos workflow in the pilot repos. Ephemeral-cluster E2E: 7 of the last 30 runs passed (12 failed, 11 cancelled). Routing integration tests: 22 of 30 passed (3,380 runs). | **Survives** | Medium | No |
| PH-5 Customers detect first | Not testable from RCA text: the template prompt text matches. A CFB is a customer case by definition. | **Not testable** | Low | **Yes**: needs incident and alert data |
| P-05 Knowledge concentration | InterVCComm owners are active (last commit 2026-10), but bus factor is 2. The agent-capacity owner left (38-50% of commits, last 2026-03-23). | **Survives** | Medium | No |
| R5b Classification | Blind second rater: escape cause 17/20 (85%), regression 17/20. Same model family. | **Acceptable** | Medium | Yes, for a truly independent rater |

**Result:** PH-1, PH-4 and P-05 survive the adversarial check, so solution design can use them. PH-2 and PH-5 cannot be decided from data. They need production dates and alert data from people.

**Limits:** GitHub code search hit its rate limit, so contact-retry and agent-capacity were not searched. Code search shows at most 100 hits per query.
