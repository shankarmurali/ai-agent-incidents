# Maintaining the AI Agent Incident Tracker

A 15-minute routine, every 3–4 days. Everything happens in the browser at
`github.com/shankarmurali/ai-agent-incidents` — no local setup, no keys, no cost.

---

## Step 1 — Find candidates (5 min)

Open your Signal Desk brief:
`github.com/shankarmurali/signal-desk/blob/main/briefs/latest.md`

Scan for anything describing an AI agent that **did something** harmful — deleted,
exfiltrated, executed, paid, or shipped something it shouldn't have. News about
models being merely wrong or biased doesn't qualify; the tracker records *actions
with consequences*.

An incident is tracker-worthy when all three are true:

1. An AI agent or assistant took (or was manipulated into) a concrete harmful action.
2. There is at least one public source you can link.
3. You can describe the failure mode — what technically went wrong.

When in doubt, wait a day or two: early reports firm up fast, and a better-sourced
entry beats a fast one.

## Step 2 — Add the incident (7 min)

1. In the repo, open the `incidents/` folder → **Add file → Create new file**.
2. Name it: `YYYY-MM-DD-short-slug.yml` (date of the incident, not today).
3. Open an existing incident file in another tab and copy its full contents —
   a filled-in example is easier to adapt than the blank template.
4. Replace **every** field:
   - `id`: next unused number for the year (check the newest existing file).
   - `category`: must be exactly one of:
     `destructive-action` · `prompt-injection-exfiltration` ·
     `prompt-injection-code-execution` · `prompt-injection-manipulation` ·
     `agentic-supply-chain`
   - `status`: `confirmed` (CVE, vendor acknowledgment, or multiple independent
     confirmations) / `user-reported` (public account, not independently verified) /
     `disputed`. Be conservative — the tracker's credibility lives in this field.
   - `sources`: at least one public link. Prefer the most primary source available.
   - Everything else: plain, neutral, 2–4 sentences per field. Record, not scorecard.
5. **Never include** exploit code, payloads, or proof-of-concept scripts —
   descriptions and links only.
6. **Commit changes** with a short message like `Add <incident slug>`.

## Step 3 — Verify (2 min)

1. **Actions** tab → the "Build site" run for your commit should go green in ~1 minute.
2. Refresh the live site: `shankarmurali.github.io/ai-agent-incidents` —
   your entry appears at the top (newest first), and its category shows in the filters.

**If the run shows a red X:** click into it → expand the failing step. The error
names your file and the missing field (e.g. `2026-08-15-foo.yml: missing impact`).
Open your file, pencil icon, fix, commit — it rebuilds automatically. The live site
never breaks; it stays on the last good version until the fix lands.

## Step 4 — Optional: work the flywheel

A fresh incident is a natural LinkedIn comment or post: two or three sentences of
analysis, linking to your tracker entry rather than only the news article. The
tracker becomes the thing people bookmark; you become the person who maintains it.

---

## Occasionally (monthly, 5 min)

- **Signal Desk health**: Actions tab on the signal-desk repo — the daily runs
  should all be green. A long run of empty briefs usually means a feed moved;
  ask Claude to help update `roster.json`.
- **Update earlier entries**: when a `user-reported` incident gets a vendor
  postmortem or CVE, edit the entry — upgrade `status`, add the new source.
  Updating old entries is what separates a maintained record from a link dump.
- **Handle PRs**: if a contribution arrives, check it against Step 2's rules
  (real sources, honest status, no exploit code, neutral tone) before merging.
  The build validates structure automatically; you judge substance.

## Golden rules

1. Public sources only — never anything known through work.
2. Conservative `status` labels — credibility over completeness.
3. No exploit code, ever.
4. Neutral tone — the tracker keeps records; your LinkedIn commentary carries opinions.
