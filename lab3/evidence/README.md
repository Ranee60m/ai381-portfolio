# Actual execution evidence

All numbers and IDs in these files come from executed commands. Local logs are not GitHub Actions runs.

- `baseline.log`: Lab 2 baseline training.
- `tests.log`, `lint.log`: verification results.
- `training.log`: the three measured candidates in batch `lab3-measured-v2`.
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

## Recorded corrections

The initial tree logging attempt failed because MLflow 3.17 uses skops and requires explicit trust for our locally trained `sklearn.tree._tree.Tree`. The training script now trusts that specific known type, not every discovered type. The unsuccessful attempt remains in `training-initial-error.log`.

`signature-check.log` verifies every finished logged model through MLflow's pyfunc flavor. Its output signature was corrected to int64 class labels to match the default `predict` flavor; the API separately calls `predict_proba`. Run tags record this correction. Scores and fitted estimators were unchanged. Future training infers the label signature directly.

The first image attempt hit this environment's HTTPS proxy certificate; the successful build used `--secret id=pip_ca,src=/etc/ssl/certs/ca-certificates.crt`. The secret is optional and is not stored in the image or project. The first deployment exhausted this small environment's disk; removing generated build cache allowed the same image to start. Original failure logs are retained alongside the successful results.

The tested image was built at `b86f82e`, and the champion trained at `b9b500e`. Later evidence/documentation commits do not retroactively change those recorded IDs. Running `scripts/run_local.sh` on the final checkout creates a new image tagged with that checkout's actual SHA.
