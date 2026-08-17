# Enterprise AI MLOps Platform — Architecture

## 1. Overview

The Enterprise AI MLOps Platform provides an end-to-end machine learning lifecycle for the Customer Churn Prediction application.

The platform integrates:

- Python machine learning
- MLflow
- FastAPI
- Docker
- Amazon ECR
- AWS EC2
- AWS EC2 Image Builder
- Kubernetes
- Helm
- Terraform
- GitHub Actions
- SonarQube
- Prometheus
- Grafana

The architecture is designed to support reproducible model development, automated deployment, scalable model serving, infrastructure automation, and production monitoring.

---

## 2. High-Level Architecture

```mermaid
flowchart TB

    DEV["Developer"]

    GIT["GitHub Repository"]

    CI["GitHub Actions CI/CD"]

    TEST["Automated Tests"]

    SONAR["SonarQube"]

    DOCKER["Docker Build"]

    ECR["Amazon ECR"]

    TF["Terraform"]

    IMAGE["AWS EC2 Image Builder"]

    AWS["AWS Infrastructure"]

    EC2["Amazon EC2"]

    K8S["Kubernetes"]

    HELM["Helm"]

    API["FastAPI Inference API"]

    MODEL["Customer Churn Production Model"]

    MLFLOW["MLflow"]

    REGISTRY["MLflow Model Registry"]

    PROM["Prometheus"]

    GRAF["Grafana"]

    ALERT["Prometheus Alert Rules"]

    CLIENT["API Client"]

    DEV --> GIT
    GIT --> CI

    CI --> TEST
    CI --> SONAR
    CI --> DOCKER

    DOCKER --> ECR

    GIT --> TF
    TF --> AWS
    TF --> IMAGE

    IMAGE --> EC2

    ECR --> EC2
    ECR --> K8S

    HELM --> K8S

    AWS --> EC2
    AWS --> K8S

    K8S --> API
    EC2 --> API

    MLFLOW --> REGISTRY
    REGISTRY --> MODEL
    MODEL --> API

    CLIENT --> API

    API --> PROM
    K8S --> PROM

    PROM --> GRAF
    PROM --> ALERT