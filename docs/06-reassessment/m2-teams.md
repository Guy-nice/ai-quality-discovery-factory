# M2-Teams - Team/POD Source of Truth and Team Variation

**Date:** 2026-10-25 | **Mission v2:** Q-C, gap E5 | **Data:** `team_map`, `agg_m2_team_profiles` in `quality.sqlite`; script `scripts/db/m2_teams.py` | Evidence only, no solution design

## 1. Sources of truth for teams and ownership

| Source | Coverage | Freshness | Usable as team key? |
|---|---|---|---|
| **Jira "Team Name" (cf_10098)** | 98% of CFBs (empty 1.7%); 205 team values since 2025 | Live (set per issue) | **Yes, best current key** for defects. Renames and splits exist (e.g. ACD Admin Bolivia -> Pune; Orchestration II new in 2026) |
| Jira "R&D VP" (cf_14852) | 94% of CFBs | Live | Yes, domain level only |
| GitHub org teams (`inContact`) | 295 teams; 14 of 40 profiled Jira teams match by name | Live | Partial. Names differ from Jira (e.g. `orchestration-allmembers`, `dforeportingpune`) |
| CODEOWNERS | Monolith: none; pilot services: `*` or team-only rules (SO-4/5) | - | No |
| Confluence "Component Ownership by Team" (IN 4256596006, 2026-10-16) | Security & Compliance teams only (S&C-Earth / Jupiter / Omni / Mercury, Pune-DevOps) | Recent | Good model, **local** - not org-wide |
| ServiceNow assignment groups (464 active) | Operational groups; 759 of 887 P1 incidents (2025+) sit in "Service Operations NOC" | Live | **No** for dev teams. Incidents do not carry the owning dev team |
| ServiceNow CMDB services | Not readable with current access | - | Unknown |

**FACT:** There is no single org-wide map of team -> service -> code. **Best current key:** Jira Team Name, normalized; link to code through Jira keys in PRs (works only where commits name keys: monolith 76%, EM 6-17%).

## 2. Team profiles (40 teams with >= 10 valid CFBs, 2025-01..2026-10)

Variation between teams (outcome dimensions have data for all 40; practice dimensions only for 17 teams in pilot repos):

| Dimension | Min | Median | Max | CV | Data |
|---|---|---|---|---|---|
| Valid CFBs (2025-2026) | 12 | 21.5 | 106 | 0.62 | 40 |
| Valid change 2026 vs 2025 (Jan-Oct) | -100% | 0% | +1600% | 2.87 | 33 |
| P1/P2 share of valid CFBs | 10% | 63% | 93% | 0.39 | 40 |
| Incidents per CFB | 1.1 | 2.4 | 10.4 | 0.74 | 40 |
| Invalid share | 6% | 40% | 79% | 0.41 | 40 |
| Median days to fix | 3 | 9.8 | 31 | 0.57 | 40 |
| AI share of fixes | 0% | 11% | 64% | 1.06 | 40 |
| RCA filled (fixed CFBs) | 80% | 100% | 100% | 0.05 | 40 |
| PR median size (lines) | 0 | 124 | 5,078 | 1.53 | 17 (few PRs each) |
| PRs touching tests | 0% | 67% | 100% | 0.57 | 17 |
| CI pass rate per team | - | - | - | - | **missing** (CI data only for pilot repos) |

**R&D VP explains only part of the variation** (share of variance between VPs, eta²): P1/P2 share 0.46, AI share 0.31, invalid share 0.28, days to fix 0.21, incidents per CFB 0.17. **Most variation is between teams inside the same VP.**

## 3. Team archetypes (rule-based, outcome data only)

| Archetype | Rule | Teams | Examples |
|---|---|---|---|
| A. High impact | P1/P2 share and incidents per CFB both >= median | 9 | Orchestration, Advanced Omnichannel Routing, Agni, Dragonfly, Reporting-Pune, Titans, Waves |
| B. Fast growing | Valid CFBs >= +50% (2026 vs 2025) | 8 | Better Calls Devs, IN-Agent Copilot, ACD Admin Pune, Data-Sandy, CXone Studio (CBBA, Sandy), Orchestration II |
| C. High noise | Invalid share >= 50% | 5 | Reporting-CBBA, DX-Platform (Prague, Sandy), Fellowship of the Metrics, Kepler |
| D. Stable / lower impact | Other | 18 | Hornet, Dark Knights, ACD Admin Bolivia, Bugcide Squad, Felix |

Some archetype B growth is re-homing (renamed or split teams), not new defects. Check with team history.

## 4. What the evidence implies (common vs team-specific) - EVIDENCE only

- **EVIDENCE (High):** RCA filling is uniform (80-100%, CV 0.05). A practice that is already common needs no team-specific treatment.
- **EVIDENCE (Medium):** Impact (incidents per CFB 1.1-10.4) and severity mix (P1/P2 10-93%) differ strongly between teams, and mostly inside VPs. So risk differs by team and product area, not only by domain.
- **EVIDENCE (Medium):** Invalid share 6-79% shows different intake and triage practice per team. This affects every outcome metric that counts CFBs.
- **EVIDENCE (Low):** AI share of fixes 0-64% per team. Adoption is uneven, so an AI comparison must control for team.
- **UNKNOWN:** Practice data (review, tests, CI health, PR size) exists only for 17 teams in pilot repos with few PRs each. Team-level practice comparison is **not possible** across the org without a team-to-repo map.

## 5. Gaps and limits

- No team-to-repo map outside the pilot. ServiceNow incidents do not name the dev team.
- Team renames and splits distort year-over-year changes.
- Jira Teams (Atlassian Teams) and CMDB services were not readable (timeouts / permission).
