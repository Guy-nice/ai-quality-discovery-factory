# Source Review: "WIP Quality Definition of Done !To review!"

**Source:** [SRC-013] Confluence CX space, page 4048715783, author Guy Guterman, last modified 2026-08-23
**Reviewed:** 2026-10-22 | **Status of source:** WIP, not mandatory input (per author)

## 1. What the page says (summary)

| # | Content | Class |
|---|---|---|
| 1 | Two gate levels: Epic (before merge to main) and Release (before ship). All items mandatory; exceptions need Director + QA Lead approval. | Proposal |
| 2 | Key gap: no harness runs agents at SDLC events, reads output, and blocks on failure. "Nothing stops developers from making code." | HYPOTHESIS (stated as fact) |
| 3 | "An agent is not a gate." Distinguishes Suggested / Mandatory (policy) / Real control. | Useful framework |
| 4 | Tiering by risk: Tier 1 revenue-critical (CXone core, Enlighten) to Tier 3 internal. | Proposal |
| 5 | Flow: G1 Epic review -> RIA phase 1 -> test case agent -> Playwright generator -> AI implementation in TDD loop -> PR: RIA phase 2 + mutation (kill >= 80% changed files). | Solution design |
| 6 | Gate map: only Sonar, mutation, pipeline pass, perf, feature toggle registration marked as technically enforceable. | Inventory of controls (partial) |

## 2. What to keep

- **Policy vs control distinction.** Strong. Use it in the controls inventory: for each existing check, record Suggested / Mandatory-policy / Real control.
- **Tiering by risk.** Matches the research need to locate risk concentration. Tier assignment should come from CFB and incident data, not only from product names.
- **Cost principle (cheap gates left, human gates right).** Sound. Keep as a design constraint for later.

## 3. Challenges (evidence discipline)

| ID | Issue | Why it matters | Class |
|---|---|---|---|
| R-01 | The page starts from solutions (harness, RIA, mutation, Playwright, chaos). No data links customer-found bugs to the absence of these gates. | Risk of building controls that do not address the main escape causes. | CONTRADICTION with Core Principle |
| R-02 | Root cause assumed: "nothing enforces". Alternative causes not tested: requirement gaps, prod/test environment differences, legacy unknown behavior, third-party, scale/race conditions. | A harness cannot catch a defect class that no test or requirement describes. | HYPOTHESIS |
| R-03 | Jira already has quality fields on Bugs: Root Cause Analysis (with "How was it missed?"), Regression Impact Analysis, EOR: Broken?, EOR: Mitigation?, Number of Incidents, Impact Rank. The page does not reference them. | These are existing policy controls with history. They show if RIA is done and still misses. | EVIDENCE (Jira field metadata, DAT-48858) |
| R-04 | Jira EOR template says "Rollback (Not applicable for monolith)". The page requires "Deploy and rollback verified". | Rollback gate may be impossible for the monolith. Needs an alternative (toggle off). | CONTRADICTION |
| R-05 | "All items mandatory" while many rows are "Suggested" or "Can be gate". | Unclear what is required today. | CONTRADICTION (internal) |
| R-06 | Mutation kill >= 80% on changed files: threshold not justified; cost per language and for the monolith unknown; no evidence that escapes come from weak assertions. | High compute and friction for unproven benefit. | ASSUMPTION |
| R-07 | Flow uses an AI implementation agent. The initiative studies whether AI-assisted development degrades quality. | The design adds the variable under study before its effect is known. | Risk |
| R-08 | "Testing needs to be separate from the LLM that codes." | Plausible (independence of verification) but no evidence yet. | HYPOTHESIS |
| R-09 | "Reference framework" with 6 gates is not cited. | Traceability. | UNKNOWN |

## 4. How this source enters the research

- Treat the page as a **candidate solution set** for Phase P5 only.
- After escape-cause classification (R5 in research plan), map each proposed gate to the escape causes it can prevent. Keep only gates that cover a top cause.
- Use the Suggested / Policy / Real-control scheme for the controls inventory (research item R6).
