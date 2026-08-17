from pathlib import Path
import json
import joblib

import mlflow
import mlflow.sklearn
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

from ml.features.feature_engineering import add_features


PROJECT_ROOT = Path(__file__).resolve().parents[2]

THRESHOLD_PATH = PROJECT_ROOT / "ml" / "models" / "optimal_threshold.json"
MLFLOW_DB = PROJECT_ROOT / "mlflow.db"

MLFLOW_TRACKING_URI = f"sqlite:///{MLFLOW_DB.as_posix()}"

MODEL_NAME = "CustomerChurnModel"
MODEL_ALIAS = "champion"
MODEL_URI = f"models:/{MODEL_NAME}@{MODEL_ALIAS}"


app = FastAPI(
    title="Customer Churn Prediction API",
    description="Production ML API using MLflow Champion Model",
    version="1.0.0",
)

Instrumentator().instrument(app).expose(app)