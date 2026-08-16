import json
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

from ml.features.feature_engineering import (
    add_features,
    build_preprocessor,
)
from ml.preprocessing.preprocess import (
    clean_data,
    create_train_test_split,
    load_data,
    split_features_target,
    validate_data,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_DIR = PROJECT_ROOT / "ml" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "champion_model.joblib"


def main():

    # -----------------------------
    # Load and prepare data
    # -----------------------------

    df = load_data()

    validate_data(df)

    df = clean_data(df)

    X, y = split_features_target(df)

    X = add_features(X)

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = create_train_test_split(
        X,
        y,
    )

    # -----------------------------
    # Build pipeline
    # -----------------------------

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                build_preprocessor(),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=5000,
                    random_state=42,
                ),
            ),
        ]
    )

    # -----------------------------
    # Hyperparameter search
    # -----------------------------

    param_grid = {
        "classifier__C": [
            0.01,
            0.05,
            0.1,
            0.25,
            0.5,
            1.0,
            2.0,
            5.0,
            10.0,
        ],
        "classifier__class_weight": [
            None,
            "balanced",
        ],
        "classifier__solver": [
            "lbfgs",
            "liblinear",
        ],
    }

    print()
    print("=" * 60)
    print("HYPERPARAMETER TUNING")
    print("=" * 60)

    print(
        f"Parameter combinations: "
        f"{len(param_grid['classifier__C']) * 2 * 2}"
    )

    print("Cross-validation: 5-fold")
    print("Scoring metric: ROC-AUC")
    print()

    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        cv=5,
        scoring="roc_auc",
        n_jobs=-1,
        verbose=1,
        refit=True,
    )

    # -----------------------------
    # MLflow experiment
    # -----------------------------

    mlflow.set_experiment(
        "customer-churn-hyperparameter-tuning"
    )

    with mlflow.start_run(
        run_name="logistic-regression-grid-search"
    ):

        grid_search.fit(
            X_train,
            y_train,
        )

        best_model = grid_search.best_estimator_

        predictions = best_model.predict(
            X_test
        )

        probabilities = (
            best_model.predict_proba(
                X_test
            )[:, 1]
        )

        metrics = {
            "accuracy": accuracy_score(
                y_test,
                predictions,
            ),
            "precision": precision_score(
                y_test,
                predictions,
            ),
            "recall": recall_score(
                y_test,
                predictions,
            ),
            "f1": f1_score(
                y_test,
                predictions,
            ),
            "roc_auc": roc_auc_score(
                y_test,
                probabilities,
            ),
        }

        # -----------------------------
        # Display results
        # -----------------------------

        print()
        print("=" * 60)
        print("BEST HYPERPARAMETERS")
        print("=" * 60)

        print(
            grid_search.best_params_
        )

        print()
        print(
            f"Best CV ROC-AUC: "
            f"{grid_search.best_score_:.4f}"
        )

        print()
        print("=" * 60)
        print("TEST SET PERFORMANCE")
        print("=" * 60)

        for name, value in metrics.items():
            print(
                f"{name:<12}: {value:.4f}"
            )

        # -----------------------------
        # Log to MLflow
        # -----------------------------

        mlflow.log_param(
            "search_type",
            "GridSearchCV",
        )

        mlflow.log_param(
            "cv_folds",
            5,
        )

        mlflow.log_param(
            "scoring",
            "roc_auc",
        )

        for name, value in grid_search.best_params_.items():
            mlflow.log_param(
                name,
                value,
            )

        mlflow.log_metric(
            "best_cv_roc_auc",
            grid_search.best_score_,
        )

        for name, value in metrics.items():
            mlflow.log_metric(
                name,
                value,
            )

        mlflow.sklearn.log_model(
            best_model,
            name="champion-model",
        )

        # -----------------------------
        # Save champion model
        # -----------------------------

        joblib.dump(
            best_model,
            MODEL_PATH,
        )

        # Save tuning information
        tuning_results = {
            "best_parameters": grid_search.best_params_,
            "best_cv_roc_auc": grid_search.best_score_,
            "test_metrics": metrics,
        }

        results_path = (
            MODEL_DIR
            / "tuning_results.json"
        )

        with open(
            results_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                tuning_results,
                file,
                indent=4,
            )

    print()
    print("=" * 60)
    print("CHAMPION MODEL SAVED")
    print("=" * 60)

    print(
        f"Model: {MODEL_PATH}"
    )

    print(
        f"Results: {results_path}"
    )


if __name__ == "__main__":
    main()