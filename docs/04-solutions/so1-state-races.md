# SO-1 State Races - Specs v0 (monitor, design, tests)

**Date:** 2026-10-22 | **Scope:** pilot in-flow valid CFBs created 2025-10-22..2026-10-22 (n=107) | **Data:** DB `failure_modes` (51 rows), [so1-failure-modes.csv](../../data/aggregates/so1-failure-modes.csv), script `scripts/db/so1_modes.py`
**Method:** 51 CFBs selected (race class in R9/R17, or sub-flow stuck / ACD state). The mode was set by reading the summary and the RCA "How did it happen" text. Single rater. Only labels are stored.

## 1. Failure-mode catalog

| Mode | What fails | CFBs | Incidents | Main components |
|---|---|---|---|---|
| M1 | Out-of-order or stale event overwrites newer state | 7 | 40 | Contact Retry (2 VCs send routable on/off), State Streams DFO, AFM skill subsequence, OBMS SkillRoutable, VC ContactStateChange vs gRPC reply |
| M2 | Concurrent update of VC in-memory state (double delivery, stale object, unlocked shared dictionary) | 7 | 28 | VC queue cache + FindMatch, agent session delivery flag, MasterVariables, PrepareForInbound |
| M3 | Event lost, not published, or consumer stopped | 6 | 16 | VC -> Kinesis drop, ContactRoutable not sent, State Streams Kinesis / KDA, retry cluster list |
| M4 | Match / delivery state not cleared after reject or timeout | 3 | 8 | VC wakeup queue (Sleeping), lastMatched flag, agent script |
| M5 | Capacity saturation (threads, rate limit, blocking call in stream) | 6 | 99 | VC thread limits, Resolver Kinesis read limit, Agent Capacity REST call |
| M6 | Non-race logic / data bug (out of SO-1 scope) | 9 | 11 | ACD admin APIs, sync jobs, build dependency |
| M7 | Unknown: RCA not filled | 13 | 45 | 9 are stuck-contact MIs |

- **EVIDENCE (Medium):** State modes M1-M4 = 23 of 107 valid in-flow CFBs (21%), 92 incidents. M1 + M2 alone = 14.
- **EVIDENCE (Medium):** 13 of 51 are major incidents; 38 were customer cases. 8 of the 13 MIs have no filled RCA. So the stuck-contact MIs teach nothing today.
- **EVIDENCE (Medium):** Two M1 fixes made new defects: the out-of-order check in State Streams DFO (EM-146033 -> regression EM-148596) and the AFM subsequence check (AOR-13256). Hand-written ordering logic per service is itself a risk.

## 2. SO-1C - Runtime monitor (first, weeks)

| # | Invariant | Mode | Signal source | Threshold (proposal) | Action |
|---|---|---|---|---|---|
| I1 | A contact in a non-terminal state with no state change for > T | M1-M4, M7 stuck | EM entity state + VC contact list | Voice > 4 h, digital > 24 h, queued > 2x skill SLA | Alert team; safe reconcile = re-publish state from VC (source of truth), not delete |
| I2 | VC state and EM / State Streams state differ for one contact | M1, M3 | VC vs EM entity state, sampled | > 5 min divergence | Alert; re-sync from VC |
| I3 | An agent has > max contacts in delivery, or "in delivery" > 60 s | M2, M4 | VC agent session | Any breach | Alert; clear delivery flag after match reject |
| I4 | Event gap: producer count vs consumer count per stream | M3 | VC publish counters, Kinesis / KDA consumer lag | Gap > 1% for 5 min, or consumer lag > 2 min | Page on-call |
| I5 | Saturation: VC blocking / execution threads, stream read limit | M5 | VC perf counters, Kinesis throttling | > 80% of limit for 5 min | Alert capacity owner |

- **Coverage (proposal):** I1-I4 cover M1-M4 + M7 stuck = 32 of 107 valid in-flow CFBs (30%). With I5: 38 (36%).
- **Shadow mode first:** run 30 days without paging; tune T to < 1 false alert per day per cluster. The thresholds above are starting points, not derived limits.
- **Side effect:** I1-I4 give the missing detection data for PH-5 (U-25). Cleanup jobs that delete stuck contacts stay only as a reconcile step, with a count.

## 3. SO-1B - Order-tolerant state design (quarter)

**Current guarantees (from code structure):**

| Path | Ordering / idempotency today |
|---|---|
| VC-to-VC sync (InterVCCommWrapper): 80 gRPC methods, 40 contact-control messages | No per-contact version or sequence field in messages. `createdAt` on 3 messages only. A separate CTI event sequence call exists. Idempotency: UNKNOWN. |
| VC -> EM / State Streams (EventPublisher, ProviderEntityStateManagement, Kinesis / Kafka) | Per-service checks (timestamp, subsequence) added after CFBs; not shared. Stream order per shard only. Exactly-once: UNKNOWN. |

**Proposed pattern (one shared library, not per service):**
1. A **per-contact state version** (monotonic counter owned by the VC that owns the contact), on every contact-state message and event.
2. **Idempotent apply:** consumers apply an event only if `version > stored_version`; duplicates are no-ops.
3. **Stale reject with a metric:** an older version is rejected and counted (it feeds I2). Do not compare wall-clock timestamps across nodes.
4. **Outbox on the VC:** a state change and its event are written together, so a crash cannot lose the event (M3).
5. **Clear-on-reject:** match / delivery flags reset in the same step that rejects (M4).

**Risks:** legacy VC core changes (few owners, SO-4 first); 80 RPCs (start with the contact-state subset); a mixed-version rollout (consumers must accept events with no version during migration).
**Steps:** (1) the shared version library + tests; (2) EM / State Streams consumers first (lowest risk, they have tests); (3) VC publishes versions behind a feature toggle; (4) InterVCCommWrapper contact-state messages; (5) remove the per-service timestamp checks.

## 4. SO-1A - Ordering test matrix

| Mode | Test (simulated transport: permute, delay, duplicate, drop) | Lives in | Exists today |
|---|---|---|---|
| M1 | Same contact: end-before-requeue, off-before-on, assign-before-status; result = newest version wins | Shared version library; EM state-manager; AFM; OBMS | EM state-manager: 4 out-of-order + 15 concurrent test files; AFM: 4 concurrent. None for OBMS, Contact Retry |
| M2 | Parallel FindMatch + refuse; 2 deliveries to 1 agent; NCache callbacks on many threads | VCSvc Providers tests (ACD, Agent), InterVCCommWrapper.Tests (26 files) | Not found by name or content (UNKNOWN: needs code read) |
| M3 | Drop 1 event in a sequence; consumer restart; outbox replay | EventPub tests, State Streams | Not found |
| M4 | Match rejected -> requeue -> new match is accepted | VCSvc ACD provider tests | Not found |

**Gate:** for changes to InterVCCommWrapper, EventPublisher, ProviderEntityStateManagement, ACDProvider and AgentHelper, the M1-M4 tests run in CI and block the merge (SO-6).

## What could invalidate this

- A second rater moves race cases into other modes (single rater, n=51).
- The M7 stuck MIs (13, no RCA) have a different cause. Fill those RCAs first; I1 will show their mode.
- The VC already has idempotent handlers that the code structure did not show. A code review of the contact-state subset checks this.
