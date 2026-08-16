from pathlib import Path

import joblib
import json
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ml.features.feature_engineering import add_features


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "champion_model.joblib"
THRESHOLD_PATH = PROJECT_ROOT / "ml" / "models" / "optimal_threshold.json"


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "customer-churn-production-model"
MODEL_ALIAS = "production"


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Production ML API for customer churn prediction",
    version="1.0.0",
)


# ============================================================
# LOAD PRODUCTION MODEL
# ============================================================

def load_production_model():

    print()
    print("=" * 60)
    print("LOADING PRODUCTION MODEL")
    print("=" * 60)

    print(f"Model: {MODEL_NAME}")
    print(f"Alias: {MODEL_ALIAS}")

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Production model not found: {MODEL_PATH}"
        )

    if not THRESHOLD_PATH.exists():
        raise FileNotFoundError(
            f"Threshold configuration not found: {THRESHOLD_PATH}"
        )

    model = joblib.load(MODEL_PATH)

    with open(
        THRESHOLD_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        threshold_config = json.load(file)

    threshold = float(
        threshold_config["production_threshold"]
    )

    print(f"Model file: {MODEL_PATH}")
    print(f"Threshold: {threshold}")
    print("Production model loaded successfully.")
    print("=" * 60)

    return model, threshold


model, DECISION_THRESHOLD = load_production_model()


# ============================================================
# REQUEST SCHEMA
# ============================================================

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


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "alias": MODEL_ALIAS,
        "threshold": DECISION_THRESHOLD,
    }


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "Customer Churn Prediction API",
        "status": "running",
        "model": MODEL_NAME,
        "alias": MODEL_ALIAS,
        "threshold": DECISION_THRESHOLD,
    }


# ============================================================
# PREDICTION
# ============================================================

@app.post("/predict")
def predict(customer: CustomerRequest):

    try:

        customer_data = customer.model_dump()

        df = pd.DataFrame(
            [customer_data]
        )

        # Feature engineering
        df = add_features(df)

        # Probability
        probability = float(
            model.predict_proba(df)[0][1]
        )

        # Production decision threshold
        prediction = (
            probability >= DECISION_THRESHOLD
        )

        return {
            "churn_prediction": (
                "Yes"
                if prediction
                else "No"
            ),
            "churn_probability": round(
                probability,
                4,
            ),
            "decision_threshold": DECISION_THRESHOLD,
            "model": MODEL_NAME,
            "model_alias": MODEL_ALIAS,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# LOCAL DEVELOPMENT
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "ml.api.app:app",
        host="0.0.0.0",
        port=8000,
    )