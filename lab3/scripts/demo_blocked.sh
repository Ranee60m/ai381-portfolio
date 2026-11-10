#!/usr/bin/env bash
# A separate weak batch; never overwrite the champion. Expected gate exit code: 1.
set -euo pipefail
cd "$(dirname "$0")/.."
export MLFLOW_TRACKING_URI="${MLFLOW_TRACKING_URI:-http://localhost:5000}"
export GIT_SHA="$(git rev-parse HEAD)"
export BATCH="weak-$(date +%s)"
WEAK_MODEL=1 python -m src.train.train_mlflow
before="$(sha256sum artifacts/champion.json artifacts/metadata.json artifacts/model.joblib)"
set +e
python scripts/promote.py
status=$?
set -e
[ "$status" -eq 1 ] || { echo "FAIL: expected blocked gate (1), got $status"; exit 1; }
[ "$before" = "$(sha256sum artifacts/champion.json artifacts/metadata.json artifacts/model.joblib)" ]
echo 'PASS: weak candidate blocked; champion artifacts unchanged.'
