from pathlib import Path
import json

import joblib
import pandas as pd

from ml.features.feature_engineering import add_features


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "champion_model.joblib"
)

THRESHOLD_PATH = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "optimal_threshold.json"
)


# ============================================================
# LOAD MODEL
# ============================================================

def load_model():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Champion model not found: {MODEL_PATH}. "
            "Run tune_model.py first."
        )

    return joblib.load(MODEL_PATH)


# ============================================================
# LOAD OPTIMAL THRESHOLD
# ============================================================

def load_threshold():

    if not THRESHOLD_PATH.exists():
        raise FileNotFoundError(
            f"Threshold configuration not found: "
            f"{THRESHOLD_PATH}. "
            "Run optimize_threshold.py first."
        )

    with open(
        THRESHOLD_PATH,
        "r",
        encoding="utf-8",
    ) as file:

        config = json.load(file)

    threshold = float(
        config["optimal_threshold"]
    )

    return threshold


# ============================================================
# PREDICTION
# ============================================================

def predict(customer: dict) -> dict:

    model = load_model()

    threshold = load_threshold()

    # Convert customer dictionary to DataFrame
    df = pd.DataFrame([customer])

    # Apply project feature engineering
    df = add_features(df)

    # Get churn probability
    probability = model.predict_proba(df)[0][1]

    # Apply optimized production threshold
    prediction = int(
        probability >= threshold
    )

    return {
        "churn_prediction": (
            "Yes"
            if prediction == 1
            else "No"
        ),
        "churn_probability": round(
            float(probability),
            4,
        ),
        "decision_threshold": threshold,
    }


# ============================================================
# TEST / CLI
# ============================================================

if __name__ == "__main__":

    customer = {
        "tenure": 8,
        "monthly_charges": 95.50,
        "total_charges": 764.00,
        "contract": "Month-to-month",
        "internet_service": "Fiber optic",
        "payment_method": "Electronic check",
        "senior_citizen": 0,
        "partner": "No",
        "dependents": "No",
    }

    result = predict(customer)

    print("\n" + "=" * 50)
    print("CUSTOMER CHURN PREDICTION")
    print("=" * 50)

    print(
        f"Prediction          : "
        f"{result['churn_prediction']}"
    )

    print(
        f"Churn Probability   : "
        f"{result['churn_probability']}"
    )

    print(
        f"Decision Threshold  : "
        f"{result['decision_threshold']}"
    )

    print("=" * 50)