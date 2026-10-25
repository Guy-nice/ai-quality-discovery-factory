@AGENTS.md

## Claude Code routing

- Default model in this repo is Sonnet (`.claude/settings.json`). Switch with `/model opus` only for synthesis or design steps, then back with `/model sonnet`.
- Data work goes to the `data-worker` subagent (runs on Sonnet). Forks run on the parent model, so keep forks for synthesis only.
- Use `/effort low` for commits, logs and formatting. Check spend with `/cost` at session end.
