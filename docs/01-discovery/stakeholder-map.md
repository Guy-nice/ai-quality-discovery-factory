# Stakeholder Map - Pilot SMEs

**Version:** v0 | **Date:** 2026-10-22 | **Research item:** R12a | **Data:** `stakeholders` table, [r12-stakeholders.csv](../../data/aggregates/r12-stakeholders.csv)

Roles are **guessed** from Git and Confluence activity. Only Kevin Pyles has a confirmed title. The ADR architect fields say "TBD". The lead must confirm the roles before contact.

| # | Name | Role (guess) | Area | Hypotheses | Evidence |
|---|---|---|---|---|---|
| 1 | Kevin Pyles | Lead QA Architect (named) | Orchestration Core QA, E2E, Go/No-Go | All | Confluence CX 4213801473; acd-playwright-e2e 281 commits |
| 2 | Karthick Chandrasekaran | Tech lead / architect | AFM, contact-retry, agent-capacity, match-distributor | PH-1, PH-2 | Top PR reviewer in 3 routing repos (37/33/43); commits 61/49/34/27 |
| 3 | Kacie Mayberry | Tech lead | VCSvc monolith + State Streams | PH-1, PH-2, PH-3 | 99 VCSvc PR reviews; state-streams commits |
| 4 | Dez Grant | Senior engineer | VCSvc .NET modernization | PH-3 | Confluence IN 3696164975 (multi-TFM); 27 VCSvc commits |
| 5 | Anshul Agarwal | Observability focal | VCSvc resilience, EOR gaps | PH-4, PH-5 | Confluence CX 3893887461, 3894051323, 3893887439 |
| 6 | Puneet Kumar | Architect | EM-TFS boundary, SLO standard | PH-1, PH-2 | Confluence IN 4041444339, 4112547862 |
| 7 | Nichole Proestakis | QA automation lead | Routing integration + ACD E2E tests | PH-1, PH-4 | 142 + 684 commits in test repos |
| 8 | Guy Law | Test-gap focal | AFM tests | PH-1, PH-4 | Confluence IN 4072866234 (Findmatch gap analysis) |

Others (ranks 9-14): Jayakesavan Muthazhagan, Jesse Blanton, Shuchivrat Mayenkar (State Streams), Derick Walburger, Rogerio Valenca da Cruz, Austin Wernli.
Sponsor-level contacts (not SMEs): Namitha Nayak (VP), Steve Gordon (program manager).

## Recommended (D-018)

| Slot | Primary | Backup |
|---|---|---|
| Architect - VC monolith | Kacie Mayberry | Dez Grant |
| Architect - routing services / EM / AFM | Karthick Chandrasekaran | Puneet Kumar |
| QA lead | Kevin Pyles | Nichole Proestakis |

## Gaps

- No Jira assignee / reviewer data was pulled (Atlassian timeouts). R12b will add it.
- Architect titles are not confirmed.
