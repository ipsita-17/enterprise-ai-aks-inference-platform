import mlflow
import tempfile

mlflow.set_tracking_uri(
    f"file:{tempfile.gettempdir()}/mlruns"
)