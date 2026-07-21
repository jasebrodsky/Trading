# Delta-band covered call strategy

## Account

- **Only:** Robinhood Agentic individual account `420763765` (display as ••••3765)
- Must be `agentic_allowed=true` and `option_level_2+`
- Do **not** trade the default individual or IRA from this playbook

## Goal

Steady premium on long stock (and optional SPY CSP), keep shares when wanted, reset income/beta when short Δ dies.

## Bands

| Zone | Short Δ | Action |
|------|---------|--------|
| Target entry | 0.20–0.30 | Sell new CC (or CSP) ~30–45 DTE |
| Harvest | &lt; 0.12 | Buy to close; rewrite down+out at target Δ |
| Hold | 0.12–0.45 | No trade |
| Defend | &gt; 0.45 | Buy to close and/or roll up+out to keep shares |

Dwell: act if outside band for a full session, or Δ moved ≥0.10 from entry since last review.

## Structure rules

- Covered calls only on symbols with ≥100 shares per contract sold
- Optional: 1× SPY cash-secured put under same Δ bands (put Δ magnitude)
- Single-leg only (MCP Level 2)
- Prefer Aug/monthly liquidity; avoid forced weeklies unless defending

## Autonomy — Tier C

After `review_option_order`, **auto-place** when all gates pass. Escalate to human when any gate fails.

### Auto-place gates (all required)

1. Account is Agentic `420763765`
2. Action matches band table (harvest or defend)
3. New short strike ≈ 0.20–0.30Δ (or close-only harvest with no rewrite if BP/shares block)
4. Net roll is credit **or** defend debit ≤ remaining extrinsic on the closed leg + $50 buffer
5. Bid–ask spread on each leg ≤ 15% of mid (or ≤ $0.10 absolute for cheap options)
6. No pending assignment / exercise quantities on the position
7. `review_option_order` returns no blocking / hard-fail alerts user must acknowledge specially
8. Regular market hours (or explicit dry-run)

### Always escalate (do not auto-place)

- Earnings within 5 trading days on the underlying
- Buying power insufficient after review
- Quantity / share coverage mismatch
- Wide spread or missing quotes
- Multi-leg needed
- Any uncertainty on covered vs naked

## Cadence

- **Mon / Wed / Fri** after open (or daily if user asks)
- Weekend / closed: dry-run report only — no `place_option_order`
