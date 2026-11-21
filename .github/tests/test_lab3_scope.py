"""Exercise the actual workflow shell against real Git commits, without MLflow."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

WORKFLOW = Path(__file__).resolve().parents[1] / "workflows" / "lab3-train.yml"


def scope_script():
    lines = WORKFLOW.read_text().splitlines()
    step = lines.index("        id: changed")
    start = lines.index("        run: |", step) + 1
    script = []
    for line in lines[start:]:
        if line.strip() and not line.startswith("          "):
            break
        script.append(line[10:])
    return "\n".join(script)


class TrainingScopeTests(unittest.TestCase):
    def check_scope(self, changes, expected, event="push", invalid_base=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def git(*args):
                return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.DEVNULL).decode().strip()

            git("init", "-q")
            git("config", "user.name", "Scope test")
            git("config", "user.email", "scope@example.invalid")
            initial = {
                "lab3/README.md": "old docs\n",
                "lab3/docs/nested.md": "old nested docs\n",
                "lab3/src/train/train_mlflow.py": "original candidates\n",
                "lab3/data/churn_v1.csv": "old data\n",
                "lab3/artifacts/model.joblib": "old model\n",
            }
            for name, content in initial.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
            git("add", ".")
            git("commit", "-qm", "baseline")
            base = git("rev-parse", "HEAD")
            for name, content in changes.items():
                path = root / name
                if content is None:
                    path.unlink()
                else:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content)
            git("add", "-A")
            git("commit", "--allow-empty", "-qm", "candidate")
            output = root / "outputs"
            env = dict(os.environ, BASE_SHA="missing-ref" if invalid_base else base,
                       GITHUB_SHA=git("rev-parse", "HEAD"), EVENT_NAME=event,
                       GITHUB_OUTPUT=str(output), GITHUB_STEP_SUMMARY=str(root / "summary"))
            subprocess.run(["bash", "-e", "-c", scope_script()], cwd=root, env=env, check=True)
            self.assertEqual(output.read_text().strip(), f"retrain={str(expected).lower()}")

    def test_document_edits_and_deletions(self):
        for name in ("lab3/README.md", "lab3/docs/nested.md"):
            for content in ("updated docs\n", None):
                with self.subTest(name=name, content=content):
                    self.check_scope({name: content}, False)

    def test_model_affecting_changes(self):
        for name in ("lab3/src/train/train_mlflow.py", "lab3/data/churn_v1.csv",
                     "lab3/requirements-dev.txt", "lab3/scripts/promote.py",
                     "lab3/artifacts/model.joblib", "lab3/Dockerfile", "lab3/new-config.json"):
            with self.subTest(name=name):
                self.check_scope({name: "changed\n"}, True)

    def test_code_deletion(self):
        self.check_scope({"lab3/src/train/train_mlflow.py": None}, True)

    def test_mixed_document_and_model_change(self):
        self.check_scope({"lab3/README.md": "new docs", "lab3/data/churn_v1.csv": "new data"}, True)

    def test_document_renamed_to_execution_file(self):
        self.check_scope({"lab3/README.md": None, "lab3/config.py": "old docs\n"}, True)

    def test_other_lab_and_workflow_only(self):
        self.check_scope({"lab2/Dockerfile": "new runtime", ".github/workflows/other.yml": "test"}, False)

    def test_manual_run_forces_training(self):
        self.check_scope({}, True, event="workflow_dispatch")

    def test_unknown_base_requires_training(self):
        self.check_scope({}, True, invalid_base=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
