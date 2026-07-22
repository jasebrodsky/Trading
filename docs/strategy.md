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

### Earnings — flatten then refill

Overrides the band table when a short is open on an underlying with **earnings within 5 trading days**:

1. **Flatten:** buy to close the short (close-only). Remove event exposure.
2. **Do not rewrite / do not sell a new short** until after that earnings print.
3. **Refill:** on a later check (post-earnings), use normal bands — typically sell new ~0.20–0.30Δ, ~30–45 DTE when ready.

Close-only flatten still must pass spread / review / BP / coverage gates on the **BTC leg**. If the close leg fails those gates → escalate (do not force a bad fill).

## Structure rules

- Covered calls only on symbols with ≥100 shares per contract sold
- Optional: 1× SPY cash-secured put under same Δ bands (put Δ magnitude)
- Single-leg only (MCP Level 2)
- Prefer Aug/monthly liquidity; avoid forced weeklies unless defending

## Autonomy — Tier C

After `review_option_order`, **auto-place** when all gates pass. Escalate to human when any gate fails.

### Auto-place gates (all required)

1. Account is Agentic `420763765`
2. Action matches band table (harvest or defend) **or** earnings flatten (close-only BTC)
3. New short strike ≈ 0.20–0.30Δ when opening/rewriting — **omit open leg** for close-only (BP/shares block, **or** earnings flatten)
4. Net roll is credit **or** defend debit ≤ remaining extrinsic on the closed leg + $50 buffer — **N/A for close-only** (debit to flatten is allowed)
5. Bid–ask spread on each leg ≤ 15% of mid (or ≤ $0.10 absolute for cheap options)
6. No pending assignment / exercise quantities on the position
7. `review_option_order` returns no blocking / hard-fail alerts user must acknowledge specially
8. Regular market hours (or explicit dry-run)

### Always escalate (do not auto-place)

- Buying power insufficient after review
- Quantity / share coverage mismatch
- Wide spread or missing quotes
- Multi-leg needed
- Any uncertainty on covered vs naked
- Attempting to **sell / rewrite** a short when earnings are within 5 trading days (flatten-only window)

## Cadence

- **Daily** after open via Slack automation (noon ET) or on demand
- Weekend / closed: dry-run report only — no `place_option_order`
