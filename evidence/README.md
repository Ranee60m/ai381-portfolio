# Actual execution evidence

All numbers and IDs in these files come from executed commands. Local logs are not GitHub Actions runs.

- `baseline.log`: Lab 2 baseline training.
- `tests.log`, `lint.log`: verification results.
- `training.log`: the three measured candidates in batch `lab3-measured`.
- `promotion.log`: first champion registration and alias assignment.
- `blocked.log`: deliberately weak model, exit 1, with unchanged champion exports.
- `runs.json`, `runs.csv`: MLflow parameters, metrics, tags and run IDs.
- `MLmodel`: selected model's logged signature/flavors.
- `build.log`, `smoke.log`, `lineage.json`, `compose-ps.txt`: real Docker deployment evidence.
- `mlflow-store.tar.gz`: consistent database and artifact export from the stopped MLflow container, including registry alias and original runs. Keep this private if later runs contain sensitive data.

## Restore the original MLflow UI on a new machine

Before the first `run_local.sh`, with Docker running:

```bash
bash scripts/restore_mlflow.sh
```

This refuses to overwrite an existing database or a running server. Run the project in its own folder/Compose project so it gets a new empty volume. Then run `bash scripts/run_local.sh`. Open http://localhost:5000; use the run ID from /health to inspect its data hash, signature, model and training commit. MLflow models in version 3 can appear under the run's **Models** section as well as the model artifact page.

To reuse your own existing store, skip restore and retrain with a fresh BATCH; the supplied CSV/JSON remain viewable without MLflow. Do not claim that an old run is present in a fresh empty server.

Latency was measured as 200 sequential one-row predict_proba calls after warmup inside this shared Linux environment. It excludes HTTP/network time; expect different values on your laptop or a GitHub runner. No production latency guarantee is inferred.
