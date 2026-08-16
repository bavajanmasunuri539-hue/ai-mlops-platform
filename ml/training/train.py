from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn

from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

from ml.preprocessing.preprocess import (
    clean_data,
    create_train_test_split,
    load_data,
    split_features_target,
    validate_data,
)
from ml.features.feature_engineering import (
    add_features,
    build_preprocessor,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = PROJECT_ROOT / "ml" / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "churn_model.joblib"


def train_model():
    df = load_data()
    validate_data(df)

    df = clean_data(df)

    X, y = split_features_target(df)

    X = add_features(X)

    X_train, X_test, y_train, y_test = create_train_test_split(
        X,
        y,
    )

    preprocessor = build_preprocessor()

    classifier = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        random_state=42,
        class_weight="balanced",
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )

    mlflow.set_experiment("customer-churn")

    with mlflow.start_run():

        pipeline.fit(X_train, y_train)

        mlflow.log_param("model", "RandomForestClassifier")
        mlflow.log_param("n_estimators", 200)
        mlflow.log_param("max_depth", 10)

        mlflow.sklearn.log_model(
            pipeline,
            "churn-model",
        )

        joblib.dump(
            pipeline,
            MODEL_PATH,
        )

        print(f"Model saved to: {MODEL_PATH}")

    return pipeline, X_test, y_test


if __name__ == "__main__":
    train_model()