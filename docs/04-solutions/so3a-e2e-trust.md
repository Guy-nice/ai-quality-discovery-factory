# SO-3A - Make the pilot E2E signal trustworthy

**Date:** 2026-10-22 | **Data:** 2,837 GitHub Actions runs (2026-04-25..2026-10-22), 495 job results, 1,544 failed-test rows from 135 failed-run logs | DB `ci_runs`, `ci_jobs`, `test_failures`, `agg_so3a_e2e` | Scripts `scripts/db/so3a_ci.py`, `so3a_analysis.py`

## Finding

Most pilot E2E failures come from the test environment, not from the product. The one suite that tests routing behavior has failed every scheduled run for 6 months.

| Workflow (repo) | Runs | Pass % | Trend | Main failure classes |
|---|---|---|---|---|
| VFM-AFM Automated Test Pipeline (integration-tests) | 85 | **1.2** | 0% on schedule since 2026-05 | assertion 50%, async state wait 23% |
| Integration Tests with BU Profiles (integration-tests) | 1,000 | 31.5 | 26% (Jul) -> 86% (Oct) | logs not available for 25 of 30 failed runs |
| Run test suites (playwright-e2e) | 733 | 78.6 | 99% (Sep) -> 72% (Oct) | env/infra, fixture, setup, timeout = 70% |
| E2E cluster run (playwright-e2e) | 59 | 69.0 | 41% (Aug) -> 92% (Oct) | credentials 39%, fixture 28% |
| Service `test` (AFM / contact-retry / agent-capacity) | 856 | 90-94 | stable | - |

- **Flaky:** the same commit both failed and passed in 50 of 66 retried commits (Run test suites), 16 of 29 (BU Profiles) and 10 of 13 (E2E cluster).
- **Diffuse failures:** Run test suites had 465 different failed tests in 29 failed runs, and no test failed more than 4 times. So quarantine does not help: top-10 quarantine adds 0%.
- **Real signal hidden:** the VFM-AFM suite fails the same routing scenarios every run, e.g. "Match not published within 30s", "Remove and update multiple skills sent out of order", contact-retry. These match PH-1 (ordering and state races). Top-10 quarantine only lifts it to 18%, so these failures are product signal and must be triaged, not muted.

## Expected pass rate if environment failures are removed

| Workflow | Now | Fix env / setup / fixture | + fix timeouts |
|---|---|---|---|
| Run test suites | 78.6% | 88.6% | 93.6% |
| E2E cluster run | 69.0% | 89.7% | 89.7% |
| BU Profiles | 31.5% | 93.1% (low confidence: missing logs) | 95.4% |
| VFM-AFM pipeline | 1.2% | 11.1% | 14.4% (needs product triage) |

## Plan

| # | Action | Owner (active authors, 6 months) | Target |
|---|---|---|---|
| 1 | Triage the 13 VFM-AFM scenarios that fail in >= 7 of 26 runs: product bug (file it) or test defect (fix it). No muting. | integration-tests: jatin-patil-incontact, Nichole Proestakis | Pipeline >= 80% in 4 weeks |
| 2 | Credential and fixture preflight: fail fast and label the run "infra", not "test failed"; isolated test data per run (BU, skills, POCs) | playwright-e2e suite owners | Env-class failures < 5% of runs |
| 3 | Keep JUnit / Playwright JSON reports as artifacts for 90 days | Both repos | 100% of failed runs have test-level data |
| 4 | **SLO:** blocking suites >= 95% pass (rolling 14 days, main / develop only, infra failures tracked separately); same-commit flaky rate <= 2% | Suite owners + QA lead | Review weekly |
| 5 | **Blocking rule:** a suite blocks merge only while it meets the SLO. Below 80% for 2 weeks -> non-blocking + owner repair ticket. Service `test` workflows block now. | QA lead | - |
| 6 | Development-branch dispatch runs (e.g. `pipeline-growth`) are excluded from the KPI | - | - |

**Limits:** failure classes come from log patterns (no human check). BU Profiles has no logs for most failures. The 1,000-run cap cuts BU Profiles before 2026-07.
