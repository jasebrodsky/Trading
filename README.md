# Trading

Personal options overlay for Robinhood — covered-call / CSP management via Cursor + Robinhood MCP.

**Not part of HelloAgain.** Open this folder as its own Cursor workspace when running trading agents.

## Strategy

Delta-band covered calls on the Agentic account:

- Enter ~0.20–0.30Δ, 30–45 DTE
- Harvest / roll when Δ &lt; ~0.12
- Defend shares / roll when Δ &gt; ~0.45
- Autonomy: **Tier C** — auto-place within rules after `review_option_order`; escalate exceptions

Details: [docs/strategy.md](docs/strategy.md) · Agent playbook: [.cursor/skills/robinhood-delta-band-cc/SKILL.md](.cursor/skills/robinhood-delta-band-cc/SKILL.md)

## Quick start

1. Open `/Users/jbrod/Apps/Trading` in Cursor (separate window from HelloAgain).
2. Ensure Robinhood MCP is connected (`user-robinhood-trading`).
3. Prompt: `Run covered-call delta band check` (markets open) or `Dry-run covered-call delta band check` (weekend / closed).
4. Slack: use the two automations in [docs/slack-automations.md](docs/slack-automations.md) (daily report ≠ continue/stop gate).

## Strategy canvas

Visual reference for program stats, sleeves/bands, and ops dashboard:

- Open [`canvas/index.html`](canvas/index.html) (or `cd canvas && python3 -m http.server 8765`)
- Snapshot data: [`canvas/data/snapshot.json`](canvas/data/snapshot.json)
- **Public hosting (GCP):** [docs/gcp-hosting.md](docs/gcp-hosting.md) — static site + JSON on GCS; agent refresh → commit → Cloud Build deploy

Prompt **Refresh the strategy canvas snapshot** after a daily check to update the numbers. Add **and publish to GCP** to commit and deploy the live site.

## Layout

| Path | Purpose |
|------|---------|
| `canvas/` | Strategy + stats ops canvas |
| `docs/strategy.md` | Rules, bands, account scope |
| `docs/slack-automations.md` | Slack daily-check + continue/stop prompts |
| `runbooks/` | Dated session notes / checklists |
| `.cursor/skills/robinhood-delta-band-cc/` | Tier C agent skill |

## Safety

- Trades real money on the Agentic account only.
- Informational P&amp;L — not tax or investment advice.
- No secrets in this repo (no API keys, no full account dumps in commits).
