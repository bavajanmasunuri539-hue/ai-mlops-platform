from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


TARGET_COLUMN = "churn"
DROP_COLUMNS = ["customer_id"]

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "ml" / "data" / "customer_churn.csv"


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("Dataset is empty.")

    return df


def validate_data(df: pd.DataFrame) -> None:
    required_columns = {
        "customer_id",
        "tenure",
        "monthly_charges",
        "total_charges",
        "contract",
        "internet_service",
        "payment_method",
        "senior_citizen",
        "partner",
        "dependents",
        "churn",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    if df[TARGET_COLUMN].isna().any():
        raise ValueError("Target column contains missing values.")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df.drop_duplicates()

    numeric_columns = [
        "tenure",
        "monthly_charges",
        "total_charges",
        "senior_citizen",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna()

    return df


def split_features_target(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    X = df.drop(columns=[TARGET_COLUMN] + DROP_COLUMNS)
    y = df[TARGET_COLUMN].map({"No": 0, "Yes": 1})

    if y.isna().any():
        raise ValueError("Unexpected target values found.")

    return X, y


def create_train_test_split(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42,
):
    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )


if __name__ == "__main__":
    df = load_data()
    validate_data(df)

    df = clean_data(df)
    X, y = split_features_target(df)

    X_train, X_test, y_train, y_test = create_train_test_split(X, y)

    print(f"Dataset shape: {df.shape}")
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    print(f"Features: {list(X.columns)}")