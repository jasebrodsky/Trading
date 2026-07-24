# Strategy canvas — visual map

Visual companion to [strategy.md](strategy.md). Open in Cursor, GitHub, or any Mermaid renderer.

---

## 1. System stack (who does what)

```mermaid
flowchart TB
  subgraph Human
    U[You — Slack continue / stop]
    W[Manual bank withdraw on 15th]
  end

  subgraph Automation
    S[Slack daily check — report only]
    C[Slack continue/stop — place orders]
  end

  subgraph Agent
    A[Cursor agent + robinhood-delta-band-cc skill]
    R[Git playbook — strategy.md]
  end

  subgraph Broker
    M[Robinhood MCP]
    RH[Agentic account ••••3765]
  end

  S --> A
  C --> A
  A --> R
  A --> M
  M --> RH
  U --> C
  W --> RH
```

---

## 2. Portfolio sleeves (what you own vs what you sell)

```mermaid
flowchart LR
  subgraph Holdings
    EQ[Long stocks & ETFs]
  end

  subgraph Conviction["Conviction CC · Δ 0.12–0.18"]
    C1[NVDA AMZN ONEQ SPY MU]
  end

  subgraph Income["Income CC · Δ 0.20–0.30"]
    I1[TSLA DAL AAL MRNA …]
  end

  subgraph Accum["Accumulation CSP · Δ 0.20–0.25"]
    A1[AMD META · under 100 sh]
  end

  subgraph Index["Index · ballast"]
    X1[RSP ITOT SPY shares or CSP]
  end

  EQ --> C1
  EQ --> I1
  A1 -->|assigned ≥100 sh| C1
  X1 -->|assigned or buy| C1
  X1 --> Income
```

| Sleeve | Option | Goal |
|--------|--------|------|
| Conviction | Short **call** | Keep shares · low assignment risk |
| Income | Short **call** | Max premium · assignment OK |
| Accumulation | Short **put** | Buy shares cheaper · wheel into conviction |
| Index | **Put** or **shares** | Diversify · grow CC book |

---

## 3. Delta bands (every open short)

```mermaid
stateDiagram-v2
  [*] --> Hold: STO 30–45 DTE at sleeve entry Δ

  Hold --> Harvest: |Δ| < 0.12
  Hold --> Defend: |Δ| > 0.45

  Harvest --> Hold: BTC + rewrite at entry Δ
  Harvest --> CloseOnly: rewrite fails spread gate
  CloseOnly --> Hold: rewrite later when liquid

  Defend --> Hold: roll up/out · keep shares

  Hold --> Flatten: earnings ≤ 5 days
  Flatten --> WaitRefill: after print
  WaitRefill --> Hold: +1 session + spread PASS

  note right of Harvest
    DTE < 10 + harvest
    → close only into 30–45 DTE
  end note
```

**ATM ≈ Δ 0.50** · **Δ → 1 = deep ITM** (not “at strike”).

| Zone | |Δ| | Action |
|------|-----|--------|
| Harvest | < 0.12 | Buy to close · rewrite |
| Hold | 0.12 – 0.45 | Collect theta |
| Defend | > 0.45 | Roll to keep shares |

---

## 4. Daily cycle (automation)

```mermaid
sequenceDiagram
  participant Clock as 12:00 ET
  participant Agent
  participant MCP as Robinhood MCP
  participant Slack
  participant You

  Clock->>Agent: Daily check
  Agent->>MCP: portfolio · positions · quotes · earnings
  Agent->>Agent: classify · gates · deploy focus
  Agent->>Slack: Message 1 — scoreboard
  Agent->>Slack: Message 2 — action board + deploy focus
  You->>Slack: continue or stop
  alt continue
    Agent->>MCP: re-quote · review · place
    Agent->>Slack: order results
  else stop
    Agent->>Slack: no orders
  end
```

---

## 5. Deployment focus (where new premium goes)

```mermaid
flowchart TD
  START[Daily check metrics] --> CALC["idle_cc_total · put_collateral · deployable_cash"]

  CALC --> Q1{idle_cc ≥ 5?}
  Q1 -->|yes| FS[FILL-SLOTS month<br/>Prioritize idle CC writes]
  Q1 -->|no| Q2{idle_cc = 0<br/>and cash for index?}
  Q2 -->|yes| IX[INDEX month<br/>RSP/ITOT/SPY shares or CSP]
  Q2 -->|no| Q3{1–4 idle<br/>and index/accum slot?}
  Q3 -->|yes| MX[MIXED<br/>CC fills first · then one CSP]
  Q3 -->|no| BL[DEPLOY BLOCKED<br/>Hold cash · report why]

  FS --> G[Tier C gates + continue]
  IX --> G
  MX --> G
  BL --> G
```

**Priority when scaling income:** fill idle CCs → then index/accumulation with spare cash.

---

## 6. Wheel loops (CSP → shares → CC)

```mermaid
flowchart LR
  subgraph AccumWheel["Accumulation wheel · AMD META"]
    AP[Sell CSP ~0.22Δ] -->|assigned| AS[≥100 shares]
    AS --> AC[Conviction CC ~0.15Δ]
    AC --> AP2[Harvest / defend / hold]
  end

  subgraph IndexWheel["Index wheel · RSP ITOT SPY"]
    IP[Sell index CSP] -->|assigned| IS[100 sh ETF]
    IS --> IC[CC on ETF]
    IC --> IP
  end

  subgraph NoWheel["Already long · no put leg"]
    L1[Conviction & income names] --> CConly[CC only + bands]
  end
```

Use the **wheel** to **enter or grow** positions · use **CC + bands** on names you already hold full size.

---

## 7. Cash flow (premium → deploy)

```mermaid
flowchart TB
  PREM[Options premium + harvest credits]
  PREM --> CASH[Agentic cash]

  CASH --> BUF[~$2k BP buffer]
  CASH --> PCOL[Put collateral if CSP open]
  CASH --> SWEEP[$3k manual withdraw ~15th if sweep ready]

  CASH --> DEP{Deploy focus?}
  DEP -->|FILL-SLOTS| CC[Write idle covered calls]
  DEP -->|INDEX| IDX[Buy RSP/ITOT/SPY or index CSP]
  DEP -->|MIXED| BOTH[CC fills + one CSP slot]
  DEP -->|BLOCKED| HOLD[Hold until gates clear]

  CC --> PREM
  IDX --> PREM
```

---

## 8. Tier C gates (auto-place checklist)

```mermaid
flowchart TD
  O[Proposed order] --> G1{Agentic account?}
  G1 -->|no| X[ESCALATE]
  G1 -->|yes| G2{Matches band / sleeve / earnings?}
  G2 -->|no| X
  G2 -->|yes| G3{Economic spread PASS?}
  G3 -->|no| X
  G3 -->|yes| G4{Coverage / BP / CSP buffer OK?}
  G4 -->|no| X
  G4 -->|yes| G5{review_option_order clean?}
  G5 -->|no| X
  G5 -->|yes| G6{User continue on Slack?}
  G6 -->|no| R[Report only]
  G6 -->|yes| P[place_option_order]
```

Spread PASS if **any**: ≤20% of mid · ≤$0.15 abs · adverse fill ≤10% roll credit or **≤$0.25** close-only.

---

## 9. Income scale (full book targets)

```mermaid
block-beta
  columns 4
  block:Idle["Today · ~29 idle CC slots"]:1
  block:Partial["Partial book · ~$3–5k/mo net"]:1
  block:Full["Full book · ~49 CC slots"]:1
  block:Net["Target net · ~$7–8k/mo typical"]:1
```

| Stage | Gross STO / mo | Net after harvest & defend |
|-------|----------------|----------------------------|
| Partial deployment | ~$4k open | ~$3–5k |
| Full book | ~$8.7–9.1k | ~$7–8k typical · ≥$6k floor |

---

## 10. One-page ASCII summary

```
┌─────────────────────────────────────────────────────────────┐
│  LONG STOCK (conviction + income + index)                   │
│    └─ short CALLS ── Δ bands: harvest | hold | defend       │
│    └─ idle CC? ── FILL-SLOTS month                          │
├─────────────────────────────────────────────────────────────┤
│  CASH ── CSP (accum AMD/META · index RSP/ITOT/SPY)          │
│    └─ assigned ── more shares ── more CC capacity           │
│    └─ book full? ── INDEX month                             │
├─────────────────────────────────────────────────────────────┤
│  DAILY: snapshot → classify → gates → Slack → continue?     │
└─────────────────────────────────────────────────────────────┘
```

---

## Related docs

- [strategy.md](strategy.md) — full rules
- [slack-automations.md](slack-automations.md) — Slack prompts
- [income-sweep.md](income-sweep.md) — savings withdraw policy
- [.cursor/skills/robinhood-delta-band-cc/SKILL.md](../.cursor/skills/robinhood-delta-band-cc/SKILL.md) — agent procedure
