# Customer Churn Dataset

## Project Use Case

This project uses a Customer Churn Prediction use case to demonstrate an
end-to-end MLOps lifecycle.

The model predicts whether a customer is likely to churn based on customer
and service-related attributes.

## Target Variable

`Churn`

Possible values:

- `Yes` - Customer is likely to churn
- `No` - Customer is likely to remain

## Example Features

| Feature | Description |
|---|---|
| customer_id | Unique customer identifier |
| tenure | Number of months the customer has stayed |
| monthly_charges | Customer's monthly charge |
| total_charges | Total amount charged |
| contract | Customer contract type |
| internet_service | Internet service type |
| payment_method | Payment method |
| senior_citizen | Senior citizen indicator |
| partner | Whether the customer has a partner |
| dependents | Whether the customer has dependents |

## ML Pipeline

```text
Raw Dataset
    ↓
Data Validation
    ↓
Data Cleaning
    ↓
Preprocessing
    ↓
Feature Engineering
    ↓
Model Training
    ↓
Model Evaluation
    ↓
Model Registry
    ↓
Deployment
    ↓
Monitoring