#!/usr/bin/env bash
# Only restore into an EMPTY tracking store, to avoid overwriting your own work.
set -euo pipefail
cd "$(dirname "$0")/.."
skip_existing="${1:-}"
[ -f evidence/mlflow-store.tar.gz ] || { echo 'No tracking backup found'; exit 1; }
docker compose -f docker-compose.mlflow.yml create mlflow
cid="$(docker compose -f docker-compose.mlflow.yml ps -aq mlflow)"
running="$(docker inspect -f '{{.State.Running}}' "$cid")"
if [ "$running" != false ]; then
  if [ "$skip_existing" = --if-empty ]; then echo "Tracking server already running; keeping its data."; exit 0; fi
  echo "Stop MLflow before restoring"; exit 1
fi
scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
# docker cp works against a stopped container. Refuse to replace an existing database.
if docker cp "$cid:/mlflow/mlflow.db" "$scratch/existing.db" 2>/dev/null; then
  if [ "$skip_existing" = --if-empty ]; then echo "Keeping existing tracking database."; exit 0; fi
  echo 'Refusing to overwrite existing MLflow DB; use a new Compose project/volume.'
  exit 1
fi
tar -xzf evidence/mlflow-store.tar.gz -C "$scratch"
docker cp "$scratch/." "$cid:/mlflow/"
docker compose -f docker-compose.mlflow.yml up -d --wait
echo 'Restored original runs, model signatures, artifacts and champion alias.'
