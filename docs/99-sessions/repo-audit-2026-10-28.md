# Repo audit 2026-10-28

Branch feat/pod-quality-sdlc-guide. Read-only audit. Scope: docs/**/*.md, README, AGENTS, CLAUDE.

## 1. Broken relative links
| File | Result | Fix |
|---|---|---|
| All docs md files, README, AGENTS, CLAUDE (script, python3 -I, code blocks skipped) | 0 broken links | None |

## 2. Inconsistent headline numbers (current-facing docs)
| File:line | Problem | Fix |
|---|---|---|
| docs/05-summary/summary-and-recommendations.md:15 | CFB +51%, P1/P2 +72% (H1, MI not removed). Banner (line 1) says +29% / +46%, not D-035 (+13% / +49%) | Add "Superseded by action-plan-v1 + D-035" banner; keep table as history |
| docs/05-summary/summary-and-recommendations.md:13-14,20,29 | 1,428 CFB 2026, CFB per story +38%, pilot +34% (pre-D-032/D-035 basis) | Same banner, or restate on D-035 basis |
| docs/00-charter/problem-statement-v4.md:11 | +51% / +72% in body; banner has +29% / +46% | Fix banner to D-035 values and add "numbers superseded by D-035" |
| README.md, 00-brief, action-plan-v1, dod-v2, management-report, quality-model-v0, HANDOFF | Match D-035 | None |
| docs/05-summary/*.pptx/pdf (decks v2, v3, offsite, dod-v2-deck) | Not text-checked (binary) | Grep slide text against D-035 in next pass |

## 3. Stale status: no "Superseded by" note
| File | Fix |
|---|---|
| docs/00-charter/problem-statement-v0.md (has "Status: perception only", no pointer) | Add "Superseded by v4" line |
| docs/00-charter/problem-statement-v1.md, v2.md, v3.md | Add "Superseded by v4" (v4 already says Supersedes v3) |
| docs/05-summary/management-deck-v1-superseded.pptx / .pdf (name only) | Add note in README or deck-index: superseded by v3 |
| docs/05-summary/management-deck-v2.pptx / .pdf | Mark "Superseded by v3" in README/HANDOFF index |
| docs/05-summary/summary-and-recommendations.md | Mark superseded by action-plan-v1 |
| docs/03-decisions/gate-4-readiness-v0.md | Add "Superseded by current-gates-2026-10-25.md" |
| docs/02-research/research-plan-v0.md | Add "Superseded by v2 reassessment plan" or status line |
| docs/04-solutions/solution-options-v0.md | OK: has PROVISIONAL HYPOTHESIS banner (D-030). Add pointer to action-plan-v1 |

## 4. Style violations (current-facing docs)
| Check | Result | Fix |
|---|---|---|
| Em dash | 0 in README, AGENTS, CLAUDE, 00-brief, 05-summary, 07, HANDOFF | None |
| Sentences > 25 words (prose only, tables skipped) | 3: action-plan-v1.md:8 (36 words); summary-and-recommendations.md:77 (28); 00-brief.md:3 (26) | Split each sentence in two |
| Table cells | Not measured | Optional |

## 5. Gaps
| Item | Finding | Fix |
|---|---|---|
| docs/99-sessions/full-history.md | Last entry is Iteration 40. Iterations 41-45 MISSING (iteration-log has them) | Append 5 entries (offsite deck, slide 10 metrics, table slides, review, management report) |
| docs/99-sessions/HANDOFF.md "State (2026-10-25)" | Date stale (last iteration 2026-10-28). No mention of offsite deck or management-report.md (0 hits) | Update State/Next steps to 2026-10-28; add offsite-deck.pptx and management-report.md |
| Read-first list in HANDOFF.md | Lacks management-report | Add after brief |

## 6. Duplicated content (consolidate)
| Files | Fix |
|---|---|
| Headline numbers repeated in README, 00-brief, action-plan-v1, dod-v2, management-report, quality-model | One canonical numbers table (e.g. docs/00-brief.md); others link to it |
| docs/05-summary/summary-and-recommendations.md vs action-plan-v1.md + dod-v2 (same recommendations, older numbers) | Reduce summary to a stub with link, keep as history |
| docs/05-summary/management-report.md vs 00-brief.md (same claims) | Keep report as the evidence-linked one; brief links to it |
| Decks v1/v2/v3 + dod-v2-deck + offsite-deck (5 pptx + 4 pdf) | Move superseded v1/v2 to docs/05-summary/archive/ |
| docs/99-sessions/agent-reports/* vs session-NN.md vs full-history.md | Keep full-history only as index; link to the raw reports |

## 7. Tracked junk
| File | Fix |
|---|---|
| docs/05-summary/~$offsite-deck.pptx (Office lock file, tracked) | git rm; add `~$*` and `.DS_Store` to .gitignore |
| data/archive/raw-git-2026-10-25.tar.gz (37 MB) | Move to Git LFS or release asset; keep checksum in repo |
| data/db/quality.sqlite (8 MB), data/db/git_history.sqlite.gz (6 MB) | Allowed by AGENTS (restore.sh); consider LFS |
| .DS_Store, tmp files | None found |
