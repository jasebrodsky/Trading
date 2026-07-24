# Strategy canvas

Open [`index.html`](index.html) for a visual reference of the Agentic options program: scoreboard, open book, sleeves/bands, and future projects.

## View locally

```bash
cd canvas && python3 -m http.server 8765
```

Then open http://localhost:8765

Opening the file directly also works — embedded fallbacks load if `fetch` can’t reach `data/*.json`.

## Data

| File | Purpose |
|------|---------|
| `data/snapshot.json` | Account / P&L / open book / idle CC (refresh from Robinhood MCP) |
| `data/projects.json` | Roadmap mirrored from `docs/projects.md` |

After a daily check, prompt: **Refresh the strategy canvas snapshot** — rewrite `snapshot.json` and keep the HTML fallback in sync if you change fields.
