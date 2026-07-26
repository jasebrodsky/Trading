# Delta-Band Covered Call Strategy — Risk Analysis

**Account:** Agentic ••••3765  
**Analysis date:** 2026-07-26  
**Strategy:** Tier C delta-band covered calls + cash-secured puts  

---

## Executive Summary

Your understanding of the operational risk is **largely correct**, but there are nuances worth exploring. The strategy has shown strong performance in its initial phase with **100% harvest-only closes** and **zero defend rolls**, but this reflects a benign market environment. The real test comes during volatile or strong uptrend conditions.

### Key Risk Categories

1. **Operational/Execution Risk** (your primary concern) — MODERATE to HIGH
2. **Assignment Risk on Embedded Gains** — HIGH for NVDA, MU
3. **Opportunity Cost in Strong Bull Markets** — MODERATE to HIGH
4. **Earnings Event Risk** — MODERATE (mitigated by flatten rule)
5. **Liquidity Risk** — LOW to MODERATE (already escalated thin names)

---

## Current Strategy Performance

### YTD 2026 Performance (as of Jul 24)

| Metric | Value | Notes |
|--------|-------|-------|
| **Total Account Value** | $695,542 | Down -$11k from Jul 23 snapshot |
| **Net Premium (Credits − Debits)** | $8,885 YTD | Jun: $2,476 · Jul: $6,409 |
| **Realized Options P&L** | $3,227 YTD | All from harvest closes |
| **Open Credit** | $5,658 | Still holding |
| **Unrealized Equity** | +$130,001 | Full equity book vs avg cost |
| **Total Return YTD** | **−$7,803** | Equity losses exceeded option income |

### Roll Statistics — Pristine Harvest Record

| Metric | Value | Significance |
|--------|-------|--------------|
| **Total Closes** | 9 YTD | All executed via Tier C auto-place |
| **Harvest Rate** | 100% | Every close was a harvest (Δ < 0.12) |
| **Defend Rate** | **0%** | Never needed to defend yet |
| **Avg Credit Kept** | 78% (~$359/trade) | Strong premium capture |
| **Defend Debit Drag** | $0 | No defensive costs incurred |

**Interpretation:** This is a **best-case scenario** record. The strategy has operated in markets where:
- No name ran away hard enough to breach 0.45Δ
- All shorts decayed peacefully into harvest territory
- No forced rolls at unfavorable prices

This will not persist indefinitely.

---

## Market Condition Analysis

### 1. Harvest-Friendly Environment (Jun–Jul 2026) — **CURRENT**

**What happened:**
- Stocks ranged or drifted modestly
- Implied volatility was sufficient for decent premium
- Time decay worked in your favor
- All 9 YTD closes were harvest (Δ < 0.12)

**Specific Example — Jul 20 Harvest:**

| Symbol | Action | Credit In | BTC Cost | Net Kept | Keep % |
|--------|--------|-----------|----------|----------|--------|
| **NVDA** | Jul31 250c → Aug21 225c | $259 (orig) | $6 | $253 | 97.7% |
| **AMZN** | Jul31 285c → Aug21 280c | $385 (orig) | $141 | $244 | 63.4% |
| **SPY** | Jul31 680p → Aug21 715p | $492 (orig) | $36 | $456 | 92.7% |

**Net roll credit that day:** $953

**Risk assessment:** LOW operational risk. All gates passed cleanly. This is the strategy working as designed.

### 2. Defend Scenario — Not Yet Experienced, But Imminent Risk

**What would happen:**
You haven't hit this yet, but it's inevitable. A defend occurs when Δ > 0.45 — meaning the stock rallied hard and your short call is now threatening assignment.

**Hypothetical Example — NVDA Defend (if stock ran to $250):**

Current position:
- **Short:** Aug21 225c (currently Δ 0.23)
- **Credit received:** $259
- **Shares:** 142 @ $77.43 avg cost
- **Unrealized gain:** ~$25k (assuming $250 stock price)

If NVDA rallied to $250+ before Aug21:
- **Δ would spike** to >0.45 (in-the-money)
- **Action required:** BTC the 225c and roll to a higher strike further out
- **BTC cost estimate:** $25+ per share = **$2,500 debit**
- **You've only collected:** $259 premium
- **Net loss on the option:** −$2,241

**Your question: "If I defend at 45 delta, the cost is less than premium received (correct)?"**

**Answer:** **INCORRECT in most defend scenarios.** Here's why:

When Δ > 0.45, the option is typically **in the money** or very close. Your original credit was collected when the strike was **out of the money** at low Δ (~0.15 for Conviction names). 

**Math on a defend:**
- Original credit: $259 (NVDA example)
- BTC at 0.45Δ when ITM: Could be $10–25+ depending on extrinsic
- **You will often pay MORE to close than you received** if the stock ran hard

**What saves you:**
1. **The stock appreciated** — your shares gained value, offsetting the option loss
2. **You avoid assignment** — preserving LTCG status on NVDA ($77 → $250 would trigger $25k taxable event)

### 3. Strong Bull Market — Opportunity Cost Risk

**What would happen:**
If stocks in your portfolio rally 20-30% over a few months, your covered calls cap your upside.

**Real Example from Your Portfolio — NVDA:**

| Metric | Value |
|--------|-------|
| **Shares held** | 142 |
| **Avg cost** | $77.43 |
| **Current price (Jul 24)** | ~$220 (implied from Δ data) |
| **Unrealized gain** | ~$20k+ |
| **Short call** | Aug21 225c |

**Scenario:** NVDA rallies to $280 by August (possible given AI hype)

Without CC:
- Gain on shares: 142 × ($280 − $77) = **$28,826**

With CC at 225 strike:
- Gain on shares: 142 × ($225 − $77) = **$21,016**
- Option P&L: $259 credit − cost to close/roll
- **Capped upside:** Lost $7,810 in gains + cost to defend

**Mitigation:** Your Conviction sleeve uses 0.12–0.18Δ entry, giving more room to run than Income sleeve (0.20–0.30Δ). This is the correct design, but you still cap gains.

### 4. Sharp Correction / Volatility Spike

**What would happen:**
Stocks drop 10-20% quickly. Your short calls become deeply OTM and worthless — great for closing. But your equity falls.

**Real Example — Equity Losses Jul 23-24:**

| Date | Account Value |
|------|---------------|
| Jul 23 | $706,572 |
| Jul 24 | $695,542 |
| **Change** | **−$11,030 (−1.6%)** |

Meanwhile, your options are profitable (open shorts now worth less). But the equity loss swamps the option gain in a single-day correction.

**Risk assessment:** Your strategy provides **income, not principal protection**. The premium is compensation for capping upside, not insurance against drawdowns.

### 5. Earnings Whipsaws

You have a **strong earnings-flatten rule** (no shorts within 5 trading days). This has prevented disasters, but note the **waiting-refill** limbo period.

**Recent Example — INTC (from Jul 24 runbook):**

| Event | Date | Status |
|-------|------|--------|
| **Earnings** | Jul 23 PM | Printed |
| **Jul 24 check** | Jul 24 | Waiting refill — no new short yet |
| **Reason** | Need 1 full session + liquid candidate | Blocked from income |

**Risk:** You miss premium income during blackout windows. With 4-5 names often in earnings proximity, this can be 20-40% of potential capacity offline.

---

## Your Risk Assessment — Annotated

> "I currently see the risk as operational risk, human risk of not executing for some reason and delta goes too high and it costs more to close option."

**Assessment:** ✅ **CORRECT.** This is your #1 risk. Examples:

### Operational Risk Scenarios (Historical Evidence)

#### A. Missed Check / Delayed Execution

**Jul 22 Harvest Escalations:**

| Symbol | Δ | Issue | Outcome |
|--------|---|-------|---------|
| **MU** | 0.042 | Broker flagged wide spread on rewrite | Escalated — not closed |
| **MRNA** | 0.058 | Wide spread (mid $0.25, spread $0.30) | Escalated — not closed |
| **AAL** | 0.044 | Earnings next day | Escalated — not closed |
| **TSLA** | 0.091 | Earnings same day | Escalated — not closed |

**What happened next:**
- MU short remained open with 0.042Δ (nearly worthless, but not closed)
- By Jul 24, it was finally replaced with a new Aug28 1300c
- **Cost of delay:** Minimal in this case, but the short remained as dead risk

**Worst-case:** If MU had spiked on earnings or news before the close, Δ could have jumped to >0.45, forcing a defend. The longer a dead short sits, the more event risk you carry.

#### B. Earnings Surprise / News-Driven Spike

**Hypothetical (didn't happen yet, but structurally possible):**

You hold NVDA Aug21 225c (Δ 0.23). Suppose NVDA announces a major AI chip deal after hours:
- Stock gaps up 15% overnight to $250+
- Your 225c is now deep ITM, Δ > 0.80
- **You're past the defend threshold** — you're in assignment danger
- BTC cost: $25+ per share ($2,500 debit)
- You collected $259 originally
- **Net option loss:** −$2,241

**Saving grace:**
- Your 142 shares gained 15% × $220 = $33/share = $4,686
- **Net position:** +$2,445 (share gain minus option loss)
- **But:** If you didn't execute the defend quickly, you could be assigned at $225, realizing $20k+ LTCG tax event

**This is the operational risk you're worried about.** Tier C helps, but:
- Slack automations could miss a notification
- Market closed over weekend (can't defend)
- User (you) could be unavailable to approve an exception

---

> "If I defend more often, I'm getting out at 45 delta so the cost is less than the premium already received (correct)?"

**Assessment:** ❌ **INCORRECT in most cases.** Let's break down the math.

### Defend Math — Why Your Assumption Is Wrong

**What you're thinking:**
- I sold a call for $259 (NVDA example)
- If Δ hits 0.45, I buy it back
- At 0.45Δ, it's still OTM or barely ITM, so it should cost less than $259

**What actually happens:**

Delta is a **probability** metric, not a price ceiling. A 0.45Δ option can have substantial **extrinsic value** if there's time and volatility left.

**Example Calculation — NVDA 225c Defend at 0.45Δ:**

Assume:
- Stock: $220 (at entry) → $230 (when Δ hits 0.45)
- Strike: $225
- DTE remaining: 20 days
- IV: 30%

At 0.45Δ with stock at $230:
- **Intrinsic value:** $230 − $225 = **$5** ($500 per contract)
- **Extrinsic value:** ~$3-5 depending on IV and DTE
- **Total option price:** ~$8-10 per share = **$800-1,000**

You received $259 originally.  
**BTC cost:** $800  
**Loss on option:** −$541

**But your shares gained:**
- 142 shares × ($230 − $220) = **+$1,420**

**Net position:** +$879 (share gain minus option loss)

### The Critical Insight

**Your statement "the cost is less than premium received" is wrong for the option in isolation.**

**But you're directionally correct that defending isn't catastrophic** because:
1. The stock **must** appreciate for Δ to spike
2. Your share gains offset the option loss
3. You avoid assignment (critical for NVDA/MU embedded LTCGs)

**However, the cost to defend CAN exceed the original credit.** You're not getting "free money" on a defend — you're paying to keep the position alive.

---

> "The position must appreciate which compensates for the loss which shouldn't be anyways?"

**Assessment:** ✅ **CORRECT.** This is the key realization.

For Δ to spike above 0.45, the stock **must** have rallied significantly. Your shares gained value, offsetting (and usually exceeding) the option loss.

**But note the phrase "which shouldn't be anyways."** I interpret this as: "the option loss shouldn't be a loss because I'm doing this to defend my embedded gain."

**Correct for NVDA/MU.** Those names have huge unrealized LTCGs:
- **NVDA:** $77 cost → ~$220 = $143/share gain × 142 shares = **~$20k LTCG** if assigned
- **MU:** $130 cost → ~$980 = $850/share gain × 100 shares = **~$85k LTCG** if assigned

Paying $2,000 to defend and avoid a $20k+ tax event is **good risk management.**

**Less clear for Income sleeve names** (TSLA, AAL, PFE, etc.) where assignment is acceptable. For those, a defend is optional — you could let assignment happen and keep the full credit.

---

## Risk Scenarios — Detailed Walkthroughs

### Scenario 1: NVDA Assignment (Operational Failure)

**Setup:**
- Current: 142 shares @ $77.43, short Aug21 225c (Δ 0.23), credit $259
- Stock rallies to $230 before expiration

**Timeline:**

| Event | Δ | Action Needed | What Happens If Missed |
|-------|---|---------------|------------------------|
| **Jul 26** | 0.23 | None (hold zone) | N/A |
| **Aug 1** | 0.38 | Watch, prepare to defend | Miss = enter defend zone unprepared |
| **Aug 10** | 0.48 | **DEFEND NOW** — BTC + roll | Miss = assignment risk at expiration |
| **Aug 15** | 0.72 | Too late, deep ITM | BTC cost ~$8-12/share ($1,200+) |
| **Aug 21** | Expiry | Assigned at $225 | **Forced sale:** 142 shares @ $225 |

**Outcome if assigned:**
- Proceeds: 142 × $225 = $31,950
- Cost basis: 142 × $77.43 = $10,995
- **LTCG realized:** $20,955
- **Tax due (20% fed + 3.8% NIIT + state):** ~$6,000-7,000
- Premium kept: $259
- **Net after-tax:** $31,950 + $259 − $6,500 = **$25,709** (~73 cents on the dollar of gross gain)

**If defended on Aug 10:**
- BTC at 0.48Δ: ~$600-800 debit
- Roll to Sep 240c at 0.20Δ: ~$400-500 credit
- **Net roll cost:** ~$200-300
- Keep shares, defer tax, collect new premium cycle

**Verdict:** Defending is worth it for NVDA. Operational failure (missing the defend window) costs ~$6k in taxes.

---

### Scenario 2: TSLA Assignment (Income Sleeve — Should You Defend?)

**Setup:**
- Current: 109 shares @ $335.98, short Aug28 345c (Δ 0.29), credit $695
- Stock rallies to $355

**Timeline:**

| Event | Δ | Action |
|-------|---|--------|
| **Aug 10** | 0.52 | Defend threshold breached |

**Decision tree:**

**Option A: Defend (keep shares)**
- BTC at 0.52Δ: ~$1,200 debit (stock now $355, strike $345, $10 ITM + extrinsic)
- Roll to Sep 370c at 0.25Δ: ~$800 credit
- **Net cost:** −$400
- Keep shares, collect new premium

**Option B: Let assignment happen**
- Assigned at $345: 109 shares × $345 = $37,605
- Cost basis: 109 × $335.98 = $36,622
- **Gain:** $983 (short-term)
- Premium kept: $695
- **Total income:** $1,678
- Tax: ~$450 (short-term rate on $983)
- **After-tax net:** $1,228

**Option C: Defend but assignment is fine**
- Don't defend
- Take assignment
- Use proceeds to open new CSP on TSLA or buy back shares if desired

**Verdict:** For TSLA (Income sleeve, no embedded LTCG issue), **assignment is acceptable.** Defending costs $400 to keep a $1,000 gain alive. Unless you strongly believe TSLA continues higher, assignment is the clean exit.

**Your strategy doc says:** "Income sleeve — assignment acceptable." This is correctly designed.

---

### Scenario 3: Earnings Whipsaw — PFE Flatten Failure

**Setup:**
- Current: 765 shares @ $48.17, short Aug28 26c ×3 (Δ 0.23), credit $69
- Earnings: Aug 4 AM (7 trading days out as of Jul 26)

**Strategy rule:** Flatten if earnings ≤5 trading days.

**Timeline:**

| Date | Trading Days to Earnings | Action |
|------|--------------------------|--------|
| **Jul 29** | 4 days | **FLATTEN** — BTC close-only |
| **Aug 4** | Earnings print | Wait for dust to settle |
| **Aug 5** | +1 session | Refill: sell new 26c or 27c at 0.25Δ |

**What if you miss the flatten?**

Suppose PFE reports terrible earnings, stock gaps down 15%:
- Stock: $26 → $22
- Your 26c: Now deeply OTM, worthless
- **Outcome:** Great! Option expires worthless, keep full $69 × 3 = $207
- **But:** Your 765 shares lost 15% × $26 = $3.90/share × 765 = **−$2,984**

**Alternatively:** PFE beats, stock gaps up 10%:
- Stock: $26 → $28.60
- Your 26c: Now ITM, Δ > 0.80
- **Outcome:** Assignment risk on all 3 contracts
- You'd be forced to sell 300 shares at $26 (below current $28.60 market)
- Lost upside: 300 × ($28.60 − $26) = **$780**

**Verdict:** The earnings flatten rule **limits risk** of both scenarios. You pay a small debit to close (~$30-50 per contract if still OTM), but you remove event risk.

**Operational risk:** Missing the flatten deadline (Jul 29) means you're exposed to a gap.

---

## Risk Mitigation — Current vs. Recommended

### What's Working Well ✅

1. **Tier C auto-place within gates** — Eliminates human delay on liquid, clean trades
2. **Earnings flatten rule** — Prevents catastrophic gaps (0 earnings-driven assigns so far)
3. **Conviction vs. Income sleeves** — Appropriate Δ targeting preserves upside on LTCG names
4. **Economic spread rule** — Avoids bad fills; escalates thin names (DAL, ONEQ, MU alts)
5. **Daily checks via Slack** — Consistent monitoring cadence

### Gaps and Recommendations ⚠️

#### 1. Weekend / After-Hours Gap Risk

**Issue:** Markets close Fri 4 PM ET, reopen Mon 9:30 AM ET. News can break over the weekend.

**Example:** NVDA announces chip deal Saturday. Stock gaps up 15% Monday open. Your 225c is now deep ITM before you can act.

**Current mitigation:** None (Tier C only operates during market hours)

**Recommendations:**
- **A. Tighter Δ monitoring:** If a short approaches 0.40Δ on Friday close, consider preemptive defend (don't wait for 0.45)
- **B. Reduce size before known catalysts:** If NVDA has an AI conference Monday, close/roll Friday
- **C. Accept the risk:** Your shares gain value on good news; option loss is offset

#### 2. Illiquid Name Escalations Pile Up

**Issue:** DAL, ONEQ, MU (on some strikes) repeatedly fail spread gates. Dead shorts sit unhedged.

**Current mitigation:** Escalate to human, wait for tighter spreads

**Recommendations:**
- **A. Wider spread tolerance for closes:** If Δ < 0.05 (nearly worthless), pay the spread to remove risk
  - Example: MU 0.042Δ, mid $0.80, spread $1.45 (95% of mid)
  - Even at ask ($2.25), you close for $225. Small cost to remove tail risk.
- **B. Set a "close-by-Friday" rule:** If harvest fails Mon-Thu, force close Friday (avoid weekend gap)
- **C. Skip illiquid names for future CC:** Don't write DAL/ONEQ CC if spreads are persistently wide

#### 3. Defend Costs Can Exceed Credit

**Issue:** You assumed defending at 0.45Δ costs less than original credit. This is often false.

**Current mitigation:** None (strategy doc doesn't address defend debit tolerance)

**Recommendations:**
- **A. Set a defend budget:** "Willing to pay up to 1.5× original credit to keep Conviction names"
  - Example: NVDA $259 credit → willing to pay $400 to defend
- **B. Two-tier defend:** 
  - **Conviction (NVDA, MU):** Defend at any cost (LTCG preservation)
  - **Income (TSLA, AAL):** Defend only if cost < 0.5× original credit; otherwise accept assignment
- **C. Track defend P&L separately:** Report "defense drag" as a cost of maintaining the portfolio

#### 4. Idle Capacity Drag

**Issue:** 49 idle CC contracts (as of Jul 24) represent ~$9,800 in foregone income.

**Current mitigation:** Agent fills all passing gates; escalates failing ones

**Recommendations:**
- **A. Relax spread rule for first-fill:** On names like ONEQ with 11 idle contracts, accept 25% spread (vs. 20%) to get some coverage
- **B. Prioritize liquid names:** Fill TSLA, NVDA, MU first; defer ONEQ, DAL if spreads are bad
- **C. Index CSP as fallback:** If idle CC won't fill, open another RSP/ITOT CSP instead

#### 5. Accumulation CSP Collateral Blockage

**Issue:** META CSP needs ~$60k collateral, but AMD CSP is already consuming ~$46k. Can't stack both.

**Current mitigation:** "One accumulation CSP at a time"

**Recommendations:**
- **A. Close AMD CSP early if META earnings clear:** Harvest AMD put (currently 0.26Δ, hold zone), free up cash for META
- **B. Tier accumulation targets:** AMD → 100 shares is closer (need 55 more). Prioritize AMD until graduation, then META.
- **C. Use SPY CSP closure to fund accumulation:** When SPY Aug21 715p closes (frees $71.5k), immediately rotate to META CSP

---

## What-If Scenarios: Stress Testing

### Stress Test 1: Market Correction (−15% in 2 weeks)

**Setup:** Broad market drops 15% (e.g., Fed shock, geopolitical event)

**Portfolio Impact:**

| Asset Class | Current Value | After −15% | Change |
|-------------|---------------|------------|--------|
| **Equities** | $548,361 | $466,107 | **−$82,254** |
| **Short Calls** | −$6,016 (liability) | −$500 (nearly worthless) | **+$5,516** (gain) |
| **Cash** | $153,197 | $153,197 | $0 |
| **Total** | $695,542 | $619,804 | **−$75,738 (−10.9%)** |

**Analysis:**
- Your short calls decay to near-zero (all OTM) — **big win**
- But equity losses swamp the option gains
- **Net loss: −10.9%** (better than −15% unhedged, but not "protected")

**Option actions:**
- Close all shorts for near-zero (harvest bonanza)
- Rewrite new shorts at higher strikes (stocks now lower)
- Collect fresh premium on depressed prices

**Risk:** If you **don't close fast enough**, stocks could bounce, and you miss the opportunity to lock gains on the shorts.

---

### Stress Test 2: Melt-Up Rally (+25% in 3 months)

**Setup:** Strong bull market, stocks rally 25% (e.g., AI boom, rate cuts)

**Portfolio Impact:**

| Asset Class | Current Value | After +25% | Change |
|-------------|---------------|------------|--------|
| **Equities (uncapped)** | $548,361 | $685,451 | **+$137,090** |
| **Equities (with CC cap)** | $548,361 | ~$620,000 (capped at strikes) | **+$71,639** (limited) |
| **Short Calls** | −$6,016 (liability) | −$30,000+ (deep ITM) | **−$24,000** (loss) |
| **Cash** | $153,197 | $153,197 | $0 |
| **Total (CC capped)** | $695,542 | $773,197 | **+$77,655 (+11.2%)** |
| **Total (no CC)** | $695,542 | $838,648 | **+$143,106 (+20.6%)** |

**Opportunity cost:** **$65,451** foregone gains (9.4% of portfolio)

**Analysis:**
- Your CC strategy **caps upside** at strike prices
- You'd gain 11.2% instead of 20.6%
- **Premium collected** (~$10-15k over 3 months) partially offsets
- **Net opportunity cost:** ~$50-60k

**This is the price of the strategy.** You trade upside for income.

---

### Stress Test 3: NVDA Moonshot (+40% in 1 month)

**Setup:** NVDA announces transformative AI breakthrough, stock runs from $220 → $308

**Position Impact:**

| Metric | Value |
|--------|-------|
| **Shares:** | 142 @ $77.43 |
| **Short:** | Aug21 225c (credit $259) |
| **Stock move:** | $220 → $308 (+$88/share) |

**Outcome:**

**Scenario A: You defend successfully**
- Aug 5: Stock $250, Δ 0.48 → BTC for $2,800, roll to Sep 260c for $1,200 credit → net cost $1,600
- Aug 15: Stock $280, Δ 0.50 → BTC for $3,500, roll to Oct 300c for $1,800 credit → net cost $1,700
- Aug 25: Stock $308, short Oct 300c at 0.35Δ → holding
- **Total defense costs:** $3,300
- **Original credit:** $259
- **Net option loss:** −$3,041
- **Share gain:** 142 × ($308 − $220) = **+$12,496**
- **Net position:** +$9,455

**Scenario B: You miss the defend, assigned at $225**
- Assigned: 142 shares @ $225 = $31,950
- Cost basis: $10,995
- **LTCG:** $20,955
- **Tax:** $6,500 (estimate)
- **After-tax proceeds:** $25,450
- **If you rebuy at $308:** 142 shares × $308 = $43,736
- **Net cash needed:** $43,736 − $25,450 = **$18,286**
- **Effective loss:** $18,286 vs. the $9,455 defend scenario = **$8,831 worse**

**Verdict:** Defending is critical for NVDA. Missing the defend costs ~$9k in this scenario.

---

## Recommendations — Action Items

### Immediate (Next 7 Days)

1. **Review defend thresholds for Conviction names**
   - NVDA: Set a "watch closely" alert at 0.35Δ (before 0.45 defend)
   - MU: Same
   - Consider preemptive defend if Δ > 0.40 on Friday close (weekend gap protection)

2. **Close dead harvests (Δ < 0.05) at any spread**
   - Don't let near-worthless shorts sit unhedged
   - Pay the spread to remove tail risk

3. **Fill SNAP CC capacity (6 contracts idle)**
   - Stock: 600 shares, $0 coverage
   - Should be easy to write 0.25Δ calls, collect ~$100-200/contract
   - Low-hanging fruit for income

4. **Prioritize AMD CSP graduation**
   - 45 shares → need 55 more to reach 100 (Conviction CC)
   - Current CSP: Aug28 460p, 0.26Δ
   - If assigned, immediately write Aug expiry CC at 0.15Δ

### Short-Term (Next 30 Days)

5. **Stress-test your Slack automation**
   - Simulate a missed daily check (skip one day)
   - Verify continue/stop logic works if you're unavailable
   - Consider adding a "backup check" (evening sweep at 7 PM ET)

6. **Document defend budget per sleeve**
   - Conviction: "Defend at any cost up to 2× original credit"
   - Income: "Defend only if cost < 0.5× original credit"
   - Update strategy.md with these thresholds

7. **Earnings calendar ahead**
   - NVDA: Aug 26 (24 days out) — current short expires Aug 21 (safe)
   - AMD: Aug 4 (7 days) — CSP open, watch for flatten trigger Jul 30
   - PFE: Aug 4 (7 days) — CC open, flatten by Jul 30

8. **Index CSP closure → accumulation rotation**
   - SPY 715p closes Aug 21 → frees $71.5k
   - Immediately open META 0.22Δ CSP if earnings clear (Jul 29 print)

### Long-Term (Next 90 Days)

9. **Track defend P&L separately**
   - Add a "defendDebitDragMtd" field to snapshot.json
   - Report it alongside harvestPct
   - Goal: Keep defend drag < 20% of gross premium

10. **Liquidity review: Consider dropping thin names**
    - If ONEQ continues to fail spread gates, sell shares
    - Redeploy capital into liquid index ETFs (SPY, RSP)
    - Trade-off: Lower potential alpha, but higher strategy execution rate

11. **Accumulation graduation path**
    - AMD: Target Sept for 100-share graduation
    - META: Target Oct-Nov (post-earnings, if CSP can open)
    - Once graduated, shift to Conviction CC sleeve (0.15Δ)

12. **Annual review: Defend frequency vs. cap drag**
    - If you defend >5 times in a year, consider raising entry Δ (e.g., Conviction 0.18-0.25Δ)
    - Trade-off: More premium, less upside, fewer defends
    - Or: Accept defend costs as "cost of keeping shares"

---

## Final Verdict: Your Risk Understanding

### What You Got Right ✅

1. **Operational risk is your #1 threat** — Missing a defend window can cost thousands
2. **Defending preserves tax efficiency** — Critical for NVDA/MU embedded gains
3. **Share appreciation offsets option losses** — Defending isn't "losing money" in isolation

### What You Got Wrong ❌

1. **"Defend costs less than premium received"** — False. Defend can cost 2-5× original credit.
2. **Implied safety of 0.45Δ threshold** — By the time you hit 0.45, you're often deep ITM and expensive to close.

### What You Didn't Consider 🤔

1. **Opportunity cost in bull markets** — You'll underperform buy-and-hold by ~40-60% of upside
2. **Idle capacity drag** — 49 idle contracts = $10k/month foregone income
3. **Liquidity risk on thin names** — DAL, ONEQ, MU alts repeatedly fail gates
4. **Weekend gap risk** — No defense mechanism for after-hours news

---

## Bottom Line

Your strategy is **sound and well-designed**, but you're in a **honeymoon phase**:
- 100% harvest, 0% defend (won't last)
- Benign market (no big spikes yet)
- Strong execution (Tier C + Slack automation working)

**When the first defend hits, you'll learn:**
- Defending costs real money (often > original credit)
- But it's worth it for Conviction names (tax deferral + upside preservation)
- And it's optional for Income names (assignment is fine)

**Prepare now:**
- Set defend budgets
- Add "watch" alerts at 0.35Δ
- Close dead harvests fast (don't let them linger)
- Fill idle capacity on liquid names

**You'll be fine.** Just don't assume defending is "cheap." It's the **insurance premium** you pay to keep the strategy alive.

---

**End of Risk Analysis**  
**Next action:** Review this doc, update strategy.md with defend budgets, run a stress test on NVDA defend scenario.
