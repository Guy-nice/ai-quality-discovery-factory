# Problem Statement v3

**Version:** v3 | **Date:** 2026-10-22 | **Supersedes:** [v2](problem-statement-v2.md) | **Gate 2:** PASSED (interim)
**Evidence:** [Round 1](../02-research/findings-round-1.md), [Round 2](../02-research/findings-round-2.md), [Round 3](../02-research/findings-round-3.md)

## 1. Statement

In 2026, customers find more, and more severe, defects than in any year since at least 2021: CFB +51%, P1/P2 +72% (H1 YoY). The organization delivers much more change. Its validation, review and release controls did not scale with it:
- most quality fields are not filled;
- there is no Story-level RIA;
- there is no blocking automated gate;
- tests do not cover real scenarios, concurrency or production scale.

**AI-assisted development is not shown to be the cause.** AI changes escape at about the same rate per change as non-AI changes (RR about 1.0, Low-Medium confidence). AI does increase the volume of change.

Risk is concentrated in Orchestration Core, in the contact routing and lifecycle flow (+77%; 7.1 incidents per routing CFB). There the main escape class is **distributed state and concurrency races** between the legacy monolith and new services, during several parallel migrations.

## 2. Claim status

| Hypothesis | Status | Confidence | Evidence |
|---|---|---|---|
| P-01 Quality declined | Supported (customer impact, severity) | Medium-High | F1, F6 |
| P-02 Change rate exceeds validation capacity | **Supported** | Medium | F6, F8, F10 |
| P-03 Legacy concentrates risk | Weak overall (4%); **stronger in pilot** (legacy named in 20%; boundary races) | Low-Medium | F3, F11 |
| P-04 AI contributes per change | **Not supported**; small effect not excluded | Low-Medium | F10 |
| P-05 Knowledge concentrated | Not tested | - | - |
| P-06 Controls on paper only | Supported | High | F8 |
| PH-1 to PH-5 (pilot) | See F11 | Medium | F11 |

## 3. Gate 2 status

PASSED (interim): the problem is described with evidence. Open, but not blocking G2: U-14 (exclude invalid CFBs after triage), a human second rater, U-15 (usage normalization).
