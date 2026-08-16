from pathlib import Path

import joblib
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from ml.preprocessing.preprocess import (
    clean_data,
    create_train_test_split,
    load_data,
    split_features_target,
    validate_data,
)
from ml.features.feature_engineering import add_features


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "churn_model.joblib"


def evaluate_model():
    df = load_data()
    validate_data(df)

    df = clean_data(df)

    X, y = split_features_target(df)
    X = add_features(X)

    _, X_test, _, y_test = create_train_test_split(X, y)

    model = joblib.load(MODEL_PATH)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions),
        "recall": recall_score(y_test, predictions),
        "f1": f1_score(y_test, predictions),
        "roc_auc": roc_auc_score(y_test, probabilities),
    }

    print("\nModel Metrics")
    print("=" * 40)

    for name, value in metrics.items():
        print(f"{name:10}: {value:.4f}")

    print("\nClassification Report")
    print("=" * 40)
    print(classification_report(y_test, predictions))

    return metrics


if __name__ == "__main__":
    evaluate_model()