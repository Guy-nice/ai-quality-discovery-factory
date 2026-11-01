# Side-by-Side: How the Claude Code Team Does Code Review vs Our Model

**Date:** 2026-11-01 | **Status:** analysis only. It does **not** change the playbook, gate catalog or findings. Items in section 6 are candidates for a later decision. | **Our model:** [pod quality playbook](pod-quality-playbook.md), [gate catalog](gate-catalog.md)

**Source:** [How the Claude Code team does code review](https://claude.dev/blog/solving-code-review-at-anthropic/) - Addy Osmani, Morgan Westlee Lunt, Qing Wang (Anthropic), 2026-10-15. Shared on [X](https://x.com/addyosmani/status/2114604912520921136).

**Trust:** MEDIUM-LOW. It is a self-report by the vendor of the tool it describes, with no outside check. This analysis was also written with Claude. Read the numbers as claims, not proof.

## 1. Their context vs ours

The context decides what we can copy.

| Factor | Claude Code team | Us (CXone) |
|---|---|---|
| Team | Team size not stated. Repo owners and a per-repo trusted list are stated. | Hundreds of pods, many repos, legacy monolith |
| Repos | Several repos: CLI, desktop and web apps, mobile apps. Not in the company monorepo. | Monolith plus many service repos |
| Who writes code | Claude writes ~90% | AI share growing; AI PRs in hotspots 5% to 47% |
| Undo a bad change | Flags off without deploy; revert in minutes; `latest` then `stable` channel | Monolith cannot roll back; toggles only |
| Who finds problems first | Their own staff (heavy internal use) | Customers (96% of P1 via customer cases) |
| Failure cost | Developer tool | Real-time contact center for regulated customers |
| Measurement | Reverts, incidents, human time per PR | Customer bugs; cause known for ~25% only |

**Not stated in the article:** number of people, number of teams or pods, org chart, total number of repos.

**Key point:** their model works because mistakes are **cheap to undo** and **found fast by themselves**. We have neither today. So we cannot copy their end state ("at most one human per PR"). We can copy their **method**.

## 2. Their model in 1 page

**Goal:** least human review time with **no rise in reverts or incidents**. Human time counts twice: time to review plus time to fix bad code.

**Layers (each catches some bugs; few bugs pass all):**

| # | Layer | Blocks? |
|---|---|---|
| 1 | Pre-PR verification: agent shows runnable proof (tests, build, screenshot); fresh-context subagent reviews the diff | No (habit) |
| 2 | AI review on every PR: parallel agents, vote on each finding, style noise removed; tags Important / Nit / Pre-existing | Yes - every finding fixed or resolved with a reason |
| 3 | Security review | Yes - open finding blocks merge |
| 4 | CI: lint, types, tests on all platforms, build; PR template asks "how tested" and "how to revert" | Yes |
| 5 | Human approval scaled by risk of the change (classifier); sensitive paths and CI workflow files always need a person | Yes |
| 6 | Merge queue; feature flags; staff first; staged release channels | Yes (queue) |
| 7 | Fast detection and rollback; weekly on-call; incident review asks "which layer should have caught it?" | Last line |

**Risk tiers:**

| Tier | Examples | Human approvals |
|---|---|---|
| Low | Docs, copy, internal-only, additive behind a flag | 0 (when automated review and security are green) |
| Medium | Normal product changes; caching, auto-updater, system prompts | 1 |
| High | Highest-risk code and listed paths | 2 |

**Approval rules:** tier set by the change, not the author. Only authors on the repo's trusted list get light paths ("generally the team that owns the repo"). The article does not say how people get on the list. Agent approval never counts as human. The person who ran the agent is a required reviewer. Approval covers one commit; new untrusted commits need re-approval.

**How they improve the reviewer:**
- **Incidents as evals:** incident and revert PRs, confirmed by experts, form a test set. The reviewer runs against it daily. A prompt, tool or model change stays only if the score rises.
- **Noise:** each comment is scored by the author's reaction (fixed, wrong, intentional, did not matter). The reviewer also runs on known-clean PRs.
- **Convergence:** one PR went 50+ rounds overnight; ~59% of repeat flags were old code. Fixes: cap at 3 rounds, then diff-only re-review, report the bug class, no repeat findings.

**Their claimed results:**

| Measure | Before | After |
|---|---|---|
| Merged PRs (Jun-Sep) | x | more than 2x |
| Share of PRs reverted (Jun-Sep) | x | down more than 40% |
| PRs with substantive review comments | 16% | 54% |
| Pass after 1 review-and-fix round | 65% | 78% |
| PRs needing 5+ rounds | 8.9% | 1.5% |
| Mean reviews to pass | 2.08 | 1.32 |

## 3. Why their approach works (expert view)

1. **Defense in layers, not one gate.** No single check is trusted. Each layer is cheap and catches a different bug class. This is the "Swiss cheese" model from safety engineering.
2. **The goal is measurable.** "Human time per change, with reverts and incidents as guardrails" can be tracked weekly. "Did someone read the code?" cannot.
3. **Reversibility buys speed.** Cheap undo lets them accept some risk at merge time. Review depth is a function of blast radius and undo cost.
4. **The reviewer is tested like a product.** An eval set from real incidents and a noise measure stop "more findings" from posing as "better review."
5. **Recurring findings are fixed at the source** (lint rule, skill, instruction file). The same bug class stops coming back.
6. **Human attention goes where only humans add value:** should we build it, risky code, architecture, reading evidence, owning the outcome.
7. **Accountability stays human.** "You land it, you own it," blameless incident reviews, and the agent operator counts as a reviewer.

## 4. Where we agree (our model already has it)

| Their practice | Our item | Note |
|---|---|---|
| Risk tier set by the change, not the author | P-01, tiers T1 / hotspot (playbook section 4) | Same principle. We use path lists; they use a classifier. |
| Agent approval never counts; human accountable | P-07, A4 | Same |
| Agent output is checked before trust | P-08, A6 | Same |
| Re-approval on new commits | H7 dismiss stale approvals ([hotspot rules](../04-solutions/drafts/hotspot-pr-rules.md)) | Same |
| Security review blocks | G4.3 | Same |
| CI blocks | G4.1, G4.2 | Same |
| Sensitive paths always need owners | G3.3 code-owner review on hotspot paths | Same idea; their list also has CI workflows |
| Feature flags, staged rollout | G5.2, G6.1 | Same |
| Start strict, relax with evidence | Gate lifecycle (prove before block) | Ours is the mirror: start Visible, block with evidence. Both demand evidence to change the level. |
| Incident review | G8.1 RCA | Theirs adds "which layer should have caught it" |
| Large PRs carry more bugs | Follow-up fixes 21% to 54% by PR size in hotspots | Their reviewer finds issues on most PRs over 1,000 lines. Same direction. |

## 5. Where we differ, and why

| Topic | Claude Code | Our model | Why we differ | Verdict |
|---|---|---|---|---|
| End goal | Fewest humans per PR | Fewer customer-found severe bugs | Our main problem is escapes to customers, not review cost | Keep ours; add human effort as a second metric (C-02) |
| AI reviewer | Required on every PR; findings must be resolved | Not in our gates; agents are Advice (A5) | No evidence yet on our code; their evidence is self-reported | Pilot it (C-03); measure on our escape set first |
| Rollback | Minutes, everywhere | Monolith: toggles only | Architecture | Reversibility before any human-review relaxation |
| Who sees problems first | Internal staff | Customers | Limited internal use of CXone | Internal or test-tenant ring first (C-09) |
| Merge queue | Yes | Not in our model | Not studied in our research | Candidate (C-08) |
| Team learning | Generated explainers, open channels | Owner backups for hotspots | Bus factor 1-2 on hotspot code | Explainers support our owner-backup need (C-10) |

## 6. Candidates for us (not applied - for D-043 decision)

Each candidate names the gate it would extend. None of them changes a current finding.

| # | Candidate | Extends | Why (their evidence + ours) | Effort | Priority |
|---|---|---|---|---|---|
| C-01 | **Escape eval set:** build a test set from our causing PRs, fix commits and reverts. Score any AI reviewer, gate or vendor tool (e.g. Harness) against it before rollout. | Gate lifecycle, X3/X4 | Their main improvement lever. We already have the data: 306 CFB-fix commits, 94 reverted PRs, causal links in `quality.sqlite`. | Low | **1** |
| C-02 | **Human effort metric:** approvals per PR, wait time on a person; guardrails = D6 change safety and D1 | Quality model D1-D8 | Their key metric. We measure outcomes but not review cost. AI raises PR volume, so review cost will grow. | Low | 2 |
| C-03 | **AI review on every PR as a pilot** in X3 pods (Visible first): findings tagged Important / Nit / Pre-existing; every Important finding resolved | New G3.6 (Visible) | Their comment rate 16% to 54%. Their reviewer flags most 1,000+ line PRs - our riskiest band. | Medium | 2 |
| C-04 | **PR template: "How tested", "Risk", "How to revert"** | G2.1, G5.2 | Cheap. "How to revert" forces toggle thinking where the monolith cannot roll back. | Low | **1** |
| C-05 | **Incident review asks "which gate should have caught it?"** and records the gate ID | G8.1 RCA | Links each escape to a gate. This gives the gate lifecycle real evidence. | Low | **1** |
| C-06 | **Review round cap:** after 3 agent-review rounds, rethink the approach; then diff-only re-review | AI working agreement (C5), A-rules | Their 50-round loop; 5+ rounds 8.9% to 1.5%. Needed once pods run agent reviewers. | Low | 3 |
| C-07 | **Always-human paths:** CI workflow files, release and toggle config, billing, auth | G3.3 | Their list. Our hotspot list covers code, not pipeline or release config. | Low | 2 |
| C-08 | **Merge queue** for the monolith main branch | S4 | Prevents two green PRs making a broken main. Not measured in our data (UNKNOWN). | Medium | 3 |
| C-09 | **Internal ring:** internal or test tenants get flags first | G6.1 | Their staff find regressions before users. Our customers find 96% of P1 first. | Medium | 2 |
| C-10 | **Generated explainers** for hotspot modules, kept with the code | C3 owner backups | Lowers bus-factor risk without line-by-line diff reading | Low | 3 |
| C-11 | **Fix recurring findings at the source:** a repeated review or escape class becomes a lint rule, test template or REVIEW.md entry | G8.2 escape-to-test | Same loop as escape-to-test, applied to review findings | Low | 2 |
| C-12 | **Circuit breaker (later):** a pod's revert or incident rise tightens its approval tier automatically | Rule R1 | Not built at Anthropic either. Needs C-02 and per-pod data first. | High | 4 |

## 7. What not to copy (now)

- **"At most one human per PR" as a goal.** It needs fast undo and fast internal detection. We have neither yet. First fix reversibility (toggles, staged rings) and detection (G7.1).
- **Zero human approvals for low-risk changes.** Only after C-01 and C-02 show no rise in escapes on our code.
- **Their numbers as targets.** Their results are self-reported, for the Claude Code repos only, on a developer tool. Team size is not stated.

## 8. Order (proposed)

1. **Now (low effort):** C-04 PR template, C-05 "which gate" field in RCA, C-01 escape eval set from the DB.
2. **Q1 2027 (with X3):** C-03 AI review pilot scored on C-01; C-02 human effort metric; C-07 always-human paths.
3. **April 2027 review:** decide C-03 mode by the gate lifecycle; C-09 internal ring; C-06 if agent reviewers spread.
4. **Later:** C-08 merge queue, C-12 circuit breaker.

## Sources

- [Anthropic: How the Claude Code team does code review](https://claude.dev/blog/solving-code-review-at-anthropic/) (primary)
- [Addy Osmani on X](https://x.com/addyosmani/status/2114604912520921136) (share)
- [Code Review for Claude Code docs](https://code.claude.com/docs/en/code-review)
- [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
