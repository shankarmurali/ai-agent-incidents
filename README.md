# AI Agent Incident Tracker

A structured, sourced, community-maintained record of **real-world AI agent failures** — destructive actions, prompt-injection exploits, data exfiltration, and agentic supply-chain compromises.

Browse the tracker: enable GitHub Pages (Settings → Pages → Deploy from branch → `main` / `docs`) and it lives at `https://<your-username>.github.io/ai-agent-incidents/`. The dataset is also published as [`docs/incidents.json`](docs/incidents.json) for anyone to build on.

## Why

Agent incidents are scattered across news posts and X threads with no structured home. Researchers, T&S teams, and security engineers need the pattern, not the anecdote: what access did the agent have, what failed, how far did it spread. Each entry captures exactly that, with sources.

## Add an incident (PRs welcome)

Create one YAML file in `incidents/` named `YYYY-MM-DD-short-slug.yml`:

```yaml
id: 2026-004            # year-sequence, next unused number
date: 2026-08-01
title: One-line description of what happened
system: Model or product involved
vendor: Company or ecosystem
category: destructive-action   # or prompt-injection-exfiltration,
                               # prompt-injection-code-execution,
                               # prompt-injection-manipulation,
                               # agentic-supply-chain
status: confirmed | user-reported | disputed (+ CVE if any)
autonomy: How autonomous was the agent, what access did it have
failure_mode: >
  What technically went wrong, in 2-4 sentences.
impact: What was lost, exposed, or executed.
lessons:
  - One-line takeaway
sources:
  - https://link-to-primary-source
```

**Standards:** every entry needs at least one public source; use `user-reported` status for accounts not independently confirmed; write neutrally — this is a record, not a scorecard. The build validates required fields and fails the PR if any are missing.

The site rebuilds automatically on every merge (GitHub Actions). No API keys, no external services, no cost.

## License

MIT for code. Incident entries are factual summaries with links to original reporting.
