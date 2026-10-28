# Brief - Product Quality (1 page)

**As of:** 2026-10-25 | **Window:** Jan-Sep 2025 vs Jan-Sep 2026, MI investigations removed (D-032) | **Model:** [quality model v0](07-quality-model/quality-model-v0.md) | **Deck:** [v3](05-summary/management-deck-v3.pptx) | **Report:** [management report](05-summary/management-report.md) | **Pod guide:** [playbook](08-pod-quality/pod-quality-playbook.md)

## Answer

1. **Bugs got more severe; volume rose a little.** P1/P2 customer-found bugs +49%, all customer-found bugs +13%. Q3 2026 volume (346) was below Q3 2025 (383), but P1/P2 was higher (258 vs 167).
2. **Customers find our problems first.** 96% of P1 incidents enter through customer cases.
3. **Almost half of valid bugs are business-correctness failures:** report data, routing, contact lifecycle, recording/QM, agent state. Their P1/P2 share rose from 52% to 70%.
4. **AI is not riskier per change** (matched ratio 0.78-0.84). AI adds volume and larger changes in hotspot code.
5. **Teams differ strongly** (incidents per bug 1.1-10.4), mostly inside the same VP. One workflow does not fit all.

## Proposal

Quality model v0: 8 outcome dimensions; a common baseline (intake rule, required bug fields, RCA, team map); a risk-based layer (correctness types, hotspot code, bug fixes, emergency changes); team adaptation by archetype; 5 experiments with control teams before any rollout.

## Action plan ([detail](05-summary/action-plan-v1.md))

| | What |
|---|---|
| Keep | RCA for P1/P2; feature toggles; AI under common rules; Xray |
| Change | Bug intake; data-based Go/No-Go; trusted E2E; review by size in hotspot code; QSU per team |
| Stop | Raw bug count as quality number; one gate set for all teams; unused Jira fields |
| Start | Quality model; team map; detection monitors; expectation-gap triage; owner backups; X1-X5 |

**When:** Now (decisions, X1, X2) -> Q1 2027 (X3-X5, team reviews) -> April 2027 (results, model v1) -> H2 2027 (spread). Gates and automation are means: few blocking checks where risk is proven now; the rest after evidence.

## Open

ServiceNow record-level read (U-26); human validation; fall in ServiceNow P1 incidents (C-08); team-to-service map (U-27).
