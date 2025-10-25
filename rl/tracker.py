"""MLflow tracking utilities."""

from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Iterator, Optional

import mlflow


class RunTracker:
    """Context manager wrapper around MLflow runs."""

    def __init__(self, experiment: str = "marl-trading") -> None:
        mlflow.set_experiment(experiment)
        self._run: Optional[mlflow.ActiveRun] = None

    @contextmanager
    def start_run(self, run_name: str | None = None) -> Iterator[mlflow.ActiveRun]:
        with mlflow.start_run(run_name=run_name) as run:
            self._run = run
            yield run
            self._run = None

    def log_params(self, params: Dict[str, float | int | str]) -> None:
        mlflow.log_params(params)

    def log_metrics(self, metrics: Dict[str, float], step: int | None = None) -> None:
        mlflow.log_metrics(metrics, step=step)

    def log_artifact(self, path: Path | str, artifact_path: str | None = None) -> None:
        mlflow.log_artifact(str(path), artifact_path=artifact_path)

    @property
    def run_id(self) -> str:
        if not self._run:
            raise RuntimeError("Run is not active")
        return self._run.info.run_id
