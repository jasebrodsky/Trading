# Greenfield overlay — implementation plan

Blueprint for a **new repository** (`overlay` or `agentic-overlay`) that replaces the agent-centric Trading repo runtime with a small, testable control plane. The current repo (`Trading`) remains the reference for strategy rules and UX until cutover.

**Status:** Planning · **Last updated:** 2026-07-27

---

## 1. Executive summary

Build a **single-account options overlay** for Robinhood Agentic (`420763765`) that:

1. **Ingests** positions and quotes on a schedule during market hours
2. **Evaluates** delta-band rules (Conviction / Income / Accumulation / Index sleeves)
3. **Proposes** actions when gates pass
4. **Notifies** via Slack and web; **executes** only after approval (or Tier C auto when enabled)
5. **Surfaces** live portfolio + historical insights via a dashboard API

**Core principle:** Postgres is source of truth; Slack and web are clients; Robinhood credentials never leave the server; no git commits for market data.

---

## 2. Goals and non-goals

### Goals (v1)

| Goal | Success criterion |
|------|-------------------|
| Continuous ingest | Positions/quotes updated every ≤60s in RTH |
| Strategy parity | Same band table, sleeves, earnings, gates as `docs/strategy.md` |
| Proposal workflow | Every actionable trade is a `proposal` row with audit trail |
| Slack approval | Approve/reject buttons → order placed or skipped deterministically |
| Web dashboard | Portfolio, open book, proposals queue, charts from DB |
| Kill switch | Global `trading_paused` stops all execution |
| Dry-run mode | Full eval + proposals marked `dry_run`; no broker orders |

### Non-goals (v1)

- Multi-account or IRA trading
- Multi-leg / spreads (MCP Level 2 only)
- Tick-level or WebSocket broker streaming
- Generic “any strategy” platform (one strategy family)
- Cursor agents as production scheduler
- Public unauthenticated dashboard (auth required)

### v2 (after v1 stable)

- Tier C auto-execute without Slack step
- Web approve/reject (parity with Slack)
- Optional thin MCP server over API for Cursor debugging
- Migration: read-only parity check vs old canvas metrics

---

## 3. Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                        overlay (monolith)                        │
├─────────────────────────────────────────────────────────────────┤
│  worker process          │  api process                         │
│  · ingest loop           │  · REST + SSE                        │
│  · strategy eval         │  · Slack webhook handlers            │
│  · execution (on approve)│  · Firebase/IAP auth middleware      │
├──────────────────────────┴──────────────────────────────────────┤
│  packages: broker · strategy · models · notifications            │
└──────────────────────────┬──────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
    PostgreSQL          Robinhood API        Slack API
    (Cloud SQL)         (REST)               (Bot + interactivity)
```

**Realtime model:** poll broker → upsert DB → eval → SSE push to web. Not broker WebSocket.

---

## 4. Tech stack

| Layer | Choice | Notes |
|-------|--------|-------|
| Language | Python 3.12 | Align with trading scripts |
| API | FastAPI | OpenAPI, async, SSE |
| ORM | SQLAlchemy 2 + Alembic | Migrations from day one |
| Worker | Same codebase; `overlay worker` CLI | asyncio loop |
| DB | PostgreSQL 15 (Cloud SQL) | Snapshots + proposals + audit |
| Web | Vite + React + TypeScript | Or Svelte if preferred |
| Charts | Chart.js or Recharts | Match current canvas views |
| Auth | Firebase Auth → API JWT | Or Google IAP on Cloud Run |
| Secrets | GCP Secret Manager | RH tokens, Slack secrets |
| Deploy | Cloud Run (api + worker) | `min_instances=1` worker in RTH |
| Scheduler | Cloud Scheduler | Health, RTH window flags, backup tick |
| Hosting | Firebase Hosting | `web/` static build |
| CI | GitHub Actions | test → deploy on main |
| Local | `docker-compose` (postgres + api + worker) | No cloud required for dev |

---

## 5. Repository structure

```text
agentic-overlay/
├── README.md
├── pyproject.toml              # uv or poetry
├── docker-compose.yml
├── Dockerfile
├── alembic.ini
├── apps/
│   ├── api/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── portfolio.py
│   │   │   ├── proposals.py
│   │   │   ├── snapshots.py
│   │   │   ├── slack.py
│   │   │   └── stream.py       # SSE
│   │   └── deps.py               # auth, db session
│   └── worker/
│       ├── main.py
│       ├── ingest.py
│       ├── evaluate.py
│       └── execute.py
├── packages/
│   ├── broker/
│   │   ├── client.py             # Robinhood HTTP client
│   │   ├── auth.py
│   │   └── types.py
│   ├── strategy/
│   │   ├── engine.py             # classify → propose
│   │   ├── gates.py
│   │   ├── sleeves.py
│   │   └── market_hours.py
│   ├── models/
│   │   ├── db.py
│   │   └── schemas.py            # Pydantic
│   └── notifications/
│       └── slack.py
├── strategy/
│   ├── strategy.yaml             # human-edited rules
│   └── README.md                 # how to edit safely
├── web/
│   ├── package.json
│   └── src/
│       ├── pages/
│       │   ├── Dashboard.tsx
│       │   ├── Proposals.tsx
│       │   └── History.tsx
│       └── components/           # mirror canvas sections
├── tests/
│   ├── unit/
│   └── integration/
├── infra/
│   ├── terraform/                # or scripts/gcp-setup.sh
│   └── cloudrun.yaml
└── docs/
    ├── architecture.md
    ├── api.md
    └── runbook.md
```

---

## 6. Data model

### 6.1 Tables

#### `app_config` (singleton row)

| Column | Type | Description |
|--------|------|-------------|
| `trading_paused` | bool | Kill switch |
| `auto_execute_tier_c` | bool | v2: auto-place when gates pass |
| `ingest_interval_sec` | int | Default 60 |
| `dry_run` | bool | Never call place_order |

#### `accounts`

| Column | Type |
|--------|------|
| `id` | uuid PK |
| `broker_account_id` | text UNIQUE (`420763765`) |
| `display_name` | text |
| `agentic_allowed` | bool (cached from broker) |

#### `equity_positions` / `option_positions`

Upserted each ingest. Key: `(account_id, instrument_id)`.

Include: symbol, quantity, avg_cost, market_value, updated_at.

#### `quotes`

Upserted each ingest. Key: `(instrument_id, as_of)`.

Equity: bid, ask, last, mid. Option: bid, ask, delta, iv, dte, etc.

#### `snapshots`

Periodic rollup for charts (every ingest or every 5 min).

| Column | Type |
|--------|------|
| `id` | uuid |
| `account_id` | uuid |
| `as_of` | timestamptz |
| `total_value` | numeric |
| `equity` | numeric |
| `cash` | numeric |
| `buying_power` | numeric |
| `options_market_value` | numeric |
| `realized_pnl_mtd` | numeric |
| `realized_pnl_ytd` | numeric |
| `payload` | jsonb | Coverage, runway, ledger, open book summary |

`payload` mirrors current `canvas/data/snapshot.json` shape for UI portability.

#### `proposals`

| Column | Type |
|--------|------|
| `id` | uuid PK |
| `account_id` | uuid |
| `status` | enum: `pending`, `approved`, `rejected`, `executing`, `done`, `failed`, `expired` |
| `tier` | enum: `A`, `B`, `C` |
| `action` | enum: `harvest_rewrite`, `harvest_close_only`, `defend_roll`, `earnings_flatten`, `idle_cc`, `index_csp`, `accumulation_csp`, `csp_harvest`, `csp_defend` |
| `symbol` | text |
| `summary` | text | Human-readable one-liner |
| `legs` | jsonb | Order legs for review/place |
| `metrics` | jsonb | delta, dte, credit, spread, etc. |
| `gates` | jsonb | Per-gate pass/fail + reasons |
| `dry_run` | bool |
| `slack_channel` | text nullable |
| `slack_message_ts` | text nullable |
| `approved_by` | text nullable |
| `approved_at` | timestamptz nullable |
| `rejected_by` | text nullable |
| `expires_at` | timestamptz | Stale proposals auto-expire |
| `created_at` | timestamptz |
| `updated_at` | timestamptz |

Unique constraint: prevent duplicate pending proposals for same `(symbol, action)` — upsert or skip.

#### `executions`

| Column | Type |
|--------|------|
| `id` | uuid |
| `proposal_id` | uuid FK |
| `broker_order_ids` | jsonb |
| `review_response` | jsonb |
| `status` | enum: `reviewing`, `placed`, `filled`, `failed`, `cancelled` |
| `error` | text nullable |
| `placed_at` | timestamptz |

#### `audit_log`

Append-only: who did what, proposal state changes, kill switch toggles.

### 6.2 Indexes

- `proposals (status, created_at)` where status = pending
- `snapshots (account_id, as_of DESC)`
- `quotes (instrument_id, as_of DESC)`

---

## 7. Strategy configuration (`strategy/strategy.yaml`)

Port from `Trading/docs/strategy.md`. Structure:

```yaml
version: 1
account:
  broker_id: "420763765"
  require_agentic_allowed: true

sleeves:
  conviction:
    symbols: [NVDA, AMZN, ONEQ, SPY, MU]
    entry_delta: [0.12, 0.18]
    target_delta: 0.15
  income:
  # default: not in conviction list
    entry_delta: [0.20, 0.30]
    target_delta: 0.25
  accumulation:
    symbols: [AMD, META]
    csp_entry_delta: [0.20, 0.25]
    min_shares_for_cc: 100
  index:
    prefer_order: [RSP, ITOT, SPY]
    avoid_csp: [VOO, IVV]

bands:
  harvest_max_delta: 0.12
  hold_max_delta: 0.45
  dwell:
    full_session_outside_band: true
    delta_move_from_entry: 0.10

dte:
  target_min: 30
  target_max: 45
  harvest_close_floor: 10

earnings:
  blackout_trading_days: 5
  refill_requires_session_after_print: true

gates:
  bp_buffer_usd: 2000
  spread_pct_of_mid: 0.20
  spread_abs_usd: 0.15
  adverse_fill_pct_of_credit: 0.10
  adverse_fill_close_only_usd: 0.25
  defend_debit_buffer_usd: 50

automation:
  default_tier: B          # notify + approve
  tier_c_actions: [...]    # which actions can auto when enabled

cadence:
  eval_after_ingest: true
  market_hours_tz: America/New_York
```

**Rule:** YAML changes require unit test updates; optional generated markdown doc for humans.

---

## 8. Worker loops

### 8.1 Ingest (`worker/ingest.py`)

Every `ingest_interval_sec` while `is_regular_session()`:

1. Verify account `agentic_allowed`
2. `get_portfolio` → cache BP, cash, totals
3. `get_equity_positions` + `get_equity_quotes`
4. `get_option_positions` + `get_option_instruments` + `get_option_quotes`
5. `get_earnings_results` (cache with TTL)
6. Upsert positions + quotes
7. Build `snapshot` row (rollup JSON)
8. Emit internal event: `ingest_complete`

If outside RTH: ingest optional (portfolio only, no eval) or sleep until open.

### 8.2 Evaluate (`worker/evaluate.py`)

On `ingest_complete`:

1. Load `strategy.yaml`
2. For each open option position → `classify()` → harvest / hold / defend / earnings
3. For idle CC capacity → `idle_cc_candidates()`
4. For accumulation / index CSP slots → `csp_candidates()`
5. For each candidate action → `run_gates()` → if all pass → create `proposal` (tier B or C)
6. Skip if duplicate pending proposal exists
7. Notify Slack for new `pending` proposals (tier B)
8. If `auto_execute_tier_c` and tier C → queue execution

### 8.3 Execute (`worker/execute.py`)

Triggered by API (Slack approve or web):

1. Load proposal; verify `pending` or `approved`
2. Re-run gates on **live** quotes (no stale memory)
3. `review_option_order` → if blockers → `failed` + notify
4. If `dry_run` or `trading_paused` → mark done without place
5. `place_option_order` → store order ids → `executing` → poll fill → `done`
6. Write `audit_log`

**Idempotency:** `approved` → only one execution row; use DB transaction + status check.

---

## 9. API (REST + SSE)

Base: `https://overlay-api-<project>.run.app`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness |
| GET | `/v1/portfolio` | Latest positions + quotes + portfolio totals |
| GET | `/v1/snapshots` | Time series (`?from=&to=&limit=`) |
| GET | `/v1/snapshots/latest` | Current rollup (canvas payload) |
| GET | `/v1/proposals` | List (`?status=pending`) |
| GET | `/v1/proposals/{id}` | Detail |
| POST | `/v1/proposals/{id}/approve` | Auth required |
| POST | `/v1/proposals/{id}/reject` | Auth required |
| POST | `/v1/admin/pause` | Kill switch on |
| POST | `/v1/admin/resume` | Kill switch off |
| GET | `/v1/stream` | SSE: snapshot + proposal events |

### Slack routes (unsigned → verify signature)

| Method | Path |
|--------|------|
| POST | `/v1/slack/events` |
| POST | `/v1/slack/interactions` |

---

## 10. Slack integration

**Replace** Cursor automations with a **Slack Bot app**:

| Event | Behavior |
|-------|----------|
| New `pending` proposal | Post to `#all-agentic-trading` with Approve / Reject block kit |
| Daily digest (optional) | Cloud Scheduler → API posts morning scoreboard (no orders) |
| Button Approve | `POST /proposals/{id}/approve` → execute |
| Button Reject | `POST /proposals/{id}/reject` |

**Portfolio chat:** separate channel webhook → API `POST /v1/chat` (read-only LLM optional, v2) or skip v1.

Store `slack_message_ts` on proposal for thread updates on execution result.

---

## 11. Web application

### Pages (mirror current canvas)

| Page | Data source | Notes |
|------|-------------|-------|
| **Scorecard** | `/snapshots/latest` | BP, MTD/YTD, pulse |
| **Equities** | `/portfolio` | Winners/losers, sleeves |
| **Options** | `/portfolio` + snapshot payload | Open book, coverage heatmap |
| **Proposals** | `/proposals` | Queue + approve/reject |
| **History** | `/proposals?status=done` + executions | Audit |
| **Settings** | `/admin` | Pause, dry-run (auth) |

### Realtime

- `EventSource` on `/v1/stream`
- On `snapshot_updated` → refresh charts
- On `proposal_created` → toast + proposals list

### Auth

- Firebase Google sign-in; allowlist emails in env
- No broker credentials in browser

---

## 12. GCP infrastructure

| Resource | Config |
|----------|--------|
| Project | Same or new GCP project |
| Cloud SQL | `db-f1-micro` dev; `db-custom-1-3840` prod |
| Cloud Run `overlay-api` | min 0, max 2 |
| Cloud Run `overlay-worker` | min 1 during RTH (Scheduler toggles or in-app sleep) |
| Secret Manager | `robinhood-credentials`, `slack-bot-token`, `slack-signing-secret` |
| Cloud Scheduler | `*/5 9-16 America/New_York` health; optional digest at 12:00 ET |
| Firebase Hosting | `web/` |
| IAM | Service account: SQL client, Secret accessor |

**Cost estimate (rough):** Cloud SQL ~$10–30/mo + Cloud Run usage; negligible at single-user scale.

---

## 13. Milestones

### M0 — Scaffold (week 0)

**Deliverables:**

- New repo with pyproject, docker-compose, FastAPI stub, Alembic, empty React app
- CI: lint + pytest on PR

**Acceptance:**

- `docker compose up` → API `/health` 200, Postgres connected

---

### M1 — Broker package (week 1)

**Deliverables:**

- Robinhood auth (token refresh)
- Read: portfolio, equity/option positions, quotes, earnings
- Read: `review_option_order`, `place_option_order` (dry-run flag)

**Acceptance:**

- Integration test against sandbox or recorded fixtures
- Manual script prints Agentic account summary

**Depends on:** RH credentials in local `.env` (never commit)

---

### M2 — Ingest + snapshots (week 2)

**Deliverables:**

- Worker ingest loop
- Tables: positions, quotes, snapshots
- Snapshot rollup approximating current `snapshot.json` sections

**Acceptance:**

- 5 min local run → snapshots table grows; payload has BP, open book, coverage

---

### M3 — Strategy engine (week 3–4)

**Deliverables:**

- `strategy.yaml` ported from `docs/strategy.md`
- `engine.py`: classify, idle CC, CSP candidates
- `gates.py`: spread, earnings, BP buffer, market hours (America/New_York)

**Acceptance:**

- Unit tests for each band zone with fixture positions
- Parity checklist: 10 historical runbook scenarios from `Trading/runbooks/` classify same action

---

### M4 — Proposals (week 4)

**Deliverables:**

- Eval creates proposals (dry-run default)
- API list/detail
- Expire stale proposals

**Acceptance:**

- Dry-run worker run → pending proposals in DB; no broker orders

---

### M5 — Slack approve path (week 5)

**Deliverables:**

- Slack app + interactivity
- Approve → execute → thread update

**Acceptance:**

- One real harvest-close or small dry-run order end-to-end in Slack

---

### M6 — Web dashboard v1 (week 6–7)

**Deliverables:**

- Scorecard + options views from API
- Proposals page with approve/reject
- SSE refresh

**Acceptance:**

- Dashboard matches canvas numbers within ingest lag
- Approve from web works

---

### M7 — Production hardening (week 8)

**Deliverables:**

- Deploy to GCP
- Kill switch, audit log, alerts on worker failure
- Runbook: token refresh, pause trading, rollback

**Acceptance:**

- 1 week RTH dry-run in prod with `dry_run=true`
- No missed ingest > 3 intervals without alert

---

### M8 — Cutover (week 9+)

**Deliverables:**

- `dry_run=false` for tier B (Slack approve)
- Optional tier C auto flag
- Archive Cursor daily automation (report-only) or keep as backup

**Acceptance:**

- Trading repo canvas becomes read-only archive or redirects to new URL

---

## 14. Testing strategy

| Layer | Approach |
|-------|----------|
| Gates / classify | Unit tests + fixtures from real MCP snapshots (saved JSON) |
| Engine | Property tests on delta bands |
| API | httpx AsyncClient + test DB |
| Execute | Mock broker client; never place in CI |
| E2E | Manual Slack + staging account |

**Fixture library:** export 3–5 ingest snapshots from current MCP runs into `tests/fixtures/`.

---

## 15. Security checklist

- [ ] Robinhood secrets only in Secret Manager / local `.env`
- [ ] API auth on all mutating routes
- [ ] Slack signature verification
- [ ] Proposal approve requires authenticated user in allowlist
- [ ] Rate limit approve endpoint
- [ ] Audit log immutable
- [ ] `trading_paused` checked in execute path
- [ ] Account id hard-validated to `420763765` in execute path

---

## 16. Relationship to `Trading` repo

| Trading artifact | Greenfield use |
|------------------|----------------|
| `docs/strategy.md` | Source for `strategy.yaml` + tests |
| `canvas/index.html` | UX reference for web pages |
| `canvas/data/snapshot.json` | Schema reference for `snapshots.payload` |
| `.cursor/skills/...` | Retire after M8 (or thin MCP wrapper on API) |
| `docs/slack-automations.md` | Replace with Slack Bot docs |
| Runbooks | Parity test cases |

**Do not migrate:** git-based snapshot pipeline, Cloud Build for JSON, three Cursor automations.

---

## 17. Open decisions (resolve before M1)

| # | Decision | Options | Recommendation |
|---|----------|---------|----------------|
| 1 | Repo name / GCP project | New project vs `hello-again-e68e6` | New repo `agentic-overlay`; same GCP project OK |
| 2 | Robinhood client | Raw HTTP vs existing library | Raw HTTP or thin wrapper; mirror MCP tool behavior |
| 3 | Package manager | uv vs poetry | uv (fast CI) |
| 4 | Web framework | React vs Svelte | React (ecosystem) |
| 5 | Auth | Firebase vs IAP | Firebase Auth + allowlist (simpler for mobile) |
| 6 | v1 execution tier | B only vs B+C | B only (Slack approve); C in M8 |
| 7 | Ingest interval | 30s vs 60s | 60s default; tune in `app_config` |
| 8 | LLM portfolio chat | v1 vs v2 | v2; SQL-backed Q&A API in v1 optional |

---

## 18. Immediate next actions

1. Create GitHub repo `agentic-overlay` from M0 scaffold
2. Resolve open decision #1–2
3. Export MCP fixture JSON from one live Agentic pull
4. Port `strategy.yaml` skeleton + first unit test (NVDA harvest fixture)
5. Set up GCP Secret Manager placeholders (no prod credentials until M5)

---

## Appendix A — Proposal `action` enum mapping

| Action | Strategy source |
|--------|-----------------|
| `harvest_rewrite` | Band harvest + rewrite liquidity PASS |
| `harvest_close_only` | Harvest + rewrite FAIL spread |
| `defend_roll` | Δ > 0.45 |
| `earnings_flatten` | Earnings ≤5 days, BTC only |
| `idle_cc` | Unused CC capacity |
| `index_csp` | Index sleeve new CSP |
| `accumulation_csp` | AMD/META wheel |
| `csp_harvest` | Short put Δ < 0.12 |
| `csp_defend` | Short put Δ > 0.45 |

## Appendix B — SSE event types

```json
{ "type": "snapshot_updated", "as_of": "..." }
{ "type": "proposal_created", "id": "...", "symbol": "...", "summary": "..." }
{ "type": "proposal_updated", "id": "...", "status": "done" }
{ "type": "trading_paused", "value": true }
```
