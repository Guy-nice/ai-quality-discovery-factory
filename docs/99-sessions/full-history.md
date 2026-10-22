# Full History

Each iteration: full prompt (verbatim) + full result summary + files + commit. Append only. ASD-STE100.
Short version: [iteration-log.md](iteration-log.md).

---

## Iteration 1 - 2026-10-22

**Prompt:** Initiative brief. Verbatim: [initiative-brief-original.md](../00-charter/initiative-brief-original.md).

**Result:**
- Repo `Guy-nice/ai-quality-discovery-factory` was empty (private, no commits). No docs to read.
- Context read: QA Architect role notes (personal vault, from Confluence role page).
- Reply in 8 sections: mission (10 bullets), risks (10), inspect list (10 sources), Q1-Q9 (Q1-Q5 blocking), deliverables, gates G0-G4, first action, approval request.
- Main challenges raised: product scope undefined; "quality" undefined; AI attribution hard; data sensitivity; solution bias from repo name and existing tools.

**Files:** none. **Commit:** none.

---

## Iteration 2 - 2026-10-22

**Prompt (verbatim):**
> Start and upload it to Git that we will have each iteraction data and commit

**Result:**
- Repo cloned to `~/ai-quality-discovery-factory`.
- 12 docs v0 made per brief structure + `docs/99-sessions/` (D-002).
- Rule set: each session ends with session log, commit, push (D-003).
- Interim data rule: aggregates and IDs only (D-004).

**Files:** README, charter, problem-statement-v0, glossary, questionnaire, discovery-map, evidence-access-inventory, unknowns register, research-plan-v0, source-analysis-plan, decision-log, research-gates, session-01. **Commit:** a4d52dc.

---

## Iteration 3 - 2026-10-22

**Prompt (verbatim):**
> I do not answer 1 -5 because I want you to do the best solution to the prpblem with best and high metrix and all needed. This is a Jira JQL for getting all the bug: issuetype = Bug  and salesforceAssociatedTypes is not EMPTY ORDER BY created ASC this is the conluance that I started (review it and this is not you guid or mandatory!) https://nice-ce-cxone-prod.atlassian.net/wiki/spaces/CX/pages/4048715783/WIP+Quality+Definition+of+Done+To+review

**Result:**
- Jira + Confluence read access confirmed. CFB population = 11,662 (2017-05 to 2026-10).
- Useful Jira fields found: R&D VP, Team Name, Root Cause Analysis, Regression Impact Analysis, Number of Incidents, Impact Rank, EOR fields.
- 3 parallel analyses (forks):
  - R1 trend: CFB flat 2021-2025 (~1.3k/yr). H1 2026 vs H1 2025: CFB +51%, P1/P2 +72%. P1/P2 share 50% -> 68%. Stories resolved ×2.4, so CFB per story -33% (C-01).
  - R2 concentration: 1,318 -> 1,760 CFB (+34%) last 12 mo. Top 3 VPs (A&D, Orchestration Core, WFM) = 60%. Component 88% empty. AI labels 1 -> 159 (9%).
  - R5 RCA classification (n=213): test gap 31%, RIA miss 15%, scale/race/env ~20%, legacy 4%, monitoring actions 2%. 0 RCAs name AI as cause (template has no AI question).
- WIP DoD page reviewed: keep agent-vs-gate, policy-vs-control, tiering. Challenge: solution-first; top escape causes not covered; rollback contradiction with Jira template (C-03).
- Decisions D-005 (scope delegated to research) to D-009 (pilot candidates).
- Gates: G0 PASSED (interim), G1 PARTIAL, G2 PARTIAL.
- Question to lead: meaning of AI labels.

**Files:** problem-statement-v1, findings-round-1, source-review-quality-dod-wip, data/aggregates/* (7 files), session-02; updates to register, inventory, plan, gates, decisions, README. **Commit:** 9eecaf1.

---

## Iteration 4 - 2026-10-22

**Prompt (verbatim):**
> I want to add a log/tracing/data of our work from each prompt and resoults. each etiration  reporting it information to new line, be extremely concise and sacrifice grammar for concision and use ASD-STE100 (Simplified Technical English). IN general and always be use ASD-STE100 (Simplified Technical English).

**Result:**
- `iteration-log.md` made: one line per iteration. Iterations 1-4 added.
- README rule: one log line + commit + push per iteration; all text in ASD-STE100.
- Memory updated (iteration log rule, STE always on).

**Files:** iteration-log.md, README. **Commit:** 7801c07.

---

## Iteration 5 - 2026-10-22

**Prompt (verbatim):**
> I cannot answer to your qeatuion because I do not know. Update a full history so and continue with next steps

**Result:**
- Full history made (this file). Original brief stored verbatim.
- Lead does not know AI label meaning -> research finds it from data (R7).
- 4 parallel analyses started: R1b throughput jumps, R2b pilot short-list, R7 AI label meaning, R6 controls inventory.
- R1b: volume jumps = data imports (ENG 2024-01, CGY 2026-Q3). Adjusted CFB per 100 stories: Q2 1.22 -> 1.68 (+38%), Q3 1.62 -> 1.38 (-15%). C-01 weaker.
- R7: AI label on bug = AI-made fix (GitHub Action on Claude Code PR), not cause. Field "Implemented by AI Agent" (cf_15229) set by PgM KPI audit. AI stories 0.4% (2025-Q3) -> 31% (2026-Q2).
- R6: 9 of ~15 Jira quality fields under 2% filled. RIA: Epic 58%, Story 0%. Regressions: RIA missed 7, not done 7. Xray heavy (1.15M executions 2026), links weak (18-25%). No blocking automated gate. Go/No-Go human, pages "TBD".
- R2b: pilot = Orchestration Core, contact routing and lifecycle flow (score 37/50; 70% P1/P2; 3.8 incidents/CFB).
- Problem statement v2, findings round 2, D-010..D-013. G3 PASSED (interim).
- Security: plain-text credentials in one Jira issue, reported to lead, not stored in repo.

**Files:** full-history.md, initiative-brief-original.md, problem-statement-v2.md, findings-round-2.md, session-03, data/aggregates r1b/r2b/r6/r7; updates to register, plan, gates, decisions, README. **Commit:** see iteration-log row 5.

---

## Iteration 6 - 2026-10-22

**Prompt (verbatim):**
> All data, analysis, conclustions that you collect, create and made - have you uploaded to the repository as well?

**Result:**
- Audit of repo vs work done. Gaps found: agent reports not verbatim; analysis scripts in /tmp only; iteration-1 reply only summarized.
- Fixed: `docs/99-sessions/agent-reports/` (round 1: R1, R2, R5; round 2: R1b, R2b, R6, R7, verbatim, 1 secret redacted). `docs/99-sessions/replies/iteration-01-reply.md` (verbatim). `scripts/analysis/` (r1b, r5-rca, r6, r7 + README).
- Not in repo by design: raw Jira JSON dumps (may hold customer text, D-004); secret details (D-013); personal memory files (outside project). Lost: R2b tally scripts (deleted by fork); R1/R2 used JQL counts only (JQL in data READMEs).
- Raw /tmp scratch data deleted.

**Files:** agent-reports/*, replies/iteration-01-reply.md, scripts/analysis/*, iteration-log, full-history, README. **Commit:** see iteration-log row 6.

---

## Iteration 7 - 2026-10-22

**Prompt (verbatim):**
> continue with next steps R8 and R9 all need documented and all data that pull saved as DB

**Result:**
- Conflict noted: raw text holds customer data. Solution (D-014): `quality.sqlite` structured, committed; `raw_local.sqlite` + `data/raw/` text, gitignored.
- DB: schema + loader (`scripts/db/`). Tables: issues 3,292+, issue_links 3,229, causal_links 475, rca_class 321, flow_tags 466, jql_counts 50, query_log 52, confluence_pages 30, git_repos 13, agg_* 15.
- R8: causing key from RCA text (26% of fixed CFBs, precision 95%). AI vs non-AI RR: crude 1.39 (0.75-2.59); reviewed-only 1.03 (0.57-1.86). P-04 not supported per change (Low-Medium). AI = volume driver (D-015).
- R9: pilot 466 CFBs. Flow 123 -> 218 (+77%). Routing 7.1 incidents per CFB. Stuck/lost +375%. Race escapes 26% (pilot) vs 11%. Legacy named 20%. Hypotheses PH-1..PH-5. Findmatch gap analysis: no concurrency / real-Kafka tests. Git `inContact` read access; monolith in TFS.
- Partial R5b: Claude vs Claude agreement 79% (escape cause). Human rater needed.
- Problem statement v3; findings round 3; G2 PASSED (interim); D-014..D-016.

**Files:** scripts/db/*, data/db/*, data/aggregates/r8-*, r9-*, docs/02-research/r8-*, r9-*, findings-round-3, problem-statement-v3, session-04, agent-reports round 3; updates to register, inventory, plan, gates, decisions, README. **Commit:** see iteration-log row 7.

---

## Iteration 8 - 2026-10-22

**Prompt (verbatim):**
> For what you need this 1 and 2. what this help you to understand and do?

**Result:**
- TFS (U-21): monolith churn x CFB hotspots; test PH-3 (library swaps, parity tests); find PH-1 event boundary code; P-05 ownership. Without: P-03 stays Low, hotspot map half. Alternative: commit history export (paths, dates, authors) of routing/contact folders.
- SMEs (U-22): independent validation of PH-1..PH-5 (Gate 4 needs it); hidden context (other tests, migration dates); human rater on 20 RCAs = classification error rate. Without: risk of solution on wrong cause. Alternative: research finds names in Jira, lead approves; async questionnaire (10 Q + 20 RCAs, ~45 min).
- Neither blocks R3, R11, R14, R13 draft. Both block G4. SMEs more important.
- Question to lead: prepare SME list + questionnaire now?

**Files:** iteration-log, full-history. **Commit:** see iteration-log row 8.

---

## Iteration 9 - 2026-10-22

**Prompt (verbatim):**
> regarding the TFS guid me what do you need, link if you can? Not sure I know. Regarding teh 2-3 Orchestration Core architects or QA leads you can find this as well in confluance and jira signed leads and relevant pocal points too.

**Result:**
- TFS: Confluence search found the monolith was migrated to GitHub: `inContact/inContact` (DEVELOP), VCSvc at `Code/C#/Services/VCSvc`. Sources: Confluence 4231594095 (KT Session), VCSvc pages 3893887461 / 3894051323. Read access verified; VCSvc history from 2021-01. TFS not needed (D-017). R9 "not in GitHub" corrected. U-21 closed.
- SMEs (R12a fork): 16 candidates from Go/No-Go page, Confluence authorship, Git PR reviews and commits. Recommended: Kacie Mayberry (VC monolith), Karthick Chandrasekaran (routing services), Kevin Pyles (QA lead, named). Backups: Dez Grant, Puneet Kumar, Nichole Proestakis (D-018, proposed). Roles mostly guessed; Jira assignee data not pulled (timeouts).
- SME validation questionnaire v0: Part A 5 hypotheses + 5 questions; Part B 20 blind RCAs (stratified, seed 20261022).

**Files:** stakeholder-map.md, sme-validation-questionnaire.md, r12-stakeholders.csv, scripts/db/r12_stakeholders.py, DB (stakeholders, git_repos fix), corrections in findings-round-3 and r9 doc, register, inventory, gates, decisions, plan. **Commit:** see iteration-log row 9.

---

## Iteration 10 - 2026-10-22

**Prompt (verbatim):**
> I want to have a link such as claude.ai/rtifcat that can be shared with all comapny meembers and I need. can it be done? before conitnue next

**Result:**
- Claude Doc made: [AI Quality Discovery - Research Summary](https://claude.ai/artifact/QDD8cDsvj7t1NzPsZgdLdf).
- Sections: purpose and status (gates), problem statement v3, key findings (+ CFB quarterly chart 2021-Q1..2026-Q3), pilot + PH-1..PH-5, AI-assisted development (+ AI story share chart, rate ratios), controls, next steps / how to help, sources and method.
- Left out for company-wide audience: SME names, security finding, customer data. One comment in the doc asks lead: add SME names or not.
- Share: lead opens doc -> Share -> add people / organization. Doc is a snapshot; repo stays source of truth.

**Files:** README (link), iteration-log, full-history. **Commit:** see iteration-log row 10.

---

## Iteration 11 - 2026-10-22

**Prompt (verbatim):**
> yes cononite please

**Result:**
- R3 hotspots (fork): 7,866 commits, 184,464 file changes, 493 authors, 24 months. Jira-key link rate: monolith 76%, AFM 51%, EM 6-17%. Top: VCSvc/Providers/ACD, AgentHelper, AFM service, InterVCCommWrapper (43-55% of commits fix or cause CFB). Concurrency-named tests 4 of 1,349. AFM lost VFM out-of-order tests.
- R14 ownership: InterVCCommWrapper bus factor 1-2; agent-capacity owner gone since 2026-04-22; big providers too diffuse (bus factor 9-21). P-05 supported.
- R11 migrations (fork): Git code-start dates only (Atlassian timeouts). Pilot step 2026-04; event-study RR 1.9-3.0 vs control ~1.1, but events overlap. Direct migration cause ~11/296 (3.7%). PH-2 Low-Medium.
- Correction (own analysis): pilot in-flow valid CFB 80 -> 107 (+34%), invalid 35% -> 51%; valid P1/P2 82%. D-020: valid CFB = primary metric.
- R13 Gate 4 readiness v0: ranked root causes, frozen baselines, constraints, proposed success criteria S1-S7, checklist. Status NOT PASSED; blockers: SME validation, production rollout dates (U-23), sponsor approval.
- DB size: git_file_changes moved to git_history.sqlite(.gz) (D-019); quality.sqlite 4 MB.
- Questionnaire: Q3 production dates, new Q6 (2026-04 step), Q7 (InterVCCommWrapper risk).

**Files:** findings-round-4, problem-statement-v4, gate-4-readiness-v0, r3-r14 doc, r11 doc, data/aggregates r3/r11/r14, scripts/db r3/r11, git_history.sqlite.gz, session-06, agent-reports round 4; updates to register, plan, gates, decisions, questionnaire, READMEs. **Commit:** see iteration-log row 11.
- Shared Claude Doc updated (rev 17): pilot valid +34%, VC-to-VC sync hotspot, PH-1 narrowed, PH-2 weakened, G4 "Not passed" with blockers. A checklist item in the doc was changed by a reader (rev 12); left as is.

---

## Iteration 12 - 2026-10-22

**Prompt (verbatim):**
> Reagrding you question you approve to find the answer from data. I want us to coninue on with focues on the last year 2026 (or more and I want you as expert to choose) with adding AI more and more. and this is a lot of data to much.

**Result:**
- Choices: window 2025-01..2026-10 (D-021); validation from data, human only for PH-2 and PH-5 (D-022); success criteria adopted (D-023); 1-page brief as entry point (D-024).
- R15 (team AI share vs valid CFB): rho 0.13-0.37, DiD CIs include 1. No clear link. Low (no workload data; Atlassian timeouts).
- R16 (1,663 PRs, 590 AI): AI PR share 0-5% (2025) -> 25/41/46% (2026 Q1-Q3); in hotspots 0 -> 51%. AI PRs 3.7x larger, more reviews per PR, not more per line, test touch 63% vs 40%, follow-up CFB-fix RR 0.67 (0.47-0.95). Open risk: review depth vs size in hotspots (D-025).
- R17 (refutation): PH-1 survives (ordering ~23%); PH-4 survives (no perf/chaos workflow; E2E 7/30 pass); P-05 survives; PH-3 minor; PH-2 weak; PH-5 not testable. Blind rater 17/20 (85%).
- Correction: concurrency tests exist in EM (19 files) and AFM (4); name-based count withdrawn.
- G4 PASSED (interim, data-based). Next: P5 solution options.

**Files:** docs/00-brief.md, r15/r16/r17 docs + csv + scripts, DB (team_quarter, team_r15, prs, pr_commits, rca_class R17), corrections in findings-round-4, gate-4-readiness, problem-statement-v4; decisions, gates, register, plan, README, session-07, agent-reports round 5. **Commit:** see iteration-log row 12.

---

## Iteration 13 - 2026-10-22

**Prompt (verbatim):**
> Yes please and update the Ui page https://claude.ai/artifact/QDD8cDsvj7t1NzPsZgdLdf?sk=WmPCNOEye-jG-cSkbWWnIg#b634839c-1f30.mk0abjdngxb.3256

**Result:**
- `docs/04-solutions/solution-options-v0.md`: SO-1 state races (order-tolerant design + ordering tests + stuck-contact monitor), SO-2 escape-to-test + contract tests, SO-3 E2E trust (>= 95%) then fault/load stage, SO-4 CODEOWNERS >= 3, SO-5 path-based hotspot PR rules for all PRs (not AI-only), SO-6 few blocking checks + retire unused fields. WIP DoD page mapped: harness + chaos yes; RIA agents, mutation testing later. Rollout order and invalidation conditions.
- Shared doc (rev 28): "Solution options (proposed)" section after pilot section; next-steps checklist and lead paragraph updated. One edit narrowed to keep an open comment anchor.
- D-026 (proposed).

**Files:** solution-options-v0.md, 00-brief, README, decision-log, research-plan, iteration-log, full-history, session-08. **Commit:** see iteration-log row 13.

---

## Iteration 14 - 2026-10-22

**Prompt (verbatim):**
> choose from data and continue with the order you proposed. update all in github and the web page to share

**Result:**
- D-027 wave 1 order from data; D-028 specs only (company repos / CI / Jira / prod need approval).
- SO-3A (fork): 2,837 CI runs, 13 workflows. Routing VFM-AFM pipeline pass 1.2%, same 13 out-of-order / retry scenarios fail (hidden PH-1 signal). E2E suites 69-79%, 70% env/setup/fixture. Quarantine useless (465 distinct failing tests). Plan: triage 13 scenarios, pre-test credential/fixture check, isolated data, SLO >= 95% / flaky <= 2%.
- SO-4/5 (fork): owners for 6/10 hotspots; gaps InterVCComm (1), AgentHelper/MCH (0), agent-capacity client (1). Monolith no CODEOWNERS. Size risk in hotspots 21% -> 54%; outside flat. Rules H1-H7: 400-line block, 1000 hard stop, 2 approvals incl. owner, test change, Jira key. Drafts in docs/04-solutions/drafts/.
- SO-1 (fork): failure modes M1-M7 over 51 CFBs; M1-M4 = 23/107 valid (21%), 92 incidents. Proto 80 RPCs, no version/sequence. Monitor 5 invariants (shadow 30 days). Design: shared lib with per-contact version, idempotent apply, stale reject, outbox. Test matrix M1-M4.
- Own: SO-2 escape-to-test spec; measurement plan + scripts/db/metrics.py (metrics_monthly; S5 baseline 1).
- Shared doc updated with wave 1 table.

**Files:** docs/04-solutions/* (wave-1-plan, so1, so2, so3a, so4-so5, measurement-plan, drafts/), data/aggregates so1/so3a/so45, scripts/db so1/so3a/so45/metrics, DB tables; decisions, brief, README, DB README, session-09. **Commit:** see iteration-log row 14.
- Shared doc updated (rev 29): "Wave 1: order chosen from data" table under Solution options (no logins).

---

## Iteration 15 - 2026-10-22

**Prompt (verbatim):**
> No you are not openning pr or cahnges. I want you to make till now a sommery. and over all data that puuled and analyze - quality have been goes down what need to done and improve. what and which gate need to add and what I have not meantion that need to be done for govrancy and quality improvements checking all needed to imrpve and the end goal not have bug in production (of cours as minimum that can be)

**Result:**
- D-029: no PRs or changes in company systems. Saved to memory.
- `docs/05-summary/summary-and-recommendations.md`: (1) decline evidence; (2) 7 ranked causes, AI not per-change cause; (3) gates G1 Design, G2 PR, G3 Build, G4 Test health, G5 Pre-release, G6 Deploy, G7 Escape - all blocking, mapped to causes and today's state; RIA agents and mutation deferred; (4) not-asked gaps: governance owner/sponsor, quality data (invalid 51%, caused-by 2.7%), traceability, detection/SLOs, migration register, AI governance, knowledge risk, secrets in work items, data platform; (5) end goal: rare escapes, caught before customers, no repeats, with targets.
- Shared doc (rev 30): new "Summary and recommendations" section after status.

**Files:** summary-and-recommendations.md, README, brief, decision-log, iteration-log, full-history, session-10. **Commit:** see iteration-log row 15.
