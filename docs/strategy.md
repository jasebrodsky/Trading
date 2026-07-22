# Delta-band covered call strategy

## Account

- **Only:** Robinhood Agentic individual account `420763765` (display as ••••3765)
- Must be `agentic_allowed=true` and `option_level_2+`
- Do **not** trade the default individual or IRA from this playbook

## Goal

Steady premium on long stock via covered calls, keep shares when wanted, reset income/beta when short Δ dies. Use CC credits (and free cash) to accumulate a diversified index sleeve over time — buy shares and/or sell cash-secured puts on liquid index ETFs.

## Bands

| Zone | Short Δ | Action |
|------|---------|--------|
| Target entry | 0.20–0.30 | Sell new CC (or CSP) ~30–45 DTE |
| Harvest | &lt; 0.12 | Buy to close; rewrite down+out at target Δ when liquidity allows |
| Hold | 0.12–0.45 | No trade |
| Defend | &gt; 0.45 | Buy to close and/or roll up+out to keep shares |

Dwell: act if outside band for a full session, or Δ moved ≥0.10 from entry since last review.

### Harvest details

1. **Prefer** BTC + rewrite to ~0.20–0.30Δ, **30–45 DTE** (monthly liquidity).
2. **DTE floor:** if the short has **&lt; 10 DTE** and \|Δ\| &lt; 0.12 → **close** and step out to a new 30–45 DTE short (do not rewrite into another short-dated weekly unless defending).
3. **Close-only if rewrite fails liquidity:** if harvest applies but the **new** short fails spread / review liquidity gates → still **BTC only** when the close leg PASSes. Dead premium → cash; rewrite on a later check when markets are tighter. Same idea as earnings flatten: do not leave a dead short open just because the roll leg is ugly.

### Earnings — flatten then refill

Overrides the band table when a short is open on an underlying with **earnings within 5 trading days**:

1. **Flatten:** buy to close the short (close-only). Remove event exposure.
2. **Do not rewrite / do not sell a new short** until after that earnings print.
3. **Refill (tightened):** after the print, do **not** auto-sell on the first session back unless **both** are true:
   - at least **one full regular session** has closed since the earnings timestamp, **and**
   - a candidate short at ~0.20–0.30Δ, ~30–45 DTE has **spread PASS** (and review without blocking alerts).
   Until then: report “waiting refill” — no STO.

Close-only flatten still must pass spread / review / BP / coverage gates on the **BTC leg**. If the close leg fails those gates → escalate (do not force a bad fill).

## Structure rules

- Covered calls only on symbols with ≥100 shares per contract sold
- Single-leg only (MCP Level 2)
- Prefer monthly liquidity; avoid forced weeklies unless defending
- New shorts target **30–45 DTE**
- Put Δ uses **magnitude** (same band table as calls)

### Covered-call book

- On each check: inventory symbols with **unused CC capacity** (`floor(shares/100) − short call contracts > 0`).
- Prefer filling idle capacity on liquid names already held (and on **SPY** when shares are in Agentic).
- Same entry bands: ~0.20–0.30Δ, 30–45 DTE. Earnings flatten/refill rules apply per underlying.
- Do not chase thin names (wide tape / meme) just to “cover everything” — escalate or skip if economic spread fails.
- Phase new underlyings in (e.g. start 2–4 contracts on a large new sleeve like ONEQ) rather than max capacity on day one when liquidity is uncertain.

### Index sleeve (rebalance / accumulate)

**Purpose:** over time, grow diversified US equity ballast funded by CC premium and free cash.

**Long shares:** prefer buying **SPY**, **RSP**, or **ITOT** with free cash / CC credits when not fully deploying into CSPs. **SPY** long shares in Agentic are first-class CC underlyings (same bands).

**Cash-secured puts (index CSP sleeve):**

| Preference | Ticker | Role | Notes |
|------------|--------|------|--------|
| 1 (default for new CSPs) | **RSP** | S&P 500 equal-weight | Lower share price → more contracts per dollar of cash; weeklies available |
| 2 | **ITOT** | Total US market | Cheaper unit; fewer expirations — insist on spread PASS |
| 3 | **SPY** | S&P 500 cap-weight | Deepest liquidity; ~1 CSP per ~$70k+ cash — fine to **hold/roll** existing; prefer RSP/ITOT when *opening* more puts for sizing |
| Avoid for CSP sizing | VOO / IVV | Same S&P 500 | Almost as expensive as SPY; no sizing win |
| Not on RH | SPLG | Cheap S&P 500 | Unavailable here — do not plan around it |

**Sizing (cash account):**

- Collateral per put ≈ `strike × 100` (use the candidate strike, not last trade alone).
- Max new+existing index CSP contracts = `floor(free_cash_for_CSP / (strike × 100))` with a **~$2,000 BP buffer** left after open (do not pin BP to ~$0).
- **Free cash for CSP** = cash not already reserved by existing short puts / broker holds. If an open SPY (or other) put already consumes most cash, **do not** stack more CSPs — report “CSP blocked: collateral in use.”
- Manage open index CSPs under the same harvest / hold / defend bands as CCs.
- Assignment → own 100 shares → that name joins the CC book.

**CC income → index path:** when harvest/close frees premium or cash builds above CSP needs + buffer, prefer deploying into index **shares** (SPY/RSP/ITOT) or a new index CSP that still PASSes gates — do not let large idle cash sit uninvested without a stated reason on the report.

## Autonomy — Tier C

After `review_option_order`, **auto-place** when all gates pass. Escalate to human when any gate fails.

### Auto-place gates (all required)

1. Account is Agentic `420763765`
2. Action matches band table (harvest or defend), earnings flatten (close-only BTC), harvest close-only (rewrite liquidity failed / DTE floor close-only path), **or** a **new short** that fills idle CC capacity / opens or rolls an **index CSP** under the Index sleeve rules (coverage + free-cash sizing)
3. New short strike ≈ 0.20–0.30Δ when opening/rewriting — **omit open leg** for close-only (BP/shares block, earnings flatten, **or** harvest rewrite liquidity fail)
4. Net roll is credit **or** defend debit ≤ remaining extrinsic on the closed leg + $50 buffer — **N/A for close-only** (debit to flatten/harvest-close is allowed)
5. **Spread / liquidity (economic):** a leg **PASSes** if **any** of these is true (missing quotes still fail):
   - bid–ask spread ≤ **20% of mid**, or
   - spread ≤ **$0.15** absolute, or
   - estimated adverse fill (use half the spread, or ask−mid for buys / mid−bid for sells) ≤ **10% of expected net roll credit** when BTC+rewrite, or ≤ **$0.25** on **close-only** harvest/flatten legs
   Rationale: do not block a multi-hundred-dollar credit (or a cheap BTC that removes dead risk) over a couple cents of tape width. Still fail truly garbage / unquoted markets.
6. No pending assignment / exercise quantities on the position
7. `review_option_order` returns no blocking / hard-fail alerts user must acknowledge specially — **except** treat `OPTION_WIDE_BID_ASK_SPREAD` as advisory when the economic spread rule above already PASSes; other hard alerts still block
8. Regular market hours (or explicit dry-run)
9. Post-earnings **refill** also requires one full session since the print (see Earnings)

### Always escalate (do not auto-place)

- Buying power insufficient after review
- Quantity / share coverage mismatch
- Spread fails the **economic** liquidity rule above (or missing quotes) on legs you would place — if rewrite fails but BTC PASSes → close-only, do not escalate the whole harvest away
- Multi-leg needed
- Any uncertainty on covered vs naked
- Attempting to **sell / rewrite** when earnings are within 5 trading days, or refill before one full post-earnings session / without spread PASS

## Cadence

- **Daily** after open via Slack automation (noon ET) or on demand
- Weekend / closed: dry-run report only — no `place_option_order`
