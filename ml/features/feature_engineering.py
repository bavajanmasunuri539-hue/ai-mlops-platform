import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


NUMERIC_FEATURES = [
    "tenure",
    "monthly_charges",
    "total_charges",
    "senior_citizen",
]

CATEGORICAL_FEATURES = [
    "contract",
    "internet_service",
    "payment_method",
    "partner",
    "dependents",
]


def build_preprocessor() -> ColumnTransformer:
    numeric_transformer = StandardScaler()

    categorical_transformer = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False,
    )

    return ColumnTransformer(
        transformers=[
            (
                "numeric",
                numeric_transformer,
                NUMERIC_FEATURES,
            ),
            (
                "categorical",
                categorical_transformer,
                CATEGORICAL_FEATURES,
            ),
        ]
    )


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["average_monthly_spend"] = (
        df["total_charges"] / df["tenure"].clip(lower=1)
    )

    return df