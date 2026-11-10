# AI381 Lab 3 — Tracked, Gated and Shipped (local Docker)

Completed from the supplied Lab 3 starter. Local deployment is used, as permitted by the updated assignment and confirmed by the student. Azure is not required.

## Start on your machine

Requirements: Python 3.12, Git, Docker Engine/Desktop with Compose, Bash (WSL2 on Windows). Run from this folder. Preserve the included Git repository so commit-based lineage works.

```bash
bash scripts/run_local.sh
```

This installs pinned dependencies, starts persistent MLflow, uses the exported champion (or trains/promotes if absent), runs lint/tests, builds a commit-tagged image, deploys with Compose and checks the API. It does not silently replace a champion with an inferior candidate.

- MLflow: http://localhost:5000
- API and health: http://localhost:8000/health
- Interactive API: http://localhost:8000/docs

The included MLflow export can be restored before starting MLflow; see `evidence/README.md`. This makes the original run IDs in the model metadata visible on a new laptop.

## Retrain and inspect the gate

```bash
source .venv/bin/activate
export MLFLOW_TRACKING_URI=http://localhost:5000
export GIT_SHA=$(git rev-parse HEAD)
export BATCH="candidate-$(date +%s)"
python -m src.train.train_mlflow
python scripts/promote.py
```

The gate requires a **finished** run, p95 <= 30 ms, and at least **0.01 absolute F1** improvement over the committed champion. With no champion the best eligible candidate is promoted. An equal model is blocked too; a red result on unchanged candidates is intentional. Metrics use the same deterministic holdout, not a new random split each time. Retuning repeatedly on this holdout risks overfitting.

```bash
bash scripts/demo_blocked.sh
```

This trains the deliberately weak C=0.00001 logistic model in a separate batch. The gate returns 1 and champion files must remain byte-for-byte unchanged. This local evidence does not replace the required red GitHub Actions run.

## GitHub demonstration

The provided repository has a `lab3` implementation branch and a `worse-model` branch for the failed PR demonstration. See `GITHUB_SETUP_AR.md` for the exact sequence. The training workflow compares against the **base branch** champion, trains in a fresh MLflow server, and blocks inferior models. After a successful main-branch gate it builds and smoke-tests the exported model. The independent CI workflow runs lint and tests; it cannot ship an ungated image.

## Trace the running model

```bash
curl -fsS http://localhost:8000/health
 git rev-parse --short HEAD
 docker images churn-api
```

`model_version` is the image build commit (first seven characters); `mlflow_run_id` identifies the actual training run. If rebuilding a previously trained champion at a newer commit, these commits can differ: open the run's `git_sha` tag for the training commit. The image commit still traces to its committed champion metadata. Both are recorded in the evidence.

`restart: unless-stopped` restarts a crashed process unless explicitly stopped. Docker HEALTHCHECK marks a hung service unhealthy; Compose alone does **not** restart a merely unhealthy process. The named MLflow volume persists tracking data across `down`/`up`.

```bash
docker compose -f docker-compose.deploy.yml down
docker compose -f docker-compose.mlflow.yml down
# Do not add -v unless you intend to erase the tracking volume.
```

## Submission

Read `MODEL_SELECTION.md`, `STATUS_AR.md`, `VIDEO_GUIDE_AR.md`, and `evidence/README.md`. Record your own 5–8 minute video with your face, voice and identity checkpoint. Upload the video and a real `repo.txt` repository URL to Teams. No identity, GitHub link, cloud deployment or submitted video is fabricated in this package.

The Lab 3 Dockerfile deliberately fails when no promoted artifact exists. It cannot silently train a different Lab 2 model during image creation. Run the tracking/training/promotion steps before the first build.
