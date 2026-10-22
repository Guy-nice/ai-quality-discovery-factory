# Decision Log

Dated, append-only. Do not edit past entries. To change a decision, add a new entry that supersedes it.

| ID | Date | Decision | Rationale | Decided by | Supersedes | Status |
|---|---|---|---|---|---|---|
| D-001 | 2026-10-22 | Phase 1 is discovery only. No solution design before Gate 4. | Initiative brief; avoid solution-first bias. | Guy Guterman | - | Active |
| D-002 | 2026-10-22 | Use repository structure `docs/00-charter` to `docs/03-decisions`, plus `docs/99-sessions` for per-session logs. | Brief structure; session logs added for traceability of each iteration. | Guy Guterman | - | Active |
| D-003 | 2026-10-22 | Each working session ends with a session log, one commit, and a push. | Keep history of each iteration. | Guy Guterman | - | Active |
| D-004 | 2026-10-22 | Until U-04 is answered, store only aggregates and IDs; no customer data, PII, or proprietary code. | Unknown data handling policy. | Guy Guterman (interim) | - | Interim |
| D-005 | 2026-10-22 | Lead delegates Round 1 scope questions (Q1-Q5) to the research. Research sets scope from data and records each choice here. Lead can override any entry. | Lead instruction: "do the best solution ... with best and high metrics". | Guy Guterman | - | Active |
| D-006 | 2026-10-22 | Interim scope = all CXone R&D projects with CFBs. Interim quality definition = CFB (`issuetype = Bug and salesforceAssociatedTypes is not EMPTY`) per quarter, total and P1/P2, plus CFB per 100 resolved stories. | Only customer-impact signal with 9 years of history; JQL given by lead. | Research (per D-005) | - | Interim |
| D-007 | 2026-10-22 | Domain analysis uses R&D VP and Team Name, not Project or Component. | Component 88% empty; projects re-homed (C-02). | Research (per D-005) | - | Active |
| D-008 | 2026-10-22 | The WIP Quality DoD page (SRC-013) is a candidate solution set for P5 only. It is not a research input on causes. | Core Principle: no solution before Gate 4. | Research (per D-005) | - | Active |
| D-009 | 2026-10-22 | Recommended pilot candidates for Gate 3: (1) Orchestration Core, (2) Analytics and Data, with the cross-domain "stuck / lost contacts" flow as the bounded business flow. Final pick after R2b. | Highest growth and share; scale/race and third-party escape profiles; boundary theme H-13. | Research (per D-005) | - | Proposed |
