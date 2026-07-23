# Income sweep — Amex savings

Fund external savings from options income on the Agentic account (••••3765). This is **not** an MCP action — set up the recurring transfer in Robinhood once; agents **report** sweep readiness on daily checks.

## Target

| Field | Value |
|-------|--------|
| Amount | **$3,000** per month |
| Destination | **American Express High Yield Savings** (linked external bank) |
| Schedule | **15th of each month** (Robinhood moves to next business day if weekend/holiday) |
| Source | Robinhood Agentic individual investing — **withdrawable / settled cash only** |

## When it runs (balance gate)

Sweep **only if** withdrawable cash is sufficient **after** reserving:

1. **~$2,000 buying-power buffer** (same buffer as index / accumulation CSP rules in [strategy.md](strategy.md))
2. **Cash-secured put collateral** already held by open short puts

**Formula (agent reporting):**

```
sweep_available = max(0, cash − max(0, 2000 − buying_power) − put_collateral_held)
sweep_ready     = sweep_available ≥ 3000
```

- Use `get_portfolio` for **cash** and **buying power**.
- Infer **put collateral** from open short put positions (`strike × 100 × contracts` per leg) when broker cash holds are not broken out.
- If `sweep_ready`: recurring transfer on the 15th should **clear**.
- If not: Robinhood **pauses** the recurring transfer until balance recovers — report **sweep blocked** with shortfall `$3,000 − sweep_available`.

Do **not** sweep from buying power, margin, or unsettled option credits. T+1 settlement applies to recent closes.

## Income context

When the covered-call + CSP book is **fully deployed**, net cash flow is typically **~$6k–8k/month** (often more, sometimes less in heavy-defend months). The **$3k sweep** is the primary external savings leg — strategy income funds household savings instead of leaning on inherited IRA distributions.

Inherited IRA auto-withdrawals can stay **paused** while options income covers spending and this sweep; optional year-end IRA draws for bracket top-up remain a separate tax decision (CPA).

## Robinhood setup (one-time, manual)

1. Robinhood app → **Transfers** → **Recurring** (or **Transfer to your bank** → schedule recurring).
2. **From:** Individual investing (Agentic ••••3765).
3. **To:** Amex savings (linked ACH account).
4. **Amount:** $3,000 · **Frequency:** Monthly · **Date:** 15th.
5. Confirm Robinhood’s “pause if insufficient funds” behavior is enabled (default).

Re-verify the linked bank and transfer limits after any Robinhood or Amex account changes.

## Agent reporting

On **every** daily check (and on-demand delta-band runs), include one **Income sweep** line in the portfolio message:

| When | What to show |
|------|----------------|
| Any day | Cash, BP, sweep_available, **ready / blocked** ($shortfall if blocked), next sweep date (15th or next biz day) |
| **13th–17th** (±2 days around sweep) | Same, plus note if recurring transfer should fire imminently; flag if a large defend debit or CSP open could block cash |

Escalate (do not auto-transfer via MCP — no such tool):

- Cash &lt; $3k sweep_available for **two consecutive** daily checks mid-month → note in overlay message; suggest skipping manual top-up unless user wants to reduce CSP collateral or buffer.
- User asks to change amount, date, or destination → edit this doc and update Robinhood recurring transfer manually.

## Related docs

- [strategy.md](strategy.md) — sleeves, premium targets, BP buffer
- [slack-automations.md](slack-automations.md) — daily-check prompt includes sweep line
- [.cursor/skills/robinhood-delta-band-cc/SKILL.md](../.cursor/skills/robinhood-delta-band-cc/SKILL.md) — snapshot procedure
