# Pod Quality Self-Assessment

**Date:** 2026-10-28 | **Parent:** [pod quality playbook](pod-quality-playbook.md) | **Time:** about 30 minutes, once per quarter

The pod quality owner fills this in with the pod. It is not a score to compare pods. It shows what the pod must do next. Answer each line Yes, Partly or No. Each line names the evidence to show.

## A. Capabilities (playbook section 3)

| # | Question | Evidence to show |
|---|---|---|
| A1 | Do we have a named quality owner (C1)? | Name in the pod page |
| A2 | Do we have a named release owner (C2)? | Name in the pod page |
| A3 | Is our pod -> service -> repo map entry correct (C3)? | Map entry |
| A4 | Does each hotspot path we own have at least 2 code owners (C3)? | CODEOWNERS file |
| A5 | Do we have a 1-page test strategy (C4)? | Link |
| A6 | Do we have an AI working agreement (C5)? | Link |
| A7 | Do our incidents reach us, with detected-by recorded (C6)? | 3 recent incidents |
| A8 | Does each failing suite have an owner and a triage date (C7)? | Suite list |

## B. Contract (all pods)

| # | Question | Evidence to show |
|---|---|---|
| B1 | Does every report get a type: defect, MI investigation or expectation gap (G0.1)? | Jira filter, last month |
| B2 | Do valid bugs record failure type, detected-by and cause (G0.2)? | Field fill rate |
| B3 | Does every valid P1/P2 bug have an RCA (G8.1)? | RCA list |
| B4 | Does every valid customer bug close with a test link or a reason (G8.2)? | Link rate |
| B5 | Did we review D1-D8 against our own baseline this month (G8.3)? | Review notes |

## C. Floor (gates that block or will block)

| # | Question | Evidence to show |
|---|---|---|
| C1 | Is Sonar a required check in all our repos (G4.2)? | Branch rules |
| C2 | Does the security scan block in all our repos (G4.3)? | Branch rules |
| C3 | Is each E2E suite that blocks at its agreed pass level for 14 days (G4.5)? | Pass-rate chart |
| C4 | Do hotspot PRs stay within the size limit, or carry an approved exception (G3.2)? | PR report |
| C5 | Do risky changes ship behind a registered toggle with an owner (G5.2)? | Toggle list |
| C6 | Does our Go/No-Go use data, not "TBD" (G5.1)? | Last Go/No-Go page |
| C7 | (T1 only) Do we run perf and chaos stages before release (G5.3)? | Last run |
| C8 | (T1 only) Do monitors check our correctness invariants (G7.1)? | Monitor list |

## D. AI use

| # | Question | Evidence to show |
|---|---|---|
| D1 | Are AI-assisted PRs labeled (G2.2)? | Label rate |
| D2 | Does a named person approve every merge (A4)? | Branch rules |
| D3 | Do generated tests prove value (an escape test fails on the pre-fix code) (A6)? | 3 samples |
| D4 | Do we judge AI value by outcomes, not opinion (P-13)? | Metric used |

## E. Result

- Count the No answers in each section. Fix A and B first. They make everything else measurable.
- Send the result to QA&RM. QA&RM uses it to plan enabling help, not to rank pods.
- Repeat each quarter. Pod type (A-D) is reviewed at the same time.
