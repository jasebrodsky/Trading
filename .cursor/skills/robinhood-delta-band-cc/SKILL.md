---
name: robinhood-delta-band-cc
description: >-
  Runs Tier C delta-band covered-call / CSP management on the Robinhood Agentic
  account via MCP — harvest low Δ, defend high Δ, auto-place within gates.
  Use when the user asks for a covered-call delta check, roll plan, options
  overlay automation, or "run the trading strategy".
---

# Robinhood delta-band covered calls (Tier C)

Read [docs/strategy.md](../../../docs/strategy.md) first. Account: Agentic `420763765` only.

## Triggers

- "Run covered-call delta band check"
- "Run the trading strategy"
- "Roll / harvest options on Agentic"
- "Dry-run covered-call delta band check"

These triggers **are the go-ahead** for the **check/report** path. Do not invent an EXECUTE/SKIP approval gate, wait for emoji ack, or ask whether to proceed before snapshotting. Slack/desktop/cloud invocations of the trigger phrases above mean: run snapshot → classify → propose → gate-evaluate → report **now**.

### Slack automations (two roles)

See [docs/slack-automations.md](../../../docs/slack-automations.md) for copy-paste prompts.

| Role | When | `place_option_order`? |
|------|------|----------------------|
| Daily check / dry-run / "Run covered-call…" | Schedule or explicit check prompt | **Never** in that run |
| Continue/stop gate | Thread reply `continue`/`stop` (or ✅/❌) **after** a daily summary | Only on EXECUTE + all gates pass |

If you are the continue/stop agent and the message is itself a new check/dry-run kickoff: do **not** ask EXECUTE/SKIP — say it belongs to the daily-check automation and exit without trading.

Interactive Cloud/desktop sessions (no Slack continue/stop automation in play): after the report, Tier C may auto-place within gates in the **same** turn unless the user said dry-run.

## Procedure

### 1. Preconditions

1. Confirm workspace is the Trading repo (not HelloAgain).
2. `get_accounts` → use Agentic `420763765` (`agentic_allowed=true`). Abort if false.
3. If markets closed, user said dry-run, **or** you are the Slack daily-check automation → **report only**, never `place_option_order`. Still do the full snapshot + classify + gate evaluation + report; dry-run is not a skip.

### 2. Snapshot

In parallel:

- `get_option_positions` (`nonzero=true`, account `420763765`)
- `get_equity_positions` (same account)
- `get_portfolio` (buying power)

For each short option: `get_option_instruments` (strike/type) + `get_option_quotes` (mark, delta, IV).

Coverage check: calls need ≥ `100 × contracts` shares of underlying.

Also compute from equities + shorts (see [docs/strategy.md](../../../docs/strategy.md)):

- **Idle CC capacity** per symbol: `floor(shares/100) − open short call contracts` (include SPY when held).
- **Index CSP sleeve:** open short puts on SPY/RSP/ITOT; free cash vs collateral; whether a new RSP/ITOT (preferred) or SPY put can open without breaching the ~$2k BP buffer.

### 3. Classify each short

Check earnings first (`get_earnings_results`):

- Earnings within **5 trading days** + short open → **earnings-flatten** (BTC close-only). No rewrite.
- Earnings **just printed** but refill not allowed yet (no full session since print, or no liquid ~0.20–0.30Δ / 30–45 DTE candidate) → class **waiting-refill** (no trade). Note on report.

Otherwise by Δ:

| Condition | Class | Default action |
|-----------|--------|----------------|
| \|Δ\| &lt; 0.12 | harvest | BTC + rewrite ~0.25Δ / 30–45 DTE; see harvest fallbacks below |
| 0.12 ≤ \|Δ\| ≤ 0.45 | hold | none |
| \|Δ\| &gt; 0.45 | defend | BTC → roll up+out ~0.25Δ, or BTC only if needed |

**Harvest fallbacks** (still actionable — do not leave dead shorts stranded):

1. If DTE **&lt; 10** and \|Δ\| &lt; 0.12 → close and rewrite only into **30–45 DTE** (not another &lt;10 DTE weekly).
2. If rewrite leg fails spread / review liquidity but **BTC leg PASSes** → downgrade to **harvest-close-only** (BTC only; rewrite later).

Use put Δ magnitude for CSPs. Prefer same chain; pick liquid strike near target Δ.

**New shorts** (same bands; propose on every check when eligible):

1. **Idle CC fill** — unused capacity on liquid holdings (and SPY if shares are in Agentic). Prefer names already in the overlay; phase large new sleeves. Skip if economic spread fails.
2. **Index CSP open** — only when free cash supports full collateral + ~$2k buffer. Prefer **RSP**, then **ITOT**, then **SPY** for *new* puts. If collateral is already tied up (e.g. existing SPY put), report blocked — do not stack.

### 4. Build orders

For each actionable class (earnings-flatten, harvest, harvest-close-only, defend, idle-CC-fill, index-CSP-open):

1. Resolve new `option_id` via chains → instruments → quotes (**skip** if close-only).
2. Close leg: buy + `position_effect=close`.
3. Open leg: sell + `position_effect=open` — **omit** for close-only paths.
4. Limit prices: fill-friendly sides (buy near high-fill buy / ask; sell near high-fill sell / bid).

### 5. Gate evaluation (always) / Tier C place (when allowed)

For each proposal:

1. Earnings / refill rules from [docs/strategy.md](../../../docs/strategy.md).
2. Evaluate rewrite and BTC legs separately when both exist. Apply the **economic spread rule** in [docs/strategy.md](../../../docs/strategy.md) (20% of mid **or** $0.15 abs **or** adverse fill ≤ 10% of expected roll credit / ≤ $0.25 close-only). If rewrite fails liquidity and BTC passes → **PASS close-only**, FAIL rewrite (do not FAIL the whole harvest into “do nothing”).
3. `review_option_order` on each leg you would place (even on dry-run / daily-check). Treat `OPTION_WIDE_BID_ASK_SPREAD` as advisory when the economic spread rule already PASSes; other hard alerts still block.
4. Mark PASS/FAIL with reasons. Never claim “would auto-place” unless every gate for that leg passed.

**Place only when** this run may trade (not dry-run / not daily-check automation; Slack continue/stop only after continue):

1. All gates pass for that leg → `place_option_order` with fresh `ref_id` UUID.
2. Close-only paths place **BTC only**.
3. Any fail → do not place that leg; escalate with reason.

Never place on non-Agentic accounts. Never skip review unless user explicitly says to bypass.

### 6. Report

Portfolio + overlay summary (optional `runbooks/YYYY-MM-DD.md`).

Slack daily-check: **two messages** per [docs/slack-automations.md](../../../docs/slack-automations.md) — (1) portfolio scoreboard, (2) overlay actions + CTA.

## Safety

- Real money. Prefer smaller first fills if unsure.
- Figures are not tax advice.
- Mask account numbers in user-facing prose (••••3765).
