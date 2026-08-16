"""
Decision Threshold Optimization

Optimizes the classification threshold for the champion
customer churn model.

Input:
    ml/models/champion_model.joblib
    ml/data/customer_churn.csv

Output:
    ml/models/optimal_threshold.json
"""

import json
from pathlib import Path

import joblib
import numpy as np
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
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "champion_model.joblib"
)

DATA_PATH = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "customer_churn.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "optimal_threshold.json"
)

TARGET_COLUMN = "churn"

TEST_SIZE = 0.20
RANDOM_STATE = 42


# ============================================================
# LOAD DATA
# ============================================================

def load_data():
    print("=" * 60)
    print("LOADING DATA")
    print("=" * 60)

    df = pd.read_csv(DATA_PATH)

    print(f"Dataset shape: {df.shape}")
    print(f"Target column: {TARGET_COLUMN}")

    if TARGET_COLUMN not in df.columns:
        raise ValueError(
            f"Target column '{TARGET_COLUMN}' not found.\n"
            f"Available columns: {list(df.columns)}"
        )

    X = df.drop(columns=[TARGET_COLUMN])

    y = df[TARGET_COLUMN]

    # --------------------------------------------------------
    # Convert Yes/No target labels to 1/0
    # --------------------------------------------------------

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

    # Check for unknown target values

    if y.isna().any():
        raise ValueError(
            "Unknown values found in churn target column. "
            "Expected Yes/No or 0/1."
        )

    y = y.astype(int)

    print("\nTarget distribution:")

    print(
        y.value_counts()
        .sort_index()
        .rename(
            index={
                0: "No Churn",
                1: "Churn",
            }
        )
    )

    return X, y


# ============================================================
# CREATE TEST SPLIT
# ============================================================

def create_test_split(X, y):

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test,
    )


# ============================================================
# THRESHOLD OPTIMIZATION
# ============================================================

def optimize_threshold(
    model,
    X_test,
    y_test,
):

    print("\n" + "=" * 60)
    print("DECISION THRESHOLD OPTIMIZATION")
    print("=" * 60)

    # --------------------------------------------------------
    # Generate probability predictions
    # --------------------------------------------------------

    probabilities = model.predict_proba(X_test)[:, 1]

    # ROC-AUC does not depend on classification threshold

    roc_auc = roc_auc_score(
        y_test,
        probabilities,
    )

    print(f"ROC-AUC: {roc_auc:.4f}")

    # --------------------------------------------------------
    # Test thresholds from 0.10 to 0.90
    # --------------------------------------------------------

    thresholds = np.arange(
        0.10,
        0.91,
        0.01,
    )

    results = []

    for threshold in thresholds:

        predictions = (
            probabilities >= threshold
        ).astype(int)

        accuracy = accuracy_score(
            y_test,
            predictions,
        )

        precision = precision_score(
            y_test,
            predictions,
            zero_division=0,
        )

        recall = recall_score(
            y_test,
            predictions,
            zero_division=0,
        )

        f1 = f1_score(
            y_test,
            predictions,
            zero_division=0,
        )

        results.append(
            {
                "threshold": round(
                    float(threshold),
                    2,
                ),
                "accuracy": round(
                    float(accuracy),
                    4,
                ),
                "precision": round(
                    float(precision),
                    4,
                ),
                "recall": round(
                    float(recall),
                    4,
                ),
                "f1": round(
                    float(f1),
                    4,
                ),
            }
        )

    results_df = pd.DataFrame(results)

    # --------------------------------------------------------
    # Select threshold with maximum F1
    # --------------------------------------------------------

    best_row = results_df.loc[
        results_df["f1"].idxmax()
    ]

    best_threshold = float(
        best_row["threshold"]
    )

    # --------------------------------------------------------
    # Display optimal threshold
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("OPTIMAL THRESHOLD")
    print("=" * 60)

    print(
        f"Threshold : {best_threshold:.2f}"
    )

    print(
        f"Accuracy  : {best_row['accuracy']:.4f}"
    )

    print(
        f"Precision : {best_row['precision']:.4f}"
    )

    print(
        f"Recall    : {best_row['recall']:.4f}"
    )

    print(
        f"F1        : {best_row['f1']:.4f}"
    )

    print(
        f"ROC-AUC   : {roc_auc:.4f}"
    )

    # --------------------------------------------------------
    # Display top 10 thresholds
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("TOP 10 THRESHOLDS BY F1")
    print("=" * 60)

    top_results = (
        results_df
        .sort_values(
            "f1",
            ascending=False,
        )
        .head(10)
    )

    print(
        top_results.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # Compare default 0.50 threshold
    # --------------------------------------------------------

    default_predictions = (
        probabilities >= 0.50
    ).astype(int)

    default_accuracy = accuracy_score(
        y_test,
        default_predictions,
    )

    default_precision = precision_score(
        y_test,
        default_predictions,
        zero_division=0,
    )

    default_recall = recall_score(
        y_test,
        default_predictions,
        zero_division=0,
    )

    default_f1 = f1_score(
        y_test,
        default_predictions,
        zero_division=0,
    )

    print("\n" + "=" * 60)
    print("DEFAULT THRESHOLD (0.50)")
    print("=" * 60)

    print(
        f"Accuracy  : {default_accuracy:.4f}"
    )

    print(
        f"Precision : {default_precision:.4f}"
    )

    print(
        f"Recall    : {default_recall:.4f}"
    )

    print(
        f"F1        : {default_f1:.4f}"
    )

    # --------------------------------------------------------
    # Improvement
    # --------------------------------------------------------

    f1_improvement = (
        best_row["f1"] - default_f1
    )

    print("\n" + "=" * 60)
    print("F1 IMPROVEMENT")
    print("=" * 60)

    print(
        f"Default F1 : {default_f1:.4f}"
    )

    print(
        f"Optimal F1 : {best_row['f1']:.4f}"
    )

    print(
        f"Improvement: {f1_improvement:+.4f}"
    )

    # --------------------------------------------------------
    # Save threshold configuration
    # --------------------------------------------------------

    output = {
        "model": str(MODEL_PATH),
        "target_column": TARGET_COLUMN,
        "optimization_metric": "f1",
        "optimal_threshold": best_threshold,
        "metrics": {
            "accuracy": float(
                best_row["accuracy"]
            ),
            "precision": float(
                best_row["precision"]
            ),
            "recall": float(
                best_row["recall"]
            ),
            "f1": float(
                best_row["f1"]
            ),
            "roc_auc": float(
                roc_auc
            ),
        },
        "default_threshold": {
            "threshold": 0.50,
            "accuracy": float(
                default_accuracy
            ),
            "precision": float(
                default_precision
            ),
            "recall": float(
                default_recall
            ),
            "f1": float(
                default_f1
            ),
        },
        "f1_improvement": float(
            f1_improvement
        ),
        "test_size": TEST_SIZE,
        "random_state": RANDOM_STATE,
    }

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            output,
            file,
            indent=4,
        )

    # --------------------------------------------------------
    # Final message
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("THRESHOLD CONFIGURATION SAVED")
    print("=" * 60)

    print(
        f"File: {OUTPUT_PATH}"
    )

    print(
        f"\nProduction threshold: "
        f"{best_threshold:.2f}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n" + "=" * 60)
    print(
        "CUSTOMER CHURN "
        "DECISION THRESHOLD OPTIMIZATION"
    )
    print("=" * 60)

    # --------------------------------------------------------
    # Validate model
    # --------------------------------------------------------

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"\nChampion model not found:\n"
            f"{MODEL_PATH}\n\n"
            "Run:\n"
            "python -m ml.training.tune_model"
        )

    # --------------------------------------------------------
    # Validate dataset
    # --------------------------------------------------------

    if not DATA_PATH.exists():

        raise FileNotFoundError(
            f"\nDataset not found:\n"
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
        f"Model loaded: {MODEL_PATH}"
    )

    # --------------------------------------------------------
    # Load dataset
    # --------------------------------------------------------

    X, y = load_data()

    # --------------------------------------------------------
    # Recreate test split
    # --------------------------------------------------------

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = create_test_split(
        X,
        y,
    )

    print(
        f"\nTest samples: {len(X_test)}"
    )

    # --------------------------------------------------------
    # Optimize threshold
    # --------------------------------------------------------

    optimize_threshold(
        model,
        X_test,
        y_test,
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()