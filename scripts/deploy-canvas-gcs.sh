#!/usr/bin/env bash
# Sync canvas/ to a GCS bucket (static site + JSON). Usage: ./scripts/deploy-canvas-gcs.sh BUCKET_NAME
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUCKET="${1:?Usage: $0 GCS_BUCKET_NAME}"

if ! command -v gsutil >/dev/null 2>&1; then
  echo "gsutil not found. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install" >&2
  exit 1
fi

echo "Syncing ${ROOT}/canvas → gs://${BUCKET}/"
# Exclude local secrets (gitignored ElevenLabs key).
# macOS: avoid gsutil -m (multiprocessing) and -c (crcmod) — old crcmod hits
# "module 'sys' has no attribute 'maxint'" on Python 3 and fails the sync.
GSUTIL_OPTS=(-o "GSUtil:parallel_process_count=1")
if [[ "$(uname -s)" == "Darwin" ]]; then
  gsutil "${GSUTIL_OPTS[@]}" rsync -r -d -x 'data/voice-config\.json$' \
    "${ROOT}/canvas/" "gs://${BUCKET}/"
else
  gsutil -m rsync -r -c -d -x 'data/voice-config\.json$' \
    "${ROOT}/canvas/" "gs://${BUCKET}/"
fi

for obj in data/snapshot.json data/equities.json; do
  if gsutil -q stat "gs://${BUCKET}/${obj}" 2>/dev/null; then
    gsutil setmeta -h "Cache-Control:no-cache, max-age=0" "gs://${BUCKET}/${obj}"
    echo "Set no-cache on ${obj}"
  fi
done

echo "Done. Site: https://storage.googleapis.com/${BUCKET}/index.html"
