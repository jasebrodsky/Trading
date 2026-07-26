# Income sweep — Amex savings

Fund external savings from options income on the Agentic account (••••3765). This is **not** an MCP action — Robinhood does **not** offer recurring outbound withdrawals; you initiate a **manual ACH withdrawal** each month. Agents **report** sweep readiness on daily checks so you know when to pull the trigger.

## Target

| Field | Value |
|-------|--------|
| Amount | **$3,000** per month |
| Destination | **American Express High Yield Savings** (linked external bank) |
| Schedule | **15th of each month** (or next business day if weekend/holiday) |
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
- If `sweep_ready`: user can submit the **$3k manual withdrawal** on the 15th.
- If not: **skip or reduce** this month’s sweep — report **sweep blocked** with shortfall `$3,000 − sweep_available`.

Do **not** sweep from buying power, margin, or unsettled option credits. T+1 settlement applies to recent closes.

## Income context

When the covered-call + CSP book is **fully deployed**, net cash flow is typically **~$6k–8k/month** (often more, sometimes less in heavy-defend months). The **$3k sweep** is the primary external savings leg — strategy income funds household savings instead of leaning on inherited IRA distributions.

Inherited IRA auto-withdrawals can stay **paused** while options income covers spending and this sweep; optional year-end IRA draws for bracket top-up remain a separate tax decision (CPA).

## Robinhood limitation — no recurring withdrawals

Robinhood supports **recurring deposits** (bank → Robinhood) and **recurring investments** (auto-buy stocks/ETFs). It does **not** support scheduled or recurring **withdrawals** from investing to an external bank.

Outbound transfers are **one-time only**: Account → Menu → **Transfers** → **Withdraw** → amount → destination → Transfer. See [Robinhood withdraw help](https://robinhood.com/us/en/support/articles/withdraw-money-from-robinhood/).

## Manual monthly procedure (15th)

1. Check the daily report (or Robinhood) for **sweep ready** / withdrawable cash.
2. Robinhood app → **Transfers** → **Withdraw**.
3. **From:** Individual investing (Agentic ••••3765) · **To:** Amex savings · **Amount:** $3,000 (or less if blocked).
4. Confirm **withdrawable cash** ≥ amount before submitting.
5. Optional: calendar reminder on the 15th; daily Slack check around **13th–17th** flags readiness.

Amex may allow scheduling inbound transfers from a linked Robinhood account on their side — check Amex transfer UI; not all banks support pull scheduling from brokerage accounts.

## Agent reporting

On **every** daily check (and on-demand delta-band runs), include one **Income sweep** line in the portfolio message:

| When | What to show |
|------|----------------|
| Any day | Cash, BP, sweep_available, **ready / blocked** ($shortfall if blocked), next sweep date (15th or next biz day) |
| **13th–17th** (±2 days around sweep) | Same, plus **CTA: manual $3k withdraw today if ready**; flag if defend debits or CSP collateral could block cash |

Escalate (do not auto-transfer via MCP — no such tool):

- `sweep_available` &lt; $3k for **two consecutive** daily checks mid-month → note in overlay message; suggest skipping or partial sweep unless user frees cash (harvest, close CSP, etc.).
- User asks to change amount, date, or destination → edit this doc; no Robinhood setting to update.

## Related docs

- [strategy.md](strategy.md) — sleeves, premium targets, BP buffer
- [slack-automations.md](slack-automations.md) — daily-check prompt includes sweep line
- [.cursor/skills/robinhood-delta-band-cc/SKILL.md](../.cursor/skills/robinhood-delta-band-cc/SKILL.md) — snapshot procedure
