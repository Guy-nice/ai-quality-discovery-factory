# Problem Statement v4

**Version:** v4 | **Date:** 2026-10-22 | **Supersedes:** [v3](problem-statement-v3.md) | **Gate 2:** PASSED (interim) | **Gate 4:** NOT PASSED
**Evidence:** Findings rounds [1](../02-research/findings-round-1.md), [2](../02-research/findings-round-2.md), [3](../02-research/findings-round-3.md), [4](../02-research/findings-round-4.md)

## 1. Statement

In 2026, customers find more, and more severe, defects than in any year since at least 2021: CFB +51%, P1/P2 +72% (H1 YoY). The organization delivers much more change, and its validation and release controls did not scale with it. AI-assisted changes are not riskier per change (RR about 1.0).

In the pilot (Orchestration Core, contact routing and lifecycle):
- **Growth:** valid CFBs rose 34% (6.7 -> 8.9 per month), with a step to about 17 per month from 2026-04. Valid P1/P2 share is 82%.
- **Duplicates:** the invalid share rose from 35% to 51%, mostly duplicates of the same incidents.
- **Main root cause (PH-1):** distributed state races in the VC-to-VC sync layer and on the monolith-to-services event path, with almost no concurrency or ordering tests (4 of 1,349 test files).
- **Knowledge concentration:** the most defect-dense code depends on 1-2 people.

## 2. Changes vs v3

| Item | v3 | v4 |
|---|---|---|
| Pilot growth | +77% (all CFBs) | **+34% valid**; invalid share 35% -> 51% (F13) |
| PH-1 | Medium-High, broad | Medium-High, **narrowed** to InterVCCommWrapper + ACDProvider / AgentHelper (F14) |
| PH-2 | Medium | **Low-Medium**: timing match, about 4% direct cause (F16) |
| P-05 | Not tested | **Supported**: bus factor 1-2 on the densest code (F15) |

## 3. Next

Gate 4 needs SME validation, production migration dates and sponsor approval of the success criteria. See [Gate 4 readiness v0](../03-decisions/gate-4-readiness-v0.md).
