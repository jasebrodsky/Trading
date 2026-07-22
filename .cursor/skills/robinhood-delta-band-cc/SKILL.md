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

### 3. Classify each short

| Condition | Class | Default action |
|-----------|--------|----------------|
| \|Δ\| &lt; 0.12 | harvest | BTC → sell new ~0.25Δ, 30–45 DTE, down+out |
| 0.12 ≤ \|Δ\| ≤ 0.45 | hold | none |
| \|Δ\| &gt; 0.45 | defend | BTC → roll up+out ~0.25Δ, or BTC only if user prefers shares free |

Use put Δ magnitude for CSPs. Prefer same chain; pick liquid strike near target Δ.

### 4. Build orders

For each non-hold:

1. Resolve new `option_id` via `get_option_chains` → `get_option_instruments` → `get_option_quotes`.
2. Close leg: buy + `position_effect=close`.
3. Open leg: sell + `position_effect=open` (omit if close-only).
4. Limit prices: use fill-friendly side of quote (buy near ask/high-fill buy; sell near bid/high-fill sell) — never mid-only hope on thin names.

### 5. Gate evaluation (always) / Tier C place (when allowed)

For each non-hold proposal:

1. Check earnings (`get_earnings_results`) — escalate if within 5 trading days.
2. Check spread, coverage, pending assignment, BP.
3. `review_option_order` with the same params you would place (even on dry-run / daily-check — report alerts, still no place if report-only).
4. Evaluate all [docs/strategy.md](../../../docs/strategy.md) auto-place gates. Mark PASS/FAIL with reasons. Never claim “would auto-place” unless every gate passed in this run.

**Place only when** this run is allowed to trade (not dry-run, not daily-check automation, and — if Slack continue/stop — user already said continue):

1. **If all gates pass** → `place_option_order` with a fresh `ref_id` UUID (Tier C standing auth).
2. **If any fail** → do not place; list reason and ask the user / escalate in-thread.

Never place on non-Agentic accounts. Never skip review unless user explicitly says to bypass.

### 6. Report

Write a short summary (and optionally `runbooks/YYYY-MM-DD.md`):

- Positions reviewed / held / harvested / defended
- Orders placed (id, symbol, credit/debit) — or “none (dry-run / daily-check)”
- Escalations / gate failures
- Open risk (nearest Δ to bands)

Slack daily-check: also ask for in-thread `continue` / `stop` (or ✅/❌) for the **separate** continue/stop automation.

## Safety

- Real money. Prefer smaller first fills if unsure.
- Figures are not tax advice.
- Mask account numbers in user-facing prose (••••3765).
