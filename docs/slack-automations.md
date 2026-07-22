# Slack automations — Agentic delta-band

Two separate Cursor Automations. Do **not** merge them into one prompt.

| Automation | Role | Places orders? |
|------------|------|----------------|
| **Agentic delta-band daily check** | Snapshot, classify, propose, gate-evaluate, post report | **Never** |
| **Agentic delta-band continue/stop** | Read thread + user continue/stop → place or skip | Only on **EXECUTE** |

Wire triggers so they do not collide:

- **Daily check:** schedule and/or keyword filter for starting a cycle (e.g. top-level messages matching `delta band` / `covered-call` that are **not** only `continue`/`stop`).
- **Continue/stop:** Slack **thread replies** and/or emoji reactions (`white_check_mark`, `x`) on the daily-check bot message — **not** top-level `@Cursor Dry-run…` kickoffs.

If a message looks like a new check (`Dry-run…`, `Run covered-call…`, “snapshot”, “classify”), it belongs to **daily check**. The continue/stop agent must **not** treat it as approval intent.

---

## Prompt — Agentic delta-band daily check

Copy into the daily-check automation:

```text
Open the jasebrodsky/Trading repo on branch main. Follow docs/strategy.md and the robinhood-delta-band-cc skill. Trade scope: Robinhood Agentic account only (display as ••••3765); abort if not agentic_allowed.

This automation is REPORT-ONLY. You are not the continue/stop approval gate.
- Do NOT invent EXECUTE/SKIP.
- Do NOT wait for continue / white_check_mark before snapshotting.
- Do NOT call place_option_order under any circumstance in this automation.
- If someone @Cursor's a dry-run or "run covered-call delta band check", that is permission to run THIS report now.

Run the covered-call / CSP delta-band check:
1. Snapshot option positions (nonzero), equity positions, and buying power for Agentic 420763765.
2. For each short: instruments + quotes (mark, delta, IV). Classify harvest (|Δ| < 0.12), hold (0.12–0.45), or defend (|Δ| > 0.45). Put Δ = magnitude.
3. Coverage: calls need ≥100 shares × contracts; flag mismatches.
4. For each non-hold: build a BTC + rewrite plan (target ~0.20–0.30Δ, ~30–45 DTE, prefer monthly liquidity). Use fill-friendly limit sides (buy near high-fill buy / ask; sell near high-fill sell / bid).
5. Evaluate auto-place gates from docs/strategy.md for each proposal — including:
   - get_earnings_results (escalate if earnings within 5 trading days)
   - bid–ask ≤15% of mid (or ≤$0.10 absolute for cheap options)
   - review_option_order on each proposed leg (report alerts; still do not place)
   - BP / coverage / pending assignment
   Mark each proposal gate PASS or FAIL with reasons. Do not claim "would auto-place" unless every gate actually passed in this run.

If markets are closed, still produce the full report (quotes may be last session); label it dry-run / closed.

Post a clear status summary to Slack channel #all-agentic-trading:
- Positions reviewed / held / proposed harvest / proposed defend
- Proposed rolls with expected credit/debit and gate pass/fail reasons
- Escalations (earnings, wide spreads, BP, coverage, review alerts)
- Open risk (nearest Δ to bands)

End the Slack message by asking the user to reply in-thread with continue or stop (or react white_check_mark / X). Remind them that the separate continue/stop automation will place only after continue — this daily-check run never places.
```

---

## Prompt — Agentic delta-band continue/stop

Copy into the continue/stop automation:

```text
You are ONLY the approval gate for the Agentic delta-band overlay. Repo: jasebrodsky/Trading on branch main. Follow docs/strategy.md and robinhood-delta-band-cc. Account: Robinhood Agentic only (••••3765). Abort if not agentic_allowed.

Scope filter (do this first):
- If the triggering message is starting a new check (contains Dry-run, "Run covered-call", "delta band check", "snapshot", or is a top-level @Cursor kickoff that is not clearly continue/stop), do NOT run EXECUTE/SKIP. Reply once in-thread: "Wrong automation for a new check — use Agentic delta-band daily check (or wait for the scheduled report). I only handle continue/stop on an existing daily summary." Then exit without placing orders.
- Otherwise read the triggering Slack message and its parent thread (the daily status summary).

Decide intent from the user message / reaction only:
- continue / yes / approve / white_check_mark → EXECUTE
- stop / no / cancel / x → SKIP
- Anything else → ask once for clarification in-thread; do not place orders.

SKIP path:
- Reply in the Slack thread confirming no orders this cycle.
- Exit.

EXECUTE path:
- Re-fetch live option quotes, deltas, coverage, and buying power.
- Only act on harvest/defend proposals from the parent thread that still match the band table.
- For each order: review_option_order, then place_option_order ONLY if ALL docs/strategy.md auto-place gates pass (including earnings within 5 trading days → escalate, and blocking review alerts → escalate).
- Never place on gate failure; escalate in-thread with the reason.
- Never trade non-Agentic accounts. Never skip review.
- Post a fill/skip summary back to the same Slack thread (order ids, credits/debits, escalations).

If markets are closed: do not place; say so in-thread.
```
