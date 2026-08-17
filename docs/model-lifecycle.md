# Model Lifecycle

## Enterprise AI MLOps Platform – Customer Churn Prediction

This document describes the complete lifecycle of the customer churn machine learning model, from data preparation and experimentation to model registration, deployment, monitoring, and retraining.

---

## 1. Model Lifecycle Overview

The platform follows an end-to-end MLOps lifecycle:

```text
Data
  |
  v
Data Validation
  |
  v
Preprocessing
  |
  v
Feature Engineering
  |
  v
Model Training
  |
  v
MLflow Experiment Tracking
  |
  v
Hyperparameter Tuning
  |
  v
Model Evaluation
  |
  v
Threshold Optimization
  |
  v
MLflow Model Registry
  |
  v
FastAPI Inference API
  |
  v
Docker Container
  |
  v
Kubernetes / Helm
  |
  v
Prometheus + Grafana
  |
  v
Monitoring
  |
  v
Retraining / Model Improvement