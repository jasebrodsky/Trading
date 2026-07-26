# Strategy canvas

Open [`index.html`](index.html) for the Agentic options program dashboard.

## Pages

| Anchor | Contents |
|--------|----------|
| `#scorecard` | Suze Orman pulse, account / equity / options totals, capital & YTD mix pies, month-by-month returns |
| `#equities` | Suze Orman pulse, equity summary, sleeve & top-holdings pies, share book |
| `#options` | Suze Orman pulse, options summary, CC/CSP pies, month-by-month credits vs debits, tables, BP |

Nav is sticky at the top. Default page is **Scorecard**.

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
| `data/equities.json` | Equity book with avgCost / unrealized (optional; falls back to snapshot) |

After a daily check, prompt: **Refresh the strategy canvas snapshot** — rebuilds ledger, ops, and keeps the HTML fallback in sync.

The canvas **Reload snapshot** button only re-reads `data/snapshot.json` from disk (or the hosted URL). It cannot call Robinhood. Use **Copy live-refresh prompt** (or ask Cursor) for live broker data.

## Public hosting (Google Cloud)

Full setup: [docs/gcp-hosting.md](../docs/gcp-hosting.md)

1. GCS bucket serves `canvas/` (HTML + `data/*.json` at the same paths).
2. Agent writes `snapshot.json` via MCP → commits → push to `main`.
3. Cloud Build runs `cloudbuild.yaml` → `gsutil rsync` to the bucket.
4. Public URL: `https://storage.googleapis.com/YOUR_BUCKET/index.html`

Manual deploy: `./scripts/deploy-canvas-gcs.sh YOUR_BUCKET`

## Suze pulse voice

**Listen** uses [ElevenLabs](https://elevenlabs.io) neural TTS (assertive American female — Suze-style energy, not a likeness clone). Browser TTS is the fallback.

1. Copy `data/voice-config.example.json` → `data/voice-config.json` and add your API key, **or**
2. Click **Listen** and paste the key when prompted (saved in `localStorage` only).

`voice-config.json` is gitignored.
