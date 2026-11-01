# 05 - Summary: Reports, Plans and Decks

**Updated:** 2026-11-01 | **Canonical numbers:** [management report](management-report.md) (headline window: D-035)

Start with the management report. Every other file supports it.

## Current

| File | What it is | For | Version, date |
|---|---|---|---|
| [Management report](management-report.md) | Findings, causes, proposal, outside evidence, 8 metrics, 5 decisions, plan, risks. Every claim linked to evidence. | Directors, VPs, architects | 2.0, 2026-11-01 |
| [Action plan v2](action-plan-v2.md) | Keep, change, stop, start (with gate IDs); gates and automation; quick wins; waves; success by April 2027 | Decision makers, QA&RM | 2.0, 2026-11-01 |
| [Offsite deck](offsite-deck.pptx) | 17 slides: findings, why gates fail, outside research, 3-layer model, pod roles, QA&RM role, SDLC gates, gate lifecycle, AI rule, pod types, metrics, timeline, 5 asks | Offsite kickoff (live talk) | 2026-11-01 |
| [DoD v2](dod-v2-evidence-based.md) | Each WIP DoD item (Confluence 4048715783) with a verdict by evidence | DoD page owners | 2026-10-25 (+ note 2026-11-01) |
| [DoD v2 deck](dod-v2-deck.pptx) / [pdf](dod-v2-deck.pdf) | 8 slides on DoD v2 | DoD review meeting | 2026-10-25 |
| [Management deck v3](management-deck-v3.pptx) / [pdf](management-deck-v3.pdf) | 15 slides: research result and 4 decisions | Management decision meeting | 2026-10-25 |

## Related (outside this folder)

| Need | File |
|---|---|
| How pods work with quality; policies; AI rules | [Pod quality playbook](../08-pod-quality/pod-quality-playbook.md) |
| Every gate with mode and evidence | [Gate catalog](../08-pod-quality/gate-catalog.md) |
| Pod quarterly check | [Self-assessment](../08-pod-quality/pod-self-assessment.md) |
| Industry evidence | [Outside research 2024-2026](../08-pod-quality/external-research-2024-2026.md), [Claude Code review model](../08-pod-quality/compare-claude-code-review.md) |
| Vendor talks | [Harness questions](../08-pod-quality/vendor-harness-questions.md) |
| 1-page answer | [Brief](../00-brief.md) |

## Archive (superseded, kept for history)

| File | Superseded by |
|---|---|
| [Action plan v1](archive/action-plan-v1.md) | Action plan v2 |
| [Summary and recommendations](archive/summary-and-recommendations.md) | Management report (numbers before D-032 / D-035) |
| [Management deck v2](archive/management-deck-v2.pptx) / [pdf](archive/management-deck-v2.pdf) | Management deck v3 |
| [Management deck v1](archive/management-deck-v1-superseded.pptx) / [pdf](archive/management-deck-v1-superseded.pdf) | Management deck v3 |

## Rules for this folder

- Numbers come from the management report. Update the report first, then decks and plans.
- A new version gets a new file. The old one moves to `archive/` with a "Superseded by" note.
- Decks are built by scripts in [scripts/deck](../../scripts/deck/README.md). Open each deck in PowerPoint after a build; there is no automatic visual check.
