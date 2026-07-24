# Strategy canvas

Open [`index.html`](index.html) for the Agentic options program dashboard.

## Sections

| Anchor | Contents |
|--------|----------|
| `#stats` | Account scoreboard, open book (credit + extrinsic), accumulation, winners/losers |
| `#ops` | Callouts, zone counts, coverage heatmap, BP/collateral runway, earnings, assignment watch |
| `#returns` | Premium ledger (credits/debits), return stack, performance pulse, sleeve income, capital mix, equity curve |
| `#outlook` | Forward premium, idle-fill estimate, expiry calendar, index sleeve |
| `#strategy` | Sleeves + delta bands |
| `#projects` | Roadmap |

## View locally

```bash
cd canvas && python3 -m http.server 8765
```

Then open http://localhost:8765

Opening the file directly also works — embedded fallbacks load if `fetch` can’t reach `data/*.json`.

## Data

| File | Purpose |
|------|---------|
| `data/snapshot.json` | Full live snapshot (refresh from Robinhood MCP) |
| `data/projects.json` | Roadmap mirrored from `docs/projects.md` |

After a daily check, prompt: **Refresh the strategy canvas snapshot** — rebuilds ledger, ops, performance, and forward income, and keeps the HTML fallback in sync.

The canvas **Reload snapshot** button only re-reads `data/snapshot.json` from disk. It cannot call Robinhood. Use **Copy live-refresh prompt** (or ask Cursor) for live broker data.
