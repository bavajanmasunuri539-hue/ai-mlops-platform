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

# Prometheus application metrics
Instrumentator().instrument(app).expose(app)


class CustomerRequest(BaseModel):
    tenure: int
    monthly_charges: float
    total_charges: float
    contract: str
    internet_service: str
    payment_method: str
    senior_citizen: int
    partner: str
    dependents: str


def load_production_model():
    print()
    print("=" * 60)
    print("LOADING CHAMPION MODEL FROM MLFLOW")
    print("=" * 60)

    print(f"Model: {MODEL_NAME}")
    print(f"Alias: {MODEL_ALIAS}")
    print(f"Model URI: {MODEL_URI}")

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    try:
        model = joblib.load(
            PROJECT_ROOT / "ml" / "models" / "champion_model.joblib"
        )
    except Exception as exc:
        raise RuntimeError(
            f"Unable to load MLflow model {MODEL_URI}: {exc}"
        )

    if not THRESHOLD_PATH.exists():
        raise FileNotFoundError(
            f"Threshold configuration not found: {THRESHOLD_PATH}"
        )

    with open(THRESHOLD_PATH, "r", encoding="utf-8") as file:
        threshold_config = json.load(file)

    threshold = float(threshold_config["optimal_threshold"])

    print(f"Threshold: {threshold}")
    print("Champion model loaded successfully.")
    print("=" * 60)

    return model, threshold


model, DECISION_THRESHOLD = load_production_model()


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "alias": MODEL_ALIAS,
        "threshold": DECISION_THRESHOLD,
        "mlflow_tracking_uri": MLFLOW_TRACKING_URI,
    }


@app.get("/")
def root():
    return {
        "message": "Customer Churn Prediction API",
        "status": "running",
        "model": MODEL_NAME,
        "model_alias": MODEL_ALIAS,
        "model_uri": MODEL_URI,
        "decision_threshold": DECISION_THRESHOLD,
    }


@app.post("/predict")
def predict(customer: CustomerRequest):
    try:
        customer_data = customer.model_dump()

        df = pd.DataFrame([customer_data])

        df = add_features(df)

        probability = float(
            model.predict_proba(df)[0][1]
        )

        prediction = probability >= DECISION_THRESHOLD

        return {
            "churn_prediction": "Yes" if prediction else "No",
            "churn_probability": round(probability, 4),
            "decision_threshold": DECISION_THRESHOLD,
            "model": MODEL_NAME,
            "model_alias": MODEL_ALIAS,
            "model_uri": MODEL_URI,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "ml.api.app:app",
        host="0.0.0.0",
        port=8000,
    )