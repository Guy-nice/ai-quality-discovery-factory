# R16 - AI-authored PRs vs other PRs (pilot code)

**Date:** 2026-10-22 | **Window:** merged 2025-01-01..2026-10-22 | **Data:** DB `prs`, `pr_commits`, `agg_r16_ai_prs`; [r16-ai-prs.csv](../../data/aggregates/r16-ai-prs.csv) | **Scripts:** `scripts/db/r16_prs.py`, `r16_analysis.py`

**Answer:** AI-authored PRs are bigger, get more reviews and touch tests more often. They do **not** lead to more follow-up CFB fixes. Confidence: Low-Medium.

## Method

- Pilot commits (13 repos, monolith pilot paths) were mapped to their merged PR through GitHub GraphQL. Result: 6,125 commits -> 1,663 PRs. 1,920 commits have no PR: direct pushes, or monolith history from before the TFS migration.
- **AI flag** (590 PRs): Claude / Copilot / Cursor co-author or "Generated with Claude Code" text in the PR or its commits, `claude/` branch, bot author, or AI label. Unmarked AI work counts as non-AI, which pulls the results toward "no difference".
- **Follow-up fix:** another commit that fixes a CFB changes a file of the PR within 30 days. Only PRs merged at least 30 days before 2026-10-22 count.
- **Rate ratio:** Mantel-Haenszel across size bucket (lines) x hotspot (touches a top-20 R3 directory). Greenland-Robins 95% CI.

## Results

| Quarter | AI share of PRs | AI share in top-10 hotspot PRs |
|---|---|---|
| 2025-Q1..Q3 | 0-5% | 0% |
| 2025-Q4 | 13% | 0% |
| 2026-Q1 | 25% | 0% |
| 2026-Q2 | 41% | 20% |
| 2026-Q3 | 46% | 34% |
| 2026-Q4 (partial) | 60% | 51% |

| 2026-Q3 | AI | Non-AI |
|---|---|---|
| Median lines changed | 227 | 62 |
| Reviews per PR | 6.7 | 4.7 |
| Review threads per 100 lines | 0.13 | 0.15 |
| Median hours to merge | 33 | 21 |
| Touches tests | 63% | 40% |
| Touches a hotspot dir | 39% | 56% |
| Follow-up CFB fix within 30 days | 12.2% | 14.6% |

| Outcome (2026, adjusted for size x hotspot) | AI events / PRs | Non-AI events / PRs | RR (95% CI) |
|---|---|---|---|
| Follow-up CFB fix within 30 days | 31 / 429 | 104 / 670 | **0.67 (0.47-0.95)** |
| PR is a named causing change (RCA) | 5 / 571 | 20 / 767 | 0.35 (0.13-0.91) |
| PR touches tests | 357 / 571 | 314 / 767 | 1.25 (1.14-1.36) |

## Findings

- **EVIDENCE (High):** AI PRs went from 0% to 46-60% of pilot PRs within 2026. Since 2026-Q2 they reach the hotspot code (34-51%).
- **EVIDENCE (Medium):** AI PRs are about 3.7x larger. Review depth per line is the same or lower (0.13 vs 0.15 threads per 100 lines), so review effort did not scale with size.
- **EVIDENCE (Low-Medium):** After the size x hotspot adjustment, AI PRs have fewer follow-up CFB fixes (RR 0.67). This agrees with R8 (RR 1.03), so there is no sign that AI changes are riskier.
- **Bias:** AI PRs are newer. CFBs surface over months and RCAs name few causing changes, so the "causing" RR is not reliable. Reviews per PR may include AI review bots (reviewer logins not stored).

**Could invalidate:** a longer follow-up window (90+ days) shows AI PRs catch up; or a human check finds that many "non-AI" PRs are unmarked AI work with more fixes.
