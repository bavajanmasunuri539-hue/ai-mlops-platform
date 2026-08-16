import json
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split


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

DATA_PATH = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "customer_churn.csv"
)


TARGET_COLUMN = "churn"

TEST_SIZE = 0.20
RANDOM_STATE = 42


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    print("=" * 60)
    print("LOADING PRODUCTION DATA")
    print("=" * 60)

    df = pd.read_csv(DATA_PATH)

    print(f"Dataset shape: {df.shape}")

    X = df.drop(
        columns=[TARGET_COLUMN]
    )

    y = df[TARGET_COLUMN]

    # Convert Yes/No to 1/0
    if y.dtype == "object":

        y = (
            y.astype(str)
            .str.strip()
            .str.lower()
            .map(
                {
                    "no": 0,
                    "yes": 1,
                    "0": 0,
                    "1": 1,
                }
            )
        )

    if y.isna().any():

        raise ValueError(
            "Unknown values found in target column."
        )

    y = y.astype(int)

    return X, y


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("FINAL PRODUCTION MODEL EVALUATION")
    print("=" * 60)

    # --------------------------------------------------------
    # Validate files
    # --------------------------------------------------------

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"Champion model not found:\n"
            f"{MODEL_PATH}"
        )

    if not THRESHOLD_PATH.exists():

        raise FileNotFoundError(
            f"Threshold configuration not found:\n"
            f"{THRESHOLD_PATH}"
        )

    if not DATA_PATH.exists():

        raise FileNotFoundError(
            f"Dataset not found:\n"
            f"{DATA_PATH}"
        )

    # --------------------------------------------------------
    # Load champion model
    # --------------------------------------------------------

    print("\nLoading champion model...")

    model = joblib.load(
        MODEL_PATH
    )

    print(
        f"Model: {MODEL_PATH}"
    )

    # --------------------------------------------------------
    # Load threshold
    # --------------------------------------------------------

    with open(
        THRESHOLD_PATH,
        "r",
        encoding="utf-8",
    ) as file:

        threshold_config = json.load(
            file
        )

    threshold = float(
        threshold_config[
            "optimal_threshold"
        ]
    )

    print(
        f"Production threshold: {threshold:.2f}"
    )

    # --------------------------------------------------------
    # Load data
    # --------------------------------------------------------

    X, y = load_data()

    # --------------------------------------------------------
    # Create same test split
    # --------------------------------------------------------

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    print(
        f"\nTest samples: {len(X_test)}"
    )

    # --------------------------------------------------------
    # Generate probabilities
    # --------------------------------------------------------

    probabilities = model.predict_proba(
        X_test
    )[:, 1]

    # --------------------------------------------------------
    # Apply production threshold
    # --------------------------------------------------------

    predictions = (
        probabilities >= threshold
    ).astype(int)

    # --------------------------------------------------------
    # Calculate metrics
    # --------------------------------------------------------

    metrics = {

        "accuracy": accuracy_score(
            y_test,
            predictions,
        ),

        "precision": precision_score(
            y_test,
            predictions,
            zero_division=0,
        ),

        "recall": recall_score(
            y_test,
            predictions,
            zero_division=0,
        ),

        "f1": f1_score(
            y_test,
            predictions,
            zero_division=0,
        ),

        "roc_auc": roc_auc_score(
            y_test,
            probabilities,
        ),
    }

    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("FINAL PRODUCTION METRICS")
    print("=" * 60)

    for name, value in metrics.items():

        print(
            f"{name:<12}: {value:.4f}"
        )

    # --------------------------------------------------------
    # MLflow experiment
    # --------------------------------------------------------

    mlflow.set_experiment(
        "customer-churn-production"
    )

    with mlflow.start_run(
        run_name="final-production-model"
    ):

        # ----------------------------------------------------
        # Log parameters
        # ----------------------------------------------------

        mlflow.log_param(
            "model_type",
            "LogisticRegression",
        )

        mlflow.log_param(
            "decision_threshold",
            threshold,
        )

        mlflow.log_param(
            "test_size",
            TEST_SIZE,
        )

        mlflow.log_param(
            "random_state",
            RANDOM_STATE,
        )

        mlflow.log_param(
            "optimization_metric",
            "f1",
        )

        # ----------------------------------------------------
        # Log metrics
        # ----------------------------------------------------

        for name, value in metrics.items():

            mlflow.log_metric(
                name,
                value,
            )

        # ----------------------------------------------------
        # Log threshold improvement
        # ----------------------------------------------------

        default_threshold = 0.50

        default_predictions = (
            probabilities
            >= default_threshold
        ).astype(int)

        default_f1 = f1_score(
            y_test,
            default_predictions,
            zero_division=0,
        )

        mlflow.log_metric(
            "default_threshold_f1",
            default_f1,
        )

        mlflow.log_metric(
            "f1_improvement",
            metrics["f1"] - default_f1,
        )

        # ----------------------------------------------------
        # Log model
        # ----------------------------------------------------

        mlflow.sklearn.log_model(
            model,
            name="production-model",
        )

        # ----------------------------------------------------
        # Log threshold JSON
        # ----------------------------------------------------

        mlflow.log_artifact(
            str(THRESHOLD_PATH),
            artifact_path="configuration",
        )

        # ----------------------------------------------------
        # Tags
        # ----------------------------------------------------

        mlflow.set_tag(
            "model_stage",
            "production",
        )

        mlflow.set_tag(
            "model_status",
            "champion",
        )

        mlflow.set_tag(
            "threshold_optimized",
            "true",
        )

        mlflow.set_tag(
            "project",
            "customer-churn-mlops",
        )

        run_id = mlflow.active_run().info.run_id

    # --------------------------------------------------------
    # Final output
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("PRODUCTION MODEL LOGGED TO MLFLOW")
    print("=" * 60)

    print(
        f"Experiment: "
        f"customer-churn-production"
    )

    print(
        f"Run ID: {run_id}"
    )

    print(
        f"Threshold: {threshold:.2f}"
    )

    print()
    print("Production evaluation completed successfully.")


if __name__ == "__main__":
    main()