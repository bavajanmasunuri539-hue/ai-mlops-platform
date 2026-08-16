import mlflow
import mlflow.sklearn

from sklearn.ensemble import (
    GradientBoostingClassifier,
    HistGradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
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


def evaluate_model(
    name,
    model,
    X_train,
    X_test,
    y_train,
    y_test,
):

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                build_preprocessor(),
            ),
            (
                "classifier",
                model,
            ),
        ]
    )

    pipeline.fit(
        X_train,
        y_train,
    )

    predictions = pipeline.predict(
        X_test
    )

    probabilities = pipeline.predict_proba(
        X_test
    )[:, 1]

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

    print()
    print(name)
    print("=" * 40)

    for metric, value in metrics.items():
        print(
            f"{metric:<10}: {value:.4f}"
        )

    with mlflow.start_run(
        run_name=name
    ):

        mlflow.log_param(
            "model",
            name,
        )

        for metric, value in metrics.items():
            mlflow.log_metric(
                metric,
                value,
            )

        mlflow.sklearn.log_model(
            pipeline,
            name="model",
        )

    return pipeline, metrics


def main():

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

    models = {
        "LogisticRegression": LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            random_state=42,
        ),

        "RandomForest": RandomForestClassifier(
            n_estimators=400,
            max_depth=12,
            min_samples_split=5,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ),

        "GradientBoosting": GradientBoostingClassifier(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=3,
            random_state=42,
        ),

        "HistGradientBoosting": HistGradientBoostingClassifier(
            max_iter=300,
            learning_rate=0.05,
            max_leaf_nodes=31,
            random_state=42,
        ),
    }

    mlflow.set_experiment(
        "customer-churn-model-comparison"
    )

    results = []

    for name, model in models.items():

        pipeline, metrics = evaluate_model(
            name,
            model,
            X_train,
            X_test,
            y_train,
            y_test,
        )

        results.append(
            {
                "model": name,
                **metrics,
            }
        )

    print()
    print("=" * 70)
    print("MODEL COMPARISON")
    print("=" * 70)

    results = sorted(
        results,
        key=lambda x: x["roc_auc"],
        reverse=True,
    )

    for result in results:

        print(
            f"{result['model']:<25}"
            f"ROC-AUC={result['roc_auc']:.4f} "
            f"F1={result['f1']:.4f}"
        )


if __name__ == "__main__":
    main()