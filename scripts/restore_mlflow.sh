#!/usr/bin/env bash
# Only restore into an EMPTY tracking store, to avoid overwriting your own work.
set -euo pipefail
cd "$(dirname "$0")/.."
[ -f evidence/mlflow-store.tar.gz ] || { echo 'No tracking backup found'; exit 1; }
docker compose -f docker-compose.mlflow.yml create mlflow
cid="$(docker compose -f docker-compose.mlflow.yml ps -aq mlflow)"
running="$(docker inspect -f '{{.State.Running}}' "$cid")"
[ "$running" = false ] || { echo 'Stop MLflow before restoring'; exit 1; }
# docker cp works against a stopped container. Refuse to replace an existing database.
if docker cp "$cid:/mlflow/mlflow.db" /tmp/ai381-existing-mlflow.db 2>/dev/null; then
  rm -f /tmp/ai381-existing-mlflow.db
  echo 'Refusing to overwrite existing MLflow DB; use a new Compose project/volume.'
  exit 1
fi
scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
tar -xzf evidence/mlflow-store.tar.gz -C "$scratch"
docker cp "$scratch/." "$cid:/mlflow/"
docker compose -f docker-compose.mlflow.yml up -d --wait
echo 'Restored original runs, model signatures, artifacts and champion alias.'
