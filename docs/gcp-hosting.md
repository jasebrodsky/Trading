# GCP hosting plan — Agentic strategy canvas

Public static site on **Google Cloud Storage** (or Firebase Hosting). Live numbers come from `canvas/data/snapshot.json`, rebuilt by the Robinhood MCP agent and published on push.

## Architecture

```text
Robinhood (Agentic account)
        │
        ▼
Cursor agent + robinhood-delta-band-cc skill  (MCP)
        │
        ├── writes canvas/data/snapshot.json
        ├── updates #snapshot-fallback in canvas/index.html
        └── git commit + push to GitHub (main)
                │
                ▼
        Cloud Build trigger (on canvas/** changes)
                │
                ▼
        gsutil rsync canvas/ → gs://YOUR_BUCKET/
                │
                ▼
        Public HTTPS URL  →  phone / browser
              fetch("./data/snapshot.json")
```

**The website never calls Robinhood.** It only reads JSON files sitting next to `index.html` in the bucket.

---

## Phase 1 — One-time GCP setup

### 1.1 Create a project (or reuse one)

- [Google Cloud Console](https://console.cloud.google.com/) → pick project (e.g. `agentic-trading`).

### 1.2 Create a GCS bucket

```bash
export PROJECT_ID=your-project-id
export BUCKET=agentic-canvas-YOURNAME   # globally unique
export REGION=us-central1

gcloud config set project "$PROJECT_ID"

gsutil mb -p "$PROJECT_ID" -l "$REGION" "gs://${BUCKET}/"
```

### 1.3 Enable static website hosting

```bash
gsutil web set -m index.html -e index.html "gs://${BUCKET}/"
```

`index.html` as 404 page keeps hash routes (`#equities`, `#options`) working on refresh.

### 1.4 Public read access

**Option A — public bucket (simplest for “public link”)**

```bash
gsutil iam ch allUsers:objectViewer "gs://${BUCKET}"
```

**Option B — keep bucket private** and put **Cloud CDN + HTTPS load balancer** in front (custom domain, more setup). Skip unless you need private bucket + public URL via LB.

### 1.5 HTTPS URL

- Default: `https://storage.googleapis.com/${BUCKET}/index.html`
- Better: map a custom domain (Phase 5).

### 1.6 First manual deploy (smoke test)

From repo root:

```bash
./scripts/deploy-canvas-gcs.sh "$BUCKET"
```

Open the bucket website URL and confirm Scorecard loads.

---

## Phase 2 — GitHub + Cloud Build (auto deploy)

### 2.1 Push repo to GitHub

Ensure `jasebrodsky/Trading` (or your fork) has `main` with the `canvas/` folder.

### 2.2 Connect Cloud Build to GitHub

1. Console → **Cloud Build** → **Repositories** → connect GitHub repo.
2. **Triggers** → Create trigger:
   - Event: Push to branch `main`
   - Included files: `canvas/**`, `cloudbuild.yaml` (optional: only when canvas changes)
   - Configuration: Cloud Build configuration file → `cloudbuild.yaml`
   - Substitution variable: `_GCS_BUCKET` = your bucket name (e.g. `agentic-canvas-YOURNAME`)

### 2.3 Grant Cloud Build permission to write the bucket

```bash
PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')
CB_SA="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"

gsutil iam ch "serviceAccount:${CB_SA}:objectAdmin" "gs://${BUCKET}"
```

### 2.4 Verify trigger

Push a trivial change under `canvas/` → Build should run → `gsutil rsync` publishes files.

---

## Phase 3 — Agent / skill publish workflow

After every **“Refresh the strategy canvas snapshot”** (or end of daily check):

1. MCP pulls Robinhood data (Agentic `420763765` only).
2. Skill rebuilds ledger, ops, performance → writes:
   - `canvas/data/snapshot.json`
   - `canvas/data/equities.json` (if equity book refreshed)
   - `#snapshot-fallback` block in `canvas/index.html`
3. **Commit and push to `main`:**
   - `canvas/data/snapshot.json`
   - `canvas/data/equities.json` (if changed)
   - `canvas/index.html` (only if fallback block changed)
4. Cloud Build deploys → public site updates within ~1–2 minutes.

Prompt for agents:

```text
Refresh the strategy canvas snapshot and publish to GCP
```

(Skill step 7 — see `.cursor/skills/robinhood-delta-band-cc/SKILL.md`.)

### Optional — direct GCS upload (skip git for JSON only)

Only if you need **instant** JSON without waiting for Cloud Build:

- Store a deploy service account key in Cursor secrets / Cloud Agent env (never in repo).
- After writing files locally, run `scripts/deploy-canvas-gcs.sh "$BUCKET"`.

Prefer **git → Cloud Build** for audit trail and one deploy path.

---

## Phase 4 — Verify public site

| Check | Expected |
|-------|----------|
| Open `https://storage.googleapis.com/BUCKET/index.html` | Scorecard renders |
| `.../data/snapshot.json` | Raw JSON, `asOfLabel` matches last refresh |
| Reload snapshot button | Re-fetches JSON (`cache: no-store`) |
| Phone bookmark | Same URL works |
| After agent refresh + push | New numbers within ~2 min |

---

## Phase 5 — Custom domain (optional)

1. Verify domain in Google Cloud.
2. Create HTTPS load balancer → backend bucket → point DNS A/CNAME.
3. Or use **Firebase Hosting** (same `canvas/` folder, `firebase deploy`) if you prefer `firebase.json` over raw GCS website config.

---

## Files in this repo

| File | Purpose |
|------|---------|
| [`cloudbuild.yaml`](../cloudbuild.yaml) | Cloud Build: rsync `canvas/` → GCS, cache headers on JSON |
| [`scripts/deploy-canvas-gcs.sh`](../scripts/deploy-canvas-gcs.sh) | Manual deploy from laptop / agent |
| [`canvas/data/snapshot.json`](../canvas/data/snapshot.json) | Live dashboard data (committed, public when hosted) |
| [`.cursor/skills/robinhood-delta-band-cc/SKILL.md`](../.cursor/skills/robinhood-delta-band-cc/SKILL.md) | Publish step after snapshot refresh |

---

## Security notes

- **Public bucket** = anyone with the link can read account totals, positions, sleeves. Mask account id in JSON (already ••••3765 in labels).
- **Never** commit Robinhood tokens, MCP secrets, or GCS service account JSON.
- `voice-config.json` stays gitignored; ElevenLabs key is browser-only.
- Trading still runs only via MCP in Cursor — not from the public site.

---

## Rollout checklist

- [x] GCS bucket `agentic-trading-canvas` (project `hello-again-e68e6`) + website config + public read
- [x] Manual deploy smoke test — **live:** https://storage.googleapis.com/agentic-trading-canvas/index.html
- [x] Cloud Build SA `objectAdmin` on bucket
- [ ] Cloud Build trigger on `main` (connect GitHub in console — see Phase 2)
- [ ] Agent skill publishes commit after snapshot refresh
- [ ] Bookmark public URL on phone
- [ ] (Optional) Custom domain
