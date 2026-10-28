> **Superseded** by [action plan v1](../05-summary/action-plan-v1.md) and [gate catalog](../08-pod-quality/gate-catalog.md).

> **Status 2026-10-25: PROVISIONAL HYPOTHESIS (D-030).** Not a recommendation until mission v2 evidence gaps are closed. See [reassessment](../06-reassessment/mission-v2-reassessment.md).

# Solution Options v0 (P5)

**Date:** 2026-10-22 | **Gate:** G4 passed (interim, data-based) | **Scope:** pilot = Orchestration Core, contact routing and lifecycle
**Rule:** each option maps to a confirmed cause and a success criterion (S1-S7, [Gate 4 package](../03-decisions/gate-4-readiness-v0.md)). The options are ranked on quality, robustness and maintainability, not on build cost.

## Summary

Fix the design first, then prove it with tests, then make the checks real (blocking). AI is not the target. Large changes into hotspot code are, whoever writes them.

| # | Cause (evidence) | Recommended option | Measure |
|---|---|---|---|
| SO-1 | State races in VC-to-VC sync and event path: ordering escapes ~23% in-flow vs ~11% elsewhere; InterVCCommWrapper 43-55% defect density (PH-1) | **Order-tolerant state design + ordering tests + stuck-contact monitor** | S1, S2, S3 |
| SO-2 | Real scenarios not tested: 28-31% of escapes | **Escape-to-test rule + event contract tests** | S1, S2 |
| SO-3 | Production conditions not reproduced: no perf/chaos workflow; E2E passed 7 of 30 runs (PH-4) | **Make E2E trustworthy first, then a fault/load stage for routing** | S1, S3 |
| SO-4 | Knowledge concentration: bus factor 2 on densest code; owner left agent-capacity (P-05) | **Owned hotspots: CODEOWNERS >= 3, required review, design notes** | S5 |
| SO-5 | Large AI PRs into hotspots, review per line not higher (R16) | **Path-based hotspot rules for all PRs: size limit, 2 human reviewers, tests required** | S2, S6 |
| SO-6 | Controls on paper: 9 of ~15 quality fields < 2% filled; no blocking gate (F8) | **Few real gates for the causes above; retire unused fields** | S6, S7 |

## Options per cause

### SO-1 State races (rank 1: largest severe share)

| Option | What | For | Against |
|---|---|---|---|
| A | Ordering / duplication / drop tests for InterVCCommWrapper and event publishers, with a simulated transport (permute, delay, duplicate messages) | Proves behavior; blocks regressions | Tests alone do not remove the race |
| B | Design: versioned, idempotent state updates (sequence or version per contact, dedupe key, reject stale) on VC-to-VC sync and monolith -> EM path | Removes the class of defect | Touches legacy core code; needs owners (SO-4) |
| C | Runtime invariant monitor: contact stuck > N min, VC vs EM state divergence; alert + safe reconcile | Detects what slips; replaces cleanup jobs used as fixes | Detects, does not prevent |

**Recommend B + A, with C as the safety net.** Design for order tolerance, prove it with A, catch residue with C. C also gives the PH-5 detection data that is missing (U-25).

### SO-2 Untested real scenarios

| Option | What | For | Against |
|---|---|---|---|
| A | **Escape-to-test rule:** a valid pilot CFB closes only with a linked automated test (Xray) or a stated reason "not testable" | Turns each escape into permanent coverage; uses existing RCA + Xray | Needs Jira workflow change |
| B | Contract tests on the monolith <-> services event boundary (schema + ordering semantics) | Hits the boundary where races sit | Needs shared event definitions |

**Recommend A + B.** Today 39% of RCAs add a test; the rule makes it 100% by design.

### SO-3 Production conditions

| Option | What | For | Against |
|---|---|---|---|
| A | E2E trust: quarantine flaky tests, named owner, pass-rate SLO >= 95%, failures block merge | A 7-of-30 suite gives no signal now | Short-term work, no new coverage |
| B | Fault and load stage for routing: latency / fault injection (AFM chaos plan exists, "not started"), anonymized production event replay at scale | Covers scale / race / env escapes (~35% in pilot) | Needs a production-like environment |

**Recommend A, then B.** A broken signal makes every other test investment weaker.

### SO-4 Ownership

**Recommend:** CODEOWNERS for the top-10 hotspot directories with >= 3 owners each; required owner review; short design notes for InterVCCommWrapper and ACDProvider; pairing to spread knowledge. Alternative (rotation only) is weaker: no enforcement.

### SO-5 AI and large changes into hotspots

| Option | What | For | Against |
|---|---|---|---|
| A | AI-only rules (extra reviewer for AI PRs) | Simple | Data shows AI is not riskier per change; targets the wrong variable |
| B | **Path-based hotspot rules for every PR:** auto-label PRs that touch hotspot paths; size limit (split above ~400 changed lines); 2 human reviewers incl. 1 owner; tests required | Targets size x hotspot, the real risk; fair to AI and human work | Slower merges in hotspots |

**Recommend B.** Keep the AI label for measurement (D-025 re-test 2027-Q1).

### SO-6 Real controls, not paper

- Convert into **blocking** checks only what serves SO-1 to SO-5: hotspot PR rules, escape-to-test link, E2E pass-rate, contract tests.
- Retire Jira quality fields with < 2% use, or make them mandatory where they serve a check. Unused fields add noise.
- **WIP Quality DoD page (D-008) mapped to evidence:**

| DoD proposal | Verdict now | Why |
|---|---|---|
| Harness that runs checks and blocks | **Yes**, as the vehicle for SO-5 / SO-6 checks | No blocking gate exists today |
| RIA phase 1 / 2 agents | Later | RIA miss is 7% of pilot escapes; half of misses had RIA done |
| Mutation testing >= 80% | Not now | "Test existed but ineffective" is 3% of escapes |
| Playwright generator | Supports SO-2 A | Only after SO-3 A fixes E2E trust |
| Chaos runner | **Yes**, in SO-3 B | Matches PH-4 |
| Feature toggle rules | Keep | Rollback not possible on the monolith (C-03) |

## Rollout and proof

1. Pilot first (Orchestration Core). Order: SO-3 A and SO-4 (weeks), SO-1 C and SO-5 B (weeks), SO-2 A, then SO-1 B / A and SO-3 B (quarter).
2. Measure S1-S7 monthly from the same DB queries as the baseline. Review after 2 quarters.
3. Extend to Analytics and Data and WFM only if S1 and S2 improve in the pilot.

## What could invalidate these options

- SME or incident data shows PH-5 (late detection) or PH-2 (migrations) dominates. Then raise SO-1 C and add migration controls.
- The order-tolerant design (SO-1 B) is not possible in the legacy VC core. Then weight A + C higher.
- Escape-to-test produces low-value tests. Then audit a sample each quarter.
