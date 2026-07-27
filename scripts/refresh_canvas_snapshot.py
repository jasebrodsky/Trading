#!/usr/bin/env python3
"""Rebuild canvas/data/snapshot.json and equities.json from embedded live MCP data."""

import json
import math
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_PATH = ROOT / "canvas/data/snapshot.json"
EQUITIES_PATH = ROOT / "canvas/data/equities.json"
INDEX_PATH = ROOT / "canvas/index.html"

CONVICTION = {"NVDA", "AMZN", "ONEQ", "SPY", "MU"}
ACCUM = {"AMD", "META"}

PORTFOLIO = {
    "totalValue": round(693002.86, 2),
    "equityValue": round(545728.10, 2),
    "optionsValue": -7973,
    "cash": round(155247.76, 2),
    "buyingPower": round(34271.70, 2),
}

POSITIONS = [
    {"symbol": "MU", "qty": 100.163327, "avg": 129.91},
    {"symbol": "DAL", "qty": 569.170835, "avg": 40.87},
    {"symbol": "TSLA", "qty": 108.9, "avg": 335.98},
    {"symbol": "NVDA", "qty": 141.912449, "avg": 77.43},
    {"symbol": "AAL", "qty": 1465.116563, "avg": 19.21},
    {"symbol": "AMZN", "qty": 140.7426, "avg": 160.15},
    {"symbol": "MRNA", "qty": 108.0, "avg": 222.96},
    {"symbol": "AMD", "qty": 45.0, "avg": 81.63},
    {"symbol": "PFE", "qty": 765.135619, "avg": 48.17},
    {"symbol": "ONEQ", "qty": 1181.374909, "avg": 61.64},
    {"symbol": "TXN", "qty": 39.008947, "avg": 186.21},
    {"symbol": "GLD", "qty": 15.0, "avg": 377.99},
    {"symbol": "HOOD", "qty": 250.0, "avg": 38.0},
    {"symbol": "INTC", "qty": 295.702749, "avg": 55.63},
    {"symbol": "META", "qty": 20.0, "avg": 612.16},
    {"symbol": "DJT", "qty": 420.0, "avg": 48.01},
    {"symbol": "ABNB", "qty": 75.0, "avg": 184.37},
    {"symbol": "SNAP", "qty": 600.0, "avg": 50.38},
    {"symbol": "ZM", "qty": 17.0, "avg": 149.64},
    {"symbol": "UNH", "qty": 24.922375, "avg": 495.91},
    {"symbol": "VALE", "qty": 331.044078, "avg": 16.56},
    {"symbol": "XOM", "qty": 52.963062, "avg": 120.13},
    {"symbol": "REGN", "qty": 8.418592, "avg": 600.01},
    {"symbol": "AMC", "qty": 0.213333, "avg": 65.63},
    {"symbol": "MSFT", "qty": 0.501835, "avg": 207.24},
    {"symbol": "AAPL", "qty": 0.68294, "avg": 118.0},
    {"symbol": "VIP", "qty": 1.0, "avg": 337.79},
]

QUOTES = {
    "MU": 890.39, "DAL": 86.28, "TSLA": 308.35, "NVDA": 196.77, "AAL": 14.825,
    "AMZN": 231.965, "MRNA": 55.835, "AMD": 493.33, "PFE": 24.715, "ONEQ": 98.28,
    "TXN": 279.36, "GLD": 374.83, "HOOD": 95.65, "INTC": 91.31, "META": 594.424,
    "DJT": 9.685, "ABNB": 146.935, "SNAP": 4.525, "ZM": 90.98, "UNH": 417.64,
    "VALE": 14.765, "XOM": 154.585, "REGN": 671.69, "AMC": 2.435, "MSFT": 390.45,
    "AAPL": 336.31, "VIP": 2.28, "SPY": 737.0,
}

OPEN_BOOK = [
    {"symbol": "NVDA", "optionType": "call", "strike": 230, "expiration": "2026-08-28", "qty": 1, "credit": 172, "mark": 1.635, "delta": 0.134, "sleeve": "conviction", "role": "CC"},
    {"symbol": "INTC", "optionType": "call", "strike": 110, "expiration": "2026-08-28", "qty": 2, "credit": 660, "mark": 3.475, "delta": 0.276, "sleeve": "income", "role": "CC"},
    {"symbol": "MU", "optionType": "call", "strike": 1240, "expiration": "2026-08-28", "qty": 1, "credit": 1695, "mark": 16.70, "delta": 0.147, "sleeve": "conviction", "role": "CC"},
    {"symbol": "AAL", "optionType": "call", "strike": 16.5, "expiration": "2026-08-28", "qty": 10, "credit": 280, "mark": 0.315, "delta": 0.261, "sleeve": "income", "role": "CC"},
    {"symbol": "DAL", "optionType": "call", "strike": 94, "expiration": "2026-08-28", "qty": 5, "credit": 670, "mark": 1.32, "delta": 0.245, "sleeve": "income", "role": "CC"},
    {"symbol": "TSLA", "optionType": "call", "strike": 345, "expiration": "2026-08-28", "qty": 1, "credit": 695, "mark": 5.65, "delta": 0.239, "sleeve": "income", "role": "CC"},
    {"symbol": "PFE", "optionType": "call", "strike": 26, "expiration": "2026-08-28", "qty": 3, "credit": 69, "mark": 0.27, "delta": 0.263, "sleeve": "income", "role": "CC", "flag": "tomorrow-flatten"},
    {"symbol": "AAL", "optionType": "call", "strike": 16, "expiration": "2026-08-28", "qty": 4, "credit": 143, "mark": 0.475, "delta": 0.342, "sleeve": "income", "role": "CC"},
    {"symbol": "AMD", "optionType": "put", "strike": 460, "expiration": "2026-08-28", "qty": 1, "credit": 2100, "mark": 31.025, "delta": 0.339, "sleeve": "accumulation", "role": "CSP", "flag": "tomorrow-flatten"},
    {"symbol": "SPY", "optionType": "put", "strike": 715, "expiration": "2026-08-21", "qty": 1, "credit": 492, "mark": 5.06, "delta": 0.231, "sleeve": "index", "role": "CSP"},
]


def sleeve(sym: str) -> str:
    if sym in CONVICTION:
        return "conviction"
    if sym in ACCUM:
        return "accumulation"
    return "income"


def zone(delta: float, flag: str | None = None) -> str:
    if flag == "tomorrow-flatten":
        return "hold"
    ad = abs(delta)
    if ad < 0.12:
        return "harvest"
    if ad > 0.45:
        return "defend"
    return "hold"


def build_equities():
    seen = set()
    rows = []
    total_mv = 0
    total_unreal = 0
    for p in POSITIONS:
        sym = p["symbol"]
        if sym in seen or sym in ("AMC", "MSFT", "AAPL", "VIP"):
            continue
        seen.add(sym)
        last = QUOTES[sym]
        mv = round(p["qty"] * last)
        cost = p["qty"] * p["avg"]
        unreal = round(mv - cost)
        pct = round((last / p["avg"] - 1) * 100, 1) if p["avg"] else 0
        total_mv += mv
        total_unreal += unreal
        rows.append({
            "symbol": sym,
            "shares": round(p["qty"], 3),
            "avgCost": p["avg"],
            "last": round(last, 3),
            "marketValue": mv,
            "unrealized": unreal,
            "unrealizedPct": pct,
            "sleeve": sleeve(sym),
        })
    rows.sort(key=lambda r: -r["unrealized"])
    return rows, total_mv, total_unreal


def short_calls_by_symbol():
    m = {}
    for leg in OPEN_BOOK:
        if leg["role"] == "CC":
            m[leg["symbol"]] = m.get(leg["symbol"], 0) + leg["qty"]
    return m


def build_coverage(equities):
    shorts = short_calls_by_symbol()
    cov = []
    key_symbols = [
        "MU", "NVDA", "TSLA", "PFE", "AAL", "AMD", "AMZN", "ONEQ", "DAL", "INTC",
        "HOOD", "MRNA", "VALE", "SNAP", "DJT",
    ]
    eq_map = {e["symbol"]: e for e in equities}
    for sym in key_symbols:
        e = eq_map.get(sym)
        if not e:
            continue
        cap = math.floor(e["shares"] / 100)
        covered = shorts.get(sym, 0)
        idle = max(0, cap - covered)
        puts = 1 if sym == "AMD" and any(l["symbol"] == "AMD" and l["role"] == "CSP" for l in OPEN_BOOK) else 0
        status = "idle"
        if sym == "PFE":
            status = "hold-tomorrow-flatten"
        elif sym == "AMD":
            status = "hold-tomorrow-flatten"
        elif covered == cap and cap > 0:
            status = "covered"
        elif covered > 0:
            status = "partial"
        elif sym in ("SNAP", "DJT"):
            status = "skip-thin-tape"
        elif sym == "AMZN":
            status = "idle"
        earnings_blackout = sym in ("HOOD", "AMZN", "VALE", "MRNA")
        cov.append({
            "symbol": sym,
            "shares": round(e["shares"], 1),
            "capacity": cap,
            "covered": covered,
            "idle": idle,
            "puts": puts,
            "sleeve": sleeve(sym),
            "status": status,
            "earningsDate": {
                "PFE": "2026-08-04", "AMD": "2026-08-04", "HOOD": "2026-07-29",
                "META": "2026-07-29", "AMZN": "2026-07-30", "VALE": "2026-07-30",
                "MRNA": "2026-07-31", "NVDA": "2026-08-26", "INTC": "2026-07-23",
            }.get(sym),
            "earningsTradingDays": {
                "PFE": 6, "AMD": 6, "HOOD": 2, "AMZN": 3, "VALE": 3, "MRNA": 4, "NVDA": 22,
            }.get(sym),
            "earningsBlackout": earnings_blackout,
            "assignmentRisk": sym in ("MU", "NVDA") and covered > 0,
            "assignmentNote": {
                "MU": "Embedded LTCG — hold (|Δ| 0.147). Rewritten $1240C 8/28 after harvest.",
                "NVDA": "Embedded LTCG — hold (|Δ| 0.134). Rewritten $230C 8/28 after harvest.",
                "INTC": "Printed Jul 23 AM. Refilled 2× $110C 8/28 today.",
            }.get(sym),
        })
    return cov


def build_open_book():
    rows = []
    for leg in OPEN_BOOK:
        dte = 32 if leg["expiration"] == "2026-08-28" else 25
        extrinsic = round(leg["mark"] * 100 * leg["qty"])
        rows.append({
            "symbol": leg["symbol"],
            "side": "short",
            "optionType": leg["optionType"],
            "strike": leg["strike"],
            "expiration": leg["expiration"],
            "dte": dte,
            "qty": leg["qty"],
            "credit": leg["credit"],
            "mark": leg["mark"],
            "delta": leg["delta"],
            "zone": zone(leg["delta"], leg.get("flag")),
            "sleeve": leg["sleeve"],
            "role": leg["role"],
            "extrinsic": extrinsic,
            **({"flag": leg["flag"]} if leg.get("flag") else {}),
        })
    return rows


def main():
    now = datetime.now(ZoneInfo("America/New_York"))
    as_of = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    as_of = as_of[:-2] + ":" + as_of[-2:]
    label = now.strftime("%b %d, %Y %-I:%M %p ET") + " (post-continue · Agentic ••••3765)"

    equities, total_mv, total_unreal = build_equities()
    open_book = build_open_book()
    coverage = build_coverage(equities)

    open_credit = sum(l["credit"] for l in OPEN_BOOK)
    open_extrinsic = sum(r["extrinsic"] for r in open_book)
    mark_pnl = open_extrinsic - open_credit

    idle_cc = sum(c["idle"] for c in coverage if c["status"] not in ("skip-thin-tape", "hold-tomorrow-flatten"))
    idle_blocked = sum(c["idle"] for c in coverage if c.get("earningsBlackout"))
    idle_skip = sum(c["idle"] for c in coverage if c["status"] == "skip-thin-tape")

    hold = sum(1 for r in open_book if r["zone"] == "hold")
    harvest = sum(1 for r in open_book if r["zone"] == "harvest")

    snap = json.loads(SNAPSHOT_PATH.read_text())
    snap["asOf"] = as_of
    snap["asOfLabel"] = label
    snap["dataNote"] = (
        "Live MCP refresh after continue/stop EXECUTE (Jul 27 ~3:42 PM ET). "
        "Harvest rolls: MU $1300C→$1240C, NVDA $225C→$230C. Idle fills: ONEQ pending, "
        "AAL +10, DAL +5, INTC +2 CCs. PFE ×3 + AMD CSP enter earnings window tomorrow — flatten before Jul 28 check."
    )
    snap["portfolio"] = PORTFOLIO
    snap["pnl"] = {
        "realizedMtdOptions": 3961,
        "realizedMtdEquity": 0,
        "realizedYtdOptions": 3961,
        "realizedYtdAll": 3961,
        "unrealizedEquity": total_unreal,
        "unrealizedNote": f"Full equity book vs avg cost (live Jul 27 prices at {now.strftime('%-I:%M %p ET')})",
    }

    # Ledger — update July with post-continue fills
    snap["ledger"]["ytd"]["credits"] = 13096
    snap["ledger"]["ytd"]["debits"] = 2159
    snap["ledger"]["ytd"]["netIncome"] = 10937
    snap["ledger"]["ytd"]["realizedOptions"] = 3961
    snap["ledger"]["ytd"]["openCredit"] = open_credit
    snap["ledger"]["ytd"]["endingValue"] = PORTFOLIO["totalValue"]
    snap["ledger"]["ytd"]["totalReturn"] = 3961
    for m in snap["ledger"]["months"]:
        if m["month"] == "2026-07":
            m["credits"] = 10620
            m["debits"] = 2159
            m["netIncome"] = 8461
            m["realizedOptions"] = 3961
            m["totalValue"] = PORTFOLIO["totalValue"]
            m["totalReturn"] = 3961

    snap["callouts"] = {
        "loudest": (
            "POST-CONTINUE: 19 new CC contracts filled (AAL +10, DAL +5, INTC +2, MU+NVDA harvest rewrites). "
            "PFE ×3 + AMD CSP still enter earnings window TOMORROW — flatten before Jul 28 morning check. "
            "ONEQ 11 idle CC slots remain."
        ),
        "counts": {
            "hold": hold,
            "harvest": harvest,
            "defend": 0,
            "earningsFlattenToday": 0,
            "earningsFlattenTomorrow": 2,
            "waitingRefill": 0,
            "idleCcFill": idle_cc,
            "idleCcBlocked": idle_blocked,
            "idleCcSkip": idle_skip,
            "accumCspOpen": 1,
            "accumCspBlocked": 1,
            "indexCspHold": 1,
            "indexCspPropose": 0,
        },
        "actions": [
            {"priority": "urgent-tomorrow", "kind": "tomorrow-flatten", "detail": "PFE $26C 8/28 ×3 — |Δ|=0.263. Flatten before Jul 28 open (Aug 4 AM enters 5-TD window)."},
            {"priority": "urgent-tomorrow", "kind": "tomorrow-flatten", "detail": "AMD $460P 8/28 ×1 — |Δ|=0.339. Mark $31.03. Flatten before Jul 28 open. Reopen Aug 5+."},
            {"priority": "now", "kind": "idle-CC-fill", "detail": "ONEQ 11 CC idle — conviction ~0.15Δ Aug 28 when gates PASS."},
            {"priority": "after-AMD-BTC", "kind": "index-CSP", "detail": "After AMD CSP closes tomorrow: RSP 1× put ~0.20Δ / 30–45 DTE eligible if BP buffer confirmed."},
            {"priority": "blocked", "kind": "earnings", "detail": "HOOD/META Jul 29 PM, AMZN/VALE Jul 30 PM, MRNA Jul 31 AM — idle CC/CSP blocked."},
            {"priority": "done", "kind": "executed", "detail": "Jul 27 continue: MU harvest $1300C→$1240C, NVDA $225C→$230C, AAL +10, DAL +5, INTC +2 CCs filled."},
        ],
    }
    snap["coverage"] = coverage
    snap["runway"] = {
        "cash": PORTFOLIO["cash"],
        "buyingPower": PORTFOLIO["buyingPower"],
        "cspCollateral": 117500,
        "bpBufferTarget": 2000,
        "bpHeadroom": round(PORTFOLIO["buyingPower"] - 2000, 2),
        "nextAccumFits": False,
        "nextIndexFits": False,
        "nextAccumSymbol": "AMD",
        "nextAccumBlockedReason": "Aug 4 earnings enters 5-TD window tomorrow — flatten CSP, reopen Aug 5+",
        "nextIndexNote": "AMD CSP slot occupied; after AMD BTC tomorrow, RSP 1× put eligible if BP buffer confirmed.",
        "note": "Cash account: BP ≈ cash − CSP collateral. Post-continue fills deployed ~$3.5k new premium.",
    }
    snap["performance"] = {
        "realizedMtdOptions": 3961,
        "realizedYtdOptions": 3961,
        "realized30d": 3961,
        "realized90d": 3961,
        "runRateAnnualized": round(3961 * 12),
        "runRatePctOfAccount": round(3961 * 12 / PORTFOLIO["totalValue"] * 100, 2),
        "unrealizedEquity": total_unreal,
        "appreciationYtd": None,
        "totalReturnYtd": 3961,
        "sleeveIncomeYtd": snap["performance"].get("sleeveIncomeYtd", {}),
        "note": "Run-rate annualizes last ~30d realized options × 12; thin sample.",
    }
    snap["forward"] = {
        "openExtrinsic": open_extrinsic,
        "openCredit": open_credit,
        "markPnL": mark_pnl,
        "idleContracts": idle_cc,
        "idleContractsBlocked": idle_blocked,
        "idleContractsSkip": idle_skip,
        "idleFillEstimate": round(idle_cc * 200),
        "idleFillNote": f"{idle_cc} eligible idle × ~$200 avg mid estimate — ONEQ 11 primary remaining.",
        "expiryCalendar": [
            {
                "expiration": "2026-08-21",
                "dte": 25,
                "legs": [r for r in open_book if r["expiration"] == "2026-08-21"],
            },
            {
                "expiration": "2026-08-28",
                "dte": 32,
                "legs": [r for r in open_book if r["expiration"] == "2026-08-28"],
            },
        ],
    }
    tv = PORTFOLIO["totalValue"]
    snap["capital"] = {
        "equityPct": round(PORTFOLIO["equityValue"] / tv * 100, 1),
        "cashPct": round(PORTFOLIO["cash"] / tv * 100, 1),
        "optionsMarkPct": round(PORTFOLIO["optionsValue"] / tv * 100, 2),
        "cspCollateralPct": round(117500 / tv * 100, 1),
        "equityValue": PORTFOLIO["equityValue"],
        "cash": PORTFOLIO["cash"],
        "optionsMark": PORTFOLIO["optionsValue"],
        "cspCollateral": 117500,
    }
    snap["openBook"] = open_book
    snap["program"] = {
        "openContracts": sum(l["qty"] for l in OPEN_BOOK),
        "openCredit": open_credit,
        "idleCcContracts": idle_cc,
        "idleCcContractsBlocked": idle_blocked,
        "idleCcContractsSkip": idle_skip,
        "cspCollateralApprox": 117500,
        "bpBufferTarget": 2000,
        "accumulation": [
            {"symbol": "AMD", "shares": 45, "need": 100, "csp": "hold-tomorrow-flatten",
             "note": "Aug28 460p · |Δ| 0.339 · FLATTEN TOMORROW · reopen Aug 5+"},
            {"symbol": "META", "shares": 20, "need": 100, "csp": "waiting-earnings",
             "note": "Earn Jul 29 PM · CSP blocked until Aug 1+"},
        ],
    }
    snap["winners"] = [{"symbol": e["symbol"], "unrealized": e["unrealized"], "pct": e["unrealizedPct"],
                        "price": e["last"], "avgCost": e["avgCost"]} for e in equities[:3]]
    snap["losers"] = [{"symbol": e["symbol"], "unrealized": e["unrealized"], "pct": e["unrealizedPct"],
                       "price": e["last"], "avgCost": e["avgCost"]} for e in equities[-3:]]
    losers_sorted = sorted(equities, key=lambda e: e["unrealized"])[:3]
    snap["losers"] = [{"symbol": e["symbol"], "unrealized": e["unrealized"], "pct": e["unrealizedPct"],
                       "price": e["last"], "avgCost": e["avgCost"]} for e in losers_sorted]
    snap["equityCurve"].append({
        "date": now.strftime("%Y-%m-%d"),
        "totalValue": PORTFOLIO["totalValue"],
        "note": "Post-continue refresh — harvest rolls + idle fills executed.",
    })
    # dedupe same-day curve points
    by_date = {}
    for pt in snap["equityCurve"]:
        by_date[pt["date"]] = pt
    snap["equityCurve"] = sorted(by_date.values(), key=lambda p: p["date"])

    snap["assignmentRisks"] = [
        {"symbol": "MU", "note": "Embedded LTCG — hold after harvest rewrite to $1240C 8/28.", "delta": 0.147},
        {"symbol": "NVDA", "note": "Embedded LTCG — hold after harvest rewrite to $230C 8/28.", "delta": 0.134},
    ]

    SNAPSHOT_PATH.write_text(json.dumps(snap, indent=2) + "\n")

    eq_doc = {
        "asOf": as_of,
        "asOfLabel": label,
        "equities": equities,
        "optionUnderlyings": [{"symbol": "SPY", "last": QUOTES["SPY"], "role": "index-CSP", "note": "No shares; $715P 8/21 ×1 held"}],
        "totalEquityValue": total_mv,
        "totalUnrealized": total_unreal,
    }
    EQUITIES_PATH.write_text(json.dumps(eq_doc, indent=2) + "\n")

    # Sync HTML fallback block
    html = INDEX_PATH.read_text()
    start = html.index('<script type="application/json" id="snapshot-fallback">')
    end = html.index("</script>", start)
    compact = json.dumps(snap, separators=(",", ":"))
    new_block = f'<script type="application/json" id="snapshot-fallback">\n{compact}\n'
    INDEX_PATH.write_text(html[:start] + new_block + html[end:])

    print(f"Wrote {SNAPSHOT_PATH}")
    print(f"Wrote {EQUITIES_PATH}")
    print(f"Updated {INDEX_PATH} fallback")
    print(f"Account value: ${PORTFOLIO['totalValue']:,.2f}")


if __name__ == "__main__":
    main()
