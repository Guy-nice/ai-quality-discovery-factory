# Current State: QA Agents and Quality Gates (2026-10-25)

**Method:** read-only check of Confluence and GitHub (pilot repos). No interviews. | **Pages:** agent catalog 3949003282, mutation hub 4201808311, rollout 4267148087, session log 4281532425, WIP DoD 4048715783, Go/No-Go master 4213801417, template 4213702945

## 1. Answer

Today **nothing in the agent set blocks a change**. Agents run locally, by choice. The only checks that block a merge are Aikido, PR / Jira-ID validation and, in one repo, the Sonar job. The 26.4 release Go/No-Go is still mostly "TBD". A blocking mutation gate (80% on changed code) is planned for 2026-12-15.

## 2. QA agents

| Agent | Status | Trigger | Blocks? |
|---|---|---|---|
| unified-mutation-testing | Rollout; pilot done (APQ go, WFM conditional, Recording pending) | Local CLI | No; gate planned 2026-12-15 |
| test-plan-generation | In use (Recording: "mandatory" by policy) | Local | No |
| playwright-script-generator | In use (Recording) | Local | No |
| exploratory-testing | In use (Recording) | Local | No |
| RIA (2 phases) | Phase 1 as docs; phase 2 not automated | Local | No |
| test-cases-optimizer, vnext-to-playwright-migrator, agent-observability-log | Listed; no adoption found | Local | No |

The catalog page has no status column; several owners are deactivated accounts.

## 3. What blocks today (pilot repos)

| Repo | Sonar runs in CI | Sonar is a required check | Other required checks |
|---|---|---|---|
| inContact (monolith) | Yes (ci_build / ci_test) | No | Validate PR, Validate Build, Aikido |
| routing-ng-contact-retry | Yes | **Yes** (`build-test-sonar`) | - |
| routing-ng-advanced-findmatch | Yes | Not visible | PR, Aikido |
| routing-ng-agent-capacity-service | Yes | Not visible | PR, Aikido |
| orch-entity-* (4 of 10 read) | Unknown (shared workflows) | No | PR, Aikido (+ Jenkins for timer) |

Unknown: Sonar quality-gate conditions and whether the quality gate (not just the analysis) fails the job.

## 4. Release Go/No-Go 26.4

- Master page: overall status **TBD**.
- Orchestration Core: **CONDITIONAL**. VMS/Recording: TBD with most criteria GO. APQ: all rows in progress. A&D, LiveVox & Digital, AHW, WFM, other domains: **TBD**.
- The decision is human sign-off on 9 exit criteria (toggles, regression, exploratory, perf, P1-P3 closed, synthetics, deploy/rollback, infra, high-risk).

## 5. Assessment: mutation score as a blocking Sonar gate (planned 2026-12-15)

| Question | Evidence | Implication |
|---|---|---|
| Which escapes does it address? | "Test existed but ineffective" = 3-3.3% of escapes. Untested scenarios 28-31%; races ~23% (pilot). | Mutation measures existing unit tests; it does not find missing scenarios or races. |
| Is the signal correct today? | 2 of 4 scored pilot runs FAIL only because timeouts / compile errors count as "not killed"; NOTHING_TO_MUTATE unhandled; passes on 2 mutants | A blocking gate would stop valid PRs. |
| Can it apply to all teams? | No tool for PHP, C, Lua; most sub-groups not started; Orchestration Core "none recorded" | An org-wide date conflicts with uneven readiness (teams differ strongly). |
| Side effect | The agent writes tests for surviving mutants | Risk of tests written to kill mutants, not to check behavior. |

**Recommendation (D-040):** on 2026-12-15, publish the mutation score in Sonar as **visible, non-blocking**, first for teams marked ready. Make it blocking for a scope only when 3 conditions hold:
1. The false-negative issues are fixed (timeout / compile-error handling, a minimum mutant count, NOTHING_TO_MUTATE).
2. Data shows that PRs below the threshold get more follow-up fixes than PRs above it. This can be measured from the PR data we already hold, as part of X3/X4.
3. The scope is risk-based (hotspot and correctness-critical code), not company-wide.

## 6. Not checked

Sonar gate conditions (sonar.nice.com not queried); composite CI actions; Jira tickets CXQA-925164 (Sonar integration), CXQA-925160; 26.3 Go/No-Go pages; Jira workflow validators; interviews.
