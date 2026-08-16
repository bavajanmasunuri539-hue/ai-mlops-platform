import mlflow
import mlflow.sklearn
import joblib

TRACKING_URI = "sqlite:///C:/Users/bavaj/OneDrive/Desktop/ai-mlops-platform/mlflow.db"
MODEL_PATH = r"C:\Users\bavaj\OneDrive\Desktop\ai-mlops-platform\ml\models\champion_model.joblib"
RUN_ID = "7fdfae1a2c454e3d8bfd8158bc554b30"

mlflow.set_tracking_uri(TRACKING_URI)

model = joblib.load(MODEL_PATH)

with mlflow.start_run(run_id=RUN_ID):
    model_info = mlflow.sklearn.log_model(
        sk_model=model,
        name="customer_churn_model"
    )

    print("MODEL LOGGED SUCCESSFULLY")
    print("Model URI:", model_info.model_uri)

print("\nRegistering model...")

registered = mlflow.register_model(
    model_info.model_uri,
    "CustomerChurnModel"
)

print("REGISTERED MODEL")
print("Name:", registered.name)
print("Version:", registered.version)