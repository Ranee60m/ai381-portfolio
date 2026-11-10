#!/usr/bin/env bash
# Run from the repository root in Linux, macOS or WSL2.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
export MLFLOW_TRACKING_URI=http://localhost:5000
export GIT_SHA="$(git rev-parse HEAD)"
if [ -f evidence/mlflow-store.tar.gz ]; then
  bash scripts/restore_mlflow.sh --if-empty
fi
docker compose -f docker-compose.mlflow.yml up -d --wait
if [ ! -f artifacts/model.joblib ]; then
  export BATCH="bootstrap-$(date +%s)"
  python -m src.train.train_mlflow
  python scripts/promote.py
fi
ruff check .
pytest -q
SHORT_SHA="${GIT_SHA:0:7}"
docker build --build-arg GIT_SHA="$GIT_SHA" -t "churn-api:$SHORT_SHA" -t churn-api:local .
IMAGE="churn-api:$SHORT_SHA" docker compose -f docker-compose.deploy.yml up -d --wait
bash scripts/smoke_test.sh http://localhost:8000
curl -fsS http://localhost:8000/health
printf '\nAPI: http://localhost:8000/docs\nMLflow: http://localhost:5000\n'
