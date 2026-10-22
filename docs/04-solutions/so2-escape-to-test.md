# SO-2 Escape-to-Test Rule - Spec v0

**Date:** 2026-10-22 | **Cause:** real scenarios not tested (28-31% of escapes) | **Measures:** S1, S2 | **Status:** spec only; Jira workflow change needs approval

## Rule

A **valid** pilot CFB (Orchestration Core; resolution Fixed or Fixed - Config) can move to Done only when one of these is true:

| Option | Evidence required |
|---|---|
| A. Test added | Jira link "is tested by" to an Xray Test, and the Test is automated (Automated = Yes) |
| B. Not testable | Field "Not testable reason" set (enum below) and approved by the team code owner |

Enum "Not testable reason": `config/data only` · `third-party defect` · `infrastructure` · `duplicate of tested defect` · `other (explain)`.

## Why this rule (data)

| Fact | Value | Source |
|---|---|---|
| Pilot RCAs that add a test today | 41 of 108 (38%) | `rca_class` R9 |
| Fixed CFBs with an Xray Test link | 30% (sample) | R6 |
| Escapes from untested scenarios | 28-31% | R5, R9 |
| Commits that already touch tests in hotspots | 49-77% | R3 |

Tests are already being written, but they are not tied to the escape. The rule closes that gap, and it makes the coverage traceable.

## Implementation steps (after approval)

1. Jira: add the "Not testable reason" field and a workflow validator on the Bug Done transition, for pilot projects first (ORC, AOR, AAD, ACD-related projects; list from `issues` where `rnd_vp` = Orchestration Core).
2. Xray: a Test template "Escape regression" that links to the CFB key.
3. Report: monthly share of valid pilot CFBs closed with option A or B (target >= 90% by the end of quarter 1).
4. Audit: each quarter, review 10 random escape tests for value. A test is valuable if it fails on the pre-fix code.

## Risks

- Low-value tests made to pass the rule. The quarterly audit limits this.
- The validator blocks urgent closures. The code owner approves option B.
