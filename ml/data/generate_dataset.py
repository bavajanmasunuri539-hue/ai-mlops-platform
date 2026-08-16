from pathlib import Path

import numpy as np
import pandas as pd


RANDOM_STATE = 42
NUM_ROWS = 10000


def generate_dataset() -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_STATE)

    tenure = rng.integers(1, 73, NUM_ROWS)

    monthly_charges = rng.normal(
        70,
        25,
        NUM_ROWS,
    ).clip(20, 130)

    contract = rng.choice(
        [
            "Month-to-month",
            "One year",
            "Two year",
        ],
        NUM_ROWS,
        p=[0.55, 0.25, 0.20],
    )

    internet_service = rng.choice(
        [
            "DSL",
            "Fiber optic",
            "No",
        ],
        NUM_ROWS,
        p=[0.35, 0.50, 0.15],
    )

    payment_method = rng.choice(
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer",
            "Credit card",
        ],
        NUM_ROWS,
    )

    senior_citizen = rng.choice(
        [0, 1],
        NUM_ROWS,
        p=[0.84, 0.16],
    )

    partner = rng.choice(
        ["Yes", "No"],
        NUM_ROWS,
        p=[0.48, 0.52],
    )

    dependents = rng.choice(
        ["Yes", "No"],
        NUM_ROWS,
        p=[0.30, 0.70],
    )

    tech_support = rng.choice(
        ["Yes", "No"],
        NUM_ROWS,
        p=[0.30, 0.70],
    )

    online_security = rng.choice(
        ["Yes", "No"],
        NUM_ROWS,
        p=[0.35, 0.65],
    )

    paperless_billing = rng.choice(
        ["Yes", "No"],
        NUM_ROWS,
        p=[0.60, 0.40],
    )

    total_charges = (
        monthly_charges * tenure
        + rng.normal(0, 100, NUM_ROWS)
    ).clip(0).round(2)

    # Stronger business-driven churn signal
    churn_score = (
        1.50 * (contract == "Month-to-month")
        + 0.90 * (internet_service == "Fiber optic")
        + 0.70 * (payment_method == "Electronic check")
        + 0.70 * (monthly_charges > 85)
        + 0.45 * (senior_citizen == 1)
        + 0.40 * (paperless_billing == "Yes")
        + 0.35 * (tech_support == "No")
        + 0.35 * (online_security == "No")
        - 0.045 * tenure
        - 0.90 * (contract == "Two year")
        - 0.35 * (contract == "One year")
        - 0.30 * (dependents == "Yes")
        - 0.25 * (partner == "Yes")
    )

    noise = rng.normal(
        0,
        0.35,
        NUM_ROWS,
    )

    churn_probability = 1 / (
        1 + np.exp(
            -(churn_score + noise - 1.25)
        )
    )

    churn = np.where(
        rng.random(NUM_ROWS) < churn_probability,
        "Yes",
        "No",
    )

    return pd.DataFrame(
        {
            "customer_id": [
                f"CUST-{i:05d}"
                for i in range(1, NUM_ROWS + 1)
            ],
            "tenure": tenure,
            "monthly_charges": monthly_charges.round(2),
            "total_charges": total_charges,
            "contract": contract,
            "internet_service": internet_service,
            "payment_method": payment_method,
            "senior_citizen": senior_citizen,
            "partner": partner,
            "dependents": dependents,
            "tech_support": tech_support,
            "online_security": online_security,
            "paperless_billing": paperless_billing,
            "churn": churn,
        }
    )


def main():
    output_path = (
        Path(__file__).parent
        / "customer_churn.csv"
    )

    df = generate_dataset()

    df.to_csv(
        output_path,
        index=False,
    )

    print(
        f"Dataset created: {output_path}"
    )

    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print("\nChurn distribution:")
    print(
        df["churn"]
        .value_counts(normalize=True)
        .round(3)
    )


if __name__ == "__main__":
    main()