from contextlib import contextmanager
import mlflow
from src.core.config import get_settings

def configure_mlflow() -> None:
    mlflow.set_tracking_uri(get_settings().mlflow_tracking_uri)
    mlflow.set_experiment("emakip-rag-evaluation")

@contextmanager
def tracked_run(run_name: str):
    configure_mlflow()
    with mlflow.start_run(run_name=run_name) as run:
        yield run

def log_metrics(metrics: dict[str, float]) -> None:
    mlflow.log_metrics(metrics)
