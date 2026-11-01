# External research 2024-2026: AI, quality gates, team structure

Scope: AI-assisted development and quality. Gates. Pod structure. AI test agents.
Method: web search, 2026-10-28. Many numbers come from secondary write-ups of primary reports. These are marked "(2nd)". Check the primary source before you quote a number in a decision paper.
Trust: HIGH = primary or peer-reviewed. MEDIUM = industry survey or telemetry study. LOW = vendor or opinion (VENDOR).

## Summary

- AI raises delivery speed but not stability. DORA 2024: AI link to lower stability. DORA 2025: throughput link turned positive, instability link stayed.
- DORA 2025 says AI is an amplifier. Small batches, version control, quality internal platforms, and a clear AI stance decide if AI helps.
- Telemetry (Faros, VENDOR): high-AI teams merge far more PRs. PRs are much bigger. Review time rises. Org-level DORA metrics do not improve.
- Code-level data is mixed. GitClear: more duplication, less refactoring (VENDOR). CodeRabbit: about 1.7x more issues per AI PR (VENDOR). GitHub RCT: better tests pass rate (VENDOR, own product).
- Only one independent RCT on experienced devs (METR 2025): 19% slower with AI. Devs still felt faster. Small sample (16 devs). Early-2025 tools.
- Security: about 40% (2021 Copilot study) and 45% (Veracode 2025, VENDOR) of AI code samples had security flaws. Models do not improve much on security.
- Trust is falling. Stack Overflow 2025: 46% distrust AI accuracy (31% in 2024). Only about 3% "highly trust".
- Test signal matters. Google: about 1.5% of test runs are flaky. Flaky tests hide real failures. Bad signal breaks any blocking gate.
- Mutation testing works at scale when it targets only the changed code in review (Google). Meta pairs it with LLM test generation. Engineers accepted 73% of generated tests.
- Platform and team model: thin platform, stream-aligned teams, enabling teams. DORA 2025: about 90% of orgs have an internal platform. Quality of the platform decides AI payoff.

## Theme 1: AI and software quality / stability

| Claim | Number | Source | Year | Trust |
|---|---|---|---|---|
| AI adoption linked to lower delivery stability and lower throughput | Per 25% more AI adoption: stability -7.2%, throughput -1.5% (2nd; one source says -14% stability, not confirmed) | [DORA 2024 report](https://dora.dev/research/2024/dora-report/) ; [InfoQ](https://www.infoq.com/news/2024/11/2024-dora-report/) | 2024 | MEDIUM |
| In 2025 AI links positively to throughput. Instability link remains. AI is an amplifier | Survey of about 5,000 pros. About 90% use AI (2nd) | [DORA 2025 report](https://dora.dev/research/2025/dora-report/) ; [Google Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report) | 2025 | MEDIUM |
| DORA AI Capabilities Model: 7 capabilities that make AI pay off (clear AI stance, healthy data, AI-accessible internal data, strong version control, small batches, user focus, quality internal platform) | 7 capabilities (list from model memory, not fetched from primary) | [DORA AI Capabilities Model](https://cloud.google.com/resources/content/2025-dora-ai-capabilities-model-report) | 2025 | MEDIUM |
| High-AI teams: more PRs, bigger PRs, longer review. No org-level DORA gain | +98% PRs merged, +154% PR size, +91% review time, +9% bugs/dev (2nd, via Augment). Other Faros pages show different values | [Faros AI Productivity Paradox](https://faros.ai/research) | 2025 | LOW (VENDOR) |
| Experienced devs were slower with AI in an RCT. They thought they were faster | -19% speed. 16 devs, 246 tasks. Forecast +24%, felt +20% | [METR](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) | 2025 | HIGH (small sample) |
| Field experiments: AI assistant raised completed tasks | +26% tasks, 4,867 devs, 3 firms. GPT-3.5 era (2022-23 data) | [Cui et al., MIT draft](https://economics.mit.edu/sites/default/files/inline-files/draft_copilot_experiments.pdf) | 2024 | HIGH |
| GitHub RCT: Copilot code passed more tests and had fewer readability errors | +53.2% pass all 10 tests. 202 devs. (Press says 56%.) | [GitHub blog](https://github.blog/2024-11-18-does-github-copilot-improve-code-quality-heres-what-the-data-says/) | 2024 | LOW (VENDOR, own product) |
| Uplevel: no productivity gain, more bugs with Copilot | +41% bug rate. About 800 devs. Only press coverage found | [DevOps.com](https://devops.com/study-finds-no-devops-productivity-gains-from-generative-ai/) | 2024 | LOW (VENDOR, 2nd) |
| Duplicated code up, refactoring down | 211M changed lines. Moved code from about 25% (2021) to under 10% (2024). Copy-paste lines passed moved lines in 2024 | [GitClear 2025 (via DevClass)](https://devclass.com/2025/02/20/ai-is-eroding-code-quality-states-new-in-depth-report/) | 2025 | LOW (VENDOR) |
| AI-coauthored PRs have more issues | About 1.7x (10.83 vs 6.45 per PR). 470 OSS PRs | [CodeRabbit report](https://www.businesswire.com/news/home/20251217666881/en/CodeRabbits-State-of-AI-vs-Human-Code-Generation-Report) | 2025 | LOW (VENDOR, sells review tool) |
| About 40% of Copilot outputs were vulnerable (CWE scenarios) | 1,689 programs, 89 scenarios. 2021 preprint, CACM 2025 | [Pearce et al.](https://arxiv.org/pdf/2108.09293) | 2021/2025 | HIGH (old model) |
| 45% of AI code samples failed security tests | 80 tasks, 100+ LLMs | [Veracode GenAI Code Security Report](https://www.veracode.com/genai-code-security-report) | 2025 | LOW (VENDOR) |
| Developers distrust AI output more each year | 46% distrust (31% in 2024). 33% trust. 3% highly trust. 66% say "almost right but not quite" | [Stack Overflow Survey 2025](https://survey.stackoverflow.co/2025/ai) | 2025 | MEDIUM |

## Theme 2: Gates, guardrails, CI policy

| Claim | Number | Source | Year | Trust |
|---|---|---|---|---|
| Flaky tests are a steady share of runs. They hide real failures | About 1.5% of runs flaky. About 16% of tests show some flakiness. About 84% of pass-to-fail changes involve a flaky test (2nd) | [Google Testing Blog (J. Micco)](https://testing.googleblog.com/search/label/John%20Micco) | 2016-17 (older, still the best public data) | MEDIUM |
| Mutation testing works at scale if limited to changed code in code review | 24,000+ devs, 1,000+ projects, 17M mutants, 760k changes | [Practical Mutation Testing at Scale (Google)](https://arxiv.org/pdf/2102.11378) | 2021 | HIGH |
| Mutation-guided LLM test generation: engineers accept most tests | 73% accepted (2nd; pilot Oct-Dec 2024, not checked in paper) | [Meta ACH paper](https://arxiv.org/abs/2501.12862) | 2025 | HIGH (paper) / numbers 2nd |
| Error budget policy: change is the main outage cause. Budget gone leads to release freeze, except P0 and security fixes | Changes about 70% of outages (Google). 99.9% SLO = 0.1% budget | [SRE Workbook: Error Budget Policy](https://sre.google/workbook/error-budget-policy/) | 2018 (still current) | HIGH (primary, practice guide) |
| Google review practice: small changes, fast reviews, one reviewer plus owner | 9M reviewed changes studied | [Modern Code Review at Google](https://research.google/pubs/modern-code-review-a-case-study-at-google/) | 2018 | HIGH (old) |
| Small batches, feature flags, progressive delivery lower change risk | No primary number found. Only vendor claims. DORA lists small batches in AI model | [DORA](https://dora.dev/capabilities/working-in-small-batches/) | 2025 | MEDIUM (claim), LOW (vendor numbers) |

## Theme 3: Team structure and platform

| Claim | Number | Source | Year | Trust |
|---|---|---|---|---|
| Stream-aligned teams own flow. Platform teams serve them as customers. Enabling teams help for a limited time. "Thinnest viable platform" | None (framework) | [Team Topologies](https://teamtopologies.com/key-concepts-content/what-are-the-core-team-types-in-team-topologies) | 2019+ | LOW (opinion, widely used) |
| Quality of internal platform decides if AI pays off. Low-quality platform: AI gain is small | About 90% of orgs have platform. About 75% have platform team (2nd) | [DORA 2025](https://dora.dev/research/2025/dora-report/) | 2025 | MEDIUM |
| CNCF platform maturity model: 5 aspects, 4 levels. Self-assessment. Weakest area in a public-sector survey: measurement | 5 aspects x 4 levels | [CNCF TAG App Delivery](https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/) | 2023 | MEDIUM |
| Paved road / golden path (Netflix, Spotify): a supported default path, not a mandate | Not verified in primary Netflix or Spotify source | Not found. Search a Netflix tech blog and Spotify Backstage docs | - | LOW |
| SPACE / DevEx: do not measure by one metric. Use several dimensions | Not searched this round | [SPACE framework (ACM Queue)](https://queue.acm.org/detail.cfm?id=3454124) | 2021 | HIGH (not re-verified) |

## Theme 4: Agentic testing and AI governance

| Claim | Number | Source | Year | Trust |
|---|---|---|---|---|
| TestGen-LLM at Meta: filters keep only tests that build, pass reliably, and add coverage | 75% built, 57% passed reliably, 25% added coverage. 73% of recommendations accepted. 11.5% of classes improved | [Meta TestGen-LLM (FSE 2024)](https://arxiv.org/pdf/2402.09171) | 2024 | HIGH |
| Filter-then-accept design is key: LLM output is untrusted until a tool checks it | Same paper | Same | 2024 | HIGH |
| OWASP Top 10 for LLM Apps 2025 lists risks such as prompt injection, improper output handling, supply chain, excessive agency | 10 items | [OWASP GenAI](https://genai.owasp.org/llm-top-10/) | 2025 | MEDIUM |
| NIST AI 600-1 (Generative AI Profile) and SP 800-218A (secure development for generative AI) give governance baselines | Not verified in this round | [NIST AI 600-1](https://www.nist.gov/itl/ai-risk-management-framework) | 2024 | HIGH (not re-verified) |
| Google SRE-style or Meta data on AI agents as test authors at scale | Gap: no strong independent field data found | - | - | - |

## Agrees with internal findings

- Instability with AI adoption: DORA 2024 and 2025 link more AI use to lower delivery stability. Faros shows bugs per dev up (VENDOR). Internal data does not show AI as the cause of our severe-bug rise (not riskier per change). Both point to batch size and volume, not to the author.
- AI PRs bigger: Faros shows PR size up sharply (VENDOR). DORA lists small batches as an AI capability.
- Review depth vs PR size: Faros shows review time up while PR size up. Google review study backs small changes. Cause (shallow review or deferred review) is not proven.
- Risk-based gate floor: Google mutation testing on changed code, error budget freeze policy, and TestGen-LLM filters all use small automatic checks on changes.
- Free means, fixed outcomes: DORA says AI is an amplifier of team practice. This supports one outcome contract plus local method.
- Customers find P1 first: SRE practice (SLO, error budget) exists because detection in production is the final signal. No external number for the "96%" figure.

## Contradicts or adds

- AI PR not riskier per change (internal): CodeRabbit (VENDOR) says about 1.7x more issues per AI PR. GitClear says worse code health. GitHub RCT (VENDOR) says better. Evidence is split. Internal data is better than all of these for your own context. Keep it.
- Add: DORA 2025 says throughput gain is real. Do not frame AI only as a risk.
- Add: METR shows a perception gap. Developer self-reports on AI value are weak evidence. Use measured outcomes.
- Add: Flaky tests. A blocking gate needs a trusted test signal. Gate floor must include a flake budget or quarantine rule, or pods will bypass it.
- Add: Platform quality. DORA says platform quality decides AI payoff. A free-means model needs a good paved road. Free means without a road adds cost per pod.
- Add: Security flaws in AI code are stable across studies (about 40-45%). Put a security scan in the floor.
- Add: Progressive delivery and feature flags have little hard public evidence. Use as practice, not as proven.
- Gap: no independent data on blocking gates versus advisory gates in autonomous pods. This is open.

## Sources

- DORA 2024: https://dora.dev/research/2024/dora-report/
- DORA 2025: https://dora.dev/research/2025/dora-report/
- DORA AI Capabilities Model: https://cloud.google.com/resources/content/2025-dora-ai-capabilities-model-report
- METR: https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
- Cui et al. field experiments: https://economics.mit.edu/sites/default/files/inline-files/draft_copilot_experiments.pdf
- GitHub Copilot quality study (VENDOR): https://github.blog/2024-11-18-does-github-copilot-improve-code-quality-heres-what-the-data-says/
- GitClear (VENDOR): https://devclass.com/2025/02/20/ai-is-eroding-code-quality-states-new-in-depth-report/
- Faros (VENDOR): https://faros.ai/research
- Uplevel (VENDOR, 2nd): https://devops.com/study-finds-no-devops-productivity-gains-from-generative-ai/
- CodeRabbit (VENDOR): https://www.businesswire.com/news/home/20251217666881/en/CodeRabbits-State-of-AI-vs-Human-Code-Generation-Report
- Veracode (VENDOR): https://www.veracode.com/genai-code-security-report
- Pearce et al.: https://arxiv.org/pdf/2108.09293
- Stack Overflow 2025: https://survey.stackoverflow.co/2025/ai
- Google flaky tests: https://testing.googleblog.com/search/label/John%20Micco
- Google mutation testing: https://arxiv.org/pdf/2102.11378
- Meta ACH: https://arxiv.org/abs/2501.12862
- Meta TestGen-LLM: https://arxiv.org/pdf/2402.09171
- Google SRE error budget policy: https://sre.google/workbook/error-budget-policy/
- Google code review: https://research.google/pubs/modern-code-review-a-case-study-at-google/
- Team Topologies: https://teamtopologies.com/key-concepts-content/what-are-the-core-team-types-in-team-topologies
- CNCF platform maturity: https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/
- SPACE: https://queue.acm.org/detail.cfm?id=3454124
- OWASP LLM Top 10: https://genai.owasp.org/llm-top-10/
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
