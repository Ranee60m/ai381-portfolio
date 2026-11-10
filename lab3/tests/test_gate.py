"""Gate boundary tests; no server or training needed."""
from types import SimpleNamespace

import pytest

from scripts import promote


def run(f1, latency, status="FINISHED"):
    return SimpleNamespace(
        info=SimpleNamespace(run_id="run-1", status=status),
        data=SimpleNamespace(
            metrics={"f1": f1, "auc": 0.8, "p95_latency_ms": latency},
            params={"model": "candidate", "data_sha256": "hash"},
            tags={"model_uri": "models:/fake"},
        ),
    )


def test_slow_and_failed_candidates_cannot_win(monkeypatch):
    monkeypatch.setattr(promote.mlflow, "search_runs", lambda **kw: [
        run(0.99, promote.LATENCY_BUDGET_MS + 1),
        run(0.95, 1, "FAILED"), run(0.7, promote.LATENCY_BUDGET_MS),
    ])
    assert promote.best_candidate("test")["f1"] == 0.7


def test_all_slow_candidates_block(monkeypatch):
    monkeypatch.setattr(promote.mlflow, "search_runs", lambda **kw: [run(0.99, 999)])
    with pytest.raises(SystemExit, match="BLOCKED"):
        promote.best_candidate("test")


@pytest.mark.parametrize("gain,expected", [(0.0099, 1), (0.01, 0), (-0.1, 1)])
def test_gain_boundary(monkeypatch, gain, expected):
    monkeypatch.setattr("sys.argv", ["promote.py"])
    monkeypatch.setattr(promote.mlflow, "set_tracking_uri", lambda uri: None)
    monkeypatch.setattr(promote, "best_candidate", lambda batch: {
        "model": "new", "f1": 0.7 + gain, "p95_latency_ms": 2,
    })
    monkeypatch.setattr(promote, "current_champion", lambda path: {
        "model": "old", "f1": 0.7, "p95_latency_ms": 2,
    })
    promoted = []
    monkeypatch.setattr(promote, "promote", promoted.append)
    assert promote.main() == expected
    assert bool(promoted) == (expected == 0)
