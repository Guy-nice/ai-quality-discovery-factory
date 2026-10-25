# Brief - Product Quality (1 page)

**As of:** 2026-10-25 | **Window:** Jan-Sep 2025 vs Jan-Sep 2026, MI investigations removed (D-032) | **Model:** [quality model v0](07-quality-model/quality-model-v0.md) | **Deck:** [v2](05-summary/management-deck-v2.pptx)

## Answer

1. **Bugs got more severe; volume rose a little.** P1/P2 customer-found bugs +49%, all customer-found bugs +13%. Q3 2026 volume (346) was below Q3 2025 (383), but P1/P2 was higher (258 vs 167).
2. **Customers find our problems first.** 96% of P1 incidents enter through customer cases.
3. **Almost half of valid bugs are business-correctness failures:** report data, routing, contact lifecycle, recording/QM, agent state. Their P1/P2 share rose from 52% to 70%.
4. **AI is not riskier per change** (matched ratio 0.78-0.84). AI adds volume and larger changes in hotspot code.
5. **Teams differ strongly** (incidents per bug 1.1-10.4), mostly inside the same VP. One workflow does not fit all.

## Proposal

Quality model v0: 8 outcome dimensions; a common baseline (intake rule, required bug fields, RCA, team map); a risk-based layer (correctness types, hotspot code, bug fixes, emergency changes); team adaptation by archetype; 5 experiments with control teams before any rollout.

## Open

ServiceNow record-level read (U-26); human validation; fall in ServiceNow P1 incidents (C-08); team-to-service map (U-27).
