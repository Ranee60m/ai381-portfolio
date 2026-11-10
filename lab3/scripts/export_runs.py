"""Portable metrics/parameters/tags export; no fabricated values."""
import json
import os
from pathlib import Path

import mlflow


def main():
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
    runs = mlflow.search_runs(experiment_names=["churn"], output_format="list")
    rows = [{
        "run_id": r.info.run_id, "status": r.info.status,
        "params": dict(r.data.params), "metrics": dict(r.data.metrics), "tags": dict(r.data.tags),
    } for r in runs]
    out = Path("evidence")
    out.mkdir(exist_ok=True)
    (out / "runs.json").write_text(json.dumps(rows, indent=2))
    mlflow.search_runs(experiment_names=["churn"]).to_csv(out / "runs.csv", index=False)
    print(f"Exported {len(rows)} actual runs to evidence/runs.json and runs.csv")


if __name__ == "__main__":
    main()
