# 🚀 Enterprise AI MLOps Platform

An end-to-end **Enterprise AI MLOps Platform** for developing, tracking, registering, deploying, monitoring, and continuously delivering machine-learning models using modern **AWS, MLOps, DevOps, containerization, Kubernetes, Infrastructure as Code, CI/CD, and observability** practices.

The platform implements a complete **Customer Churn Prediction** lifecycle from data preprocessing and model training through MLflow model management, FastAPI inference, Docker containerization, AWS deployment, Kubernetes orchestration, automated CI/CD, and production monitoring.

---

## 📌 Project Overview

The objective of this project is to demonstrate how a machine-learning model can be transformed from an experimental model into a production-oriented service.

### End-to-end workflow

```text
Dataset
   ↓
Data Preprocessing
   ↓
Feature Engineering
   ↓
Model Training
   ↓
Hyperparameter Tuning
   ↓
Model Evaluation
   ↓
Decision Threshold Optimization
   ↓
MLflow Experiment Tracking
   ↓
MLflow Model Registry
   ↓
Production Model
   ↓
FastAPI Inference API
   ↓
Docker
   ↓
Amazon ECR
   ↓
Kubernetes / AWS EC2
   ↓
Prometheus
   ↓
Grafana
```

---

# 🏗️ Architecture

The complete architecture is available in:

**[`docs/architecture.md`](docs/architecture.md)**

### High-level architecture

```text
                         ┌──────────────────────┐
                         │      Developer       │
                         │    Git / GitHub      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   GitHub Actions     │
                         │       CI/CD          │
                         └──────────┬───────────┘
                                    │
                ┌───────────────────┼──────────────────┐
                │                   │                  │
                ▼                   ▼                  ▼
         ┌────────────┐      ┌─────────────┐    ┌────────────┐
         │   Tests    │      │  SonarQube  │    │   Docker   │
         └────────────┘      └─────────────┘    └─────┬──────┘
                                                      │
                                                      ▼
                                                ┌───────────┐
                                                │   AWS ECR │
                                                └─────┬─────┘
                                                      │
                              ┌───────────────────────┼──────────────────┐
                              │                                          │
                              ▼                                          ▼
                       ┌──────────────┐                          ┌──────────────┐
                       │ Kubernetes   │                          │   AWS EC2    │
                       │ + Helm       │                          │ + Docker     │
                       └──────┬───────┘                          └──────┬───────┘
                              │                                         │
                              └────────────────┬────────────────────────┘
                                               ▼
                                      ┌─────────────────┐
                                      │    FastAPI      │
                                      │ Inference API   │
                                      └────────┬────────┘
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │ Customer Churn  │
                                      │ Production ML   │
                                      │     Model       │
                                      └─────────────────┘

             MLflow ──► Model Registry ──► Production Alias
                                                 │
                                                 ▼
                                            FastAPI Model

             Kubernetes / API ──► Prometheus ──► Grafana
                                      │
                                      ▼
                                Alert Rules
```

---

# 🧠 Machine Learning

The project implements a **Customer Churn Prediction** use case.

## Dataset

| Item              |          Value |
| ----------------- | -------------: |
| Total records     |         10,000 |
| Training records  |          8,000 |
| Testing records   |          2,000 |
| Original features |             14 |
| Target            | Customer Churn |

## Features

```text
tenure
monthly_charges
total_charges
contract
internet_service
payment_method
senior_citizen
partner
dependents
tech_support
online_security
paperless_billing
average_monthly_spend
```

---

# 🔬 Machine Learning Pipeline

```text
Raw Dataset
     │
     ▼
Data Validation
     │
     ▼
Preprocessing
     │
     ▼
Feature Engineering
     │
     ▼
Train/Test Split
     │
     ▼
Model Training
     │
     ▼
Hyperparameter Tuning
     │
     ▼
Model Evaluation
     │
     ▼
Threshold Optimization
     │
     ▼
MLflow Tracking
     │
     ▼
Model Registry
     │
     ▼
Production Model
```

---

# 📊 Model Performance

The final production evaluation achieved:

| Metric    |     Result |
| --------- | ---------: |
| Accuracy  | **72.90%** |
| Precision | **58.69%** |
| Recall    | **73.59%** |
| F1 Score  | **65.30%** |
| ROC-AUC   | **80.38%** |

### Production decision threshold

```text
0.32
```

The decision threshold was optimized from the model's probability output to improve production churn detection.

---

# 🔧 Hyperparameter Tuning

Hyperparameter tuning is implemented using cross-validation.

```text
Parameter combinations: 36
Cross-validation: 5-fold
Optimization metric: ROC-AUC
```

Script:

```text
ml/training/tune_model.py
```

---

# 🎯 Threshold Optimization

Production classification uses an optimized threshold.

```text
Optimal threshold = 0.32
ROC-AUC = 0.8038
```

Script:

```text
ml/training/optimize_threshold.py
```

---

# 📈 MLflow

MLflow provides experiment tracking and model lifecycle management.

### MLflow capabilities

* Experiment tracking
* Parameter logging
* Metric logging
* Artifact tracking
* Model versioning
* Model Registry
* Production aliases

### Experiment

```text
customer-churn
```

### Registered production model

```text
customer-churn-production-model
```

### Model alias

```text
production
```

The inference service also supports registered model aliases such as:

```text
models:/CustomerChurnModel@champion
```

---

# 🚀 FastAPI Inference Service

The production model is exposed through a FastAPI application.

### Components

```text
FastAPI
Uvicorn
Pydantic
Joblib
MLflow
```

### Start locally

```bash
uvicorn ml.api.app:app --host 0.0.0.0 --port 8000
```

### Swagger UI

```text
http://localhost:8000/docs
```

### OpenAPI

```text
http://localhost:8000/openapi.json
```

### Health endpoint

```text
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "model_alias": "champion",
  "model_uri": "models:/CustomerChurnModel@champion",
  "decision_threshold": 0.32
}
```

---

# 🐳 Docker

The FastAPI inference service is packaged as a Docker image.

### Build

```bash
docker build -t customer-churn-api:latest .
```

### Run

```bash
docker run --rm -p 8000:8000 customer-churn-api:latest
```

### Container workflow

```text
Application
    ↓
Dockerfile
    ↓
Docker Image
    ↓
Amazon ECR
    ↓
Kubernetes / EC2
```

---

# ☁️ AWS Architecture

The platform uses AWS for cloud infrastructure and deployment.

### AWS services

* Amazon EC2
* Amazon ECR
* Amazon VPC
* IAM
* Security Groups
* Application Load Balancer
* CloudWatch
* Amazon SageMaker
* AWS EC2 Image Builder
* AWS CLI

Primary region:

```text
ap-south-1
```

---

# 🖥️ AWS EC2

The FastAPI service can be deployed to an EC2 instance.

```text
AWS EC2
   │
   ▼
Docker Container
   │
   ▼
FastAPI
   │
   ▼
Customer Churn Model
```

The EC2 instance is configured with IAM permissions to authenticate with Amazon ECR and pull application images.

---

# 🏭 AWS EC2 Image Builder

AWS EC2 Image Builder is included in the infrastructure workflow to create standardized machine images.

```text
Base AMI
   ↓
Image Builder Recipe
   ↓
Build Components
   ↓
Customized AMI
   ↓
Distribution
   ↓
EC2 Deployment
```

Benefits:

* Repeatable server configuration
* Automated image creation
* Consistent deployment environments
* Reduced manual server configuration

---

# ☸️ Kubernetes

The application supports Kubernetes-based deployment.

### Kubernetes components

* Deployment
* Service
* ConfigMap
* Secrets
* Health probes
* Resource configuration

Example:

```bash
kubectl apply -f kubernetes/
```

Check deployment:

```bash
kubectl get deployments
```

Check pods:

```bash
kubectl get pods
```

Check services:

```bash
kubectl get services
```

---

# ⛵ Helm

Helm is used for reusable and parameterized Kubernetes deployments.

Example:

```bash
helm upgrade --install customer-churn ./helm/customer-churn
```

---

# 🏗️ Terraform

Terraform provides Infrastructure as Code.

### Infrastructure components

```text
VPC
Subnets
Security Groups
IAM
EC2
ECR
ALB
EKS
RDS
EC2 Image Builder
```

Project structure:

```text
terraform/
├── environments/
│   ├── dev/
│   └── prod/
│
└── modules/
    ├── alb/
    ├── ec2/
    ├── ecr/
    ├── eks/
    ├── rds/
    └── vpc/
```

### Terraform commands

```bash
terraform fmt -recursive
terraform validate
terraform plan
terraform apply
```

---

# 🔄 GitHub Actions CI/CD

GitHub Actions automates validation, building, and deployment.

```text
Git Push
   ↓
GitHub Actions
   ↓
Checkout
   ↓
Dependency Installation
   ↓
Tests
   ↓
SonarQube Analysis
   ↓
Docker Build
   ↓
Amazon ECR
   ↓
Deployment
   ↓
Health Verification
```

---

# 🔍 SonarQube

SonarQube provides static code-quality analysis.

It helps identify:

* Bugs
* Vulnerabilities
* Code smells
* Maintainability issues
* Quality regressions

The project uses SonarQube as part of the CI pipeline.

---

# 📡 Monitoring

The platform includes production observability with:

```text
Prometheus
Grafana
Kubernetes Metrics
Application Metrics
Alert Rules
```

Architecture:

```text
Application
     ↓
Kubernetes
     ↓
Prometheus
     ↓
Grafana
```

---

# 📊 Grafana

Grafana dashboards provide visibility into:

* API activity
* Application performance
* Kubernetes resources
* Pod status
* CPU usage
* Memory usage
* Prometheus target health
* Alert status

---

# 🚨 Prometheus Alerting

Prometheus alert rules monitor operational conditions such as:

* Application availability
* Pod availability
* Resource utilization
* Target health
* Service failures

---

# 🔐 Security

Security practices include:

* IAM roles
* EC2 instance profiles
* Security groups
* ECR authentication
* Restricted network access
* Kubernetes configuration
* Secret management
* No hard-coded AWS credentials
* Container isolation

---

# 📁 Repository Structure

```text
ai-mlops-platform/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── cd.yml
│       └── destroy.yml
│
├── ml/
│   ├── api/
│   │   └── app.py
│   │
│   ├── training/
│   │   ├── train_model.py
│   │   ├── tune_model.py
│   │   ├── model_comparison.py
│   │   └── optimize_threshold.py
│   │
│   ├── inference/
│   │   └── predict.py
│   │
│   └── models/
│       └── churn_model.joblib
│
├── kubernetes/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── config/
│
├── helm/
│   └── customer-churn/
│
├── terraform/
│   ├── environments/
│   │   ├── dev/
│   │   └── prod/
│   │
│   └── modules/
│       ├── alb/
│       ├── ec2/
│       ├── ecr/
│       ├── eks/
│       ├── rds/
│       └── vpc/
│
├── monitoring/
│   ├── prometheus/
│   └── grafana/
│
├── tests/
│
├── docs/
│   └── architecture.md
│
├── Makefile
├── Dockerfile
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🛠️ Local Setup

## Clone

```bash
git clone https://github.com/bavajanmasunuri539-hue/ai-mlops-platform.git

cd ai-mlops-platform
```

## Create virtual environment

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🧪 Testing

Run all tests:

```bash
pytest -v
```

Or:

```bash
make test
```

---

# 🧠 Train Model

```bash
python -m ml.training.train_model
```

or:

```bash
make train
```

---

# 🔬 Tune Model

```bash
python -m ml.training.tune_model
```

or:

```bash
make tune
```

---

# 🎯 Optimize Threshold

```bash
python -m ml.training.optimize_threshold
```

or:

```bash
make threshold
```

---

# 📊 Evaluate Model

```bash
python -m ml.training.model_comparison
```

or:

```bash
make evaluate
```

---

# 📈 Start MLflow

```bash
mlflow ui \
  --backend-store-uri sqlite:///mlflow.db \
  --host 0.0.0.0 \
  --port 5000
```

or:

```bash
make mlflow
```

---

# 🚀 Start API

```bash
uvicorn ml.api.app:app \
  --host 0.0.0.0 \
  --port 8000
```

or:

```bash
make api
```

---

# 🐳 Docker

```bash
make docker-build
make docker-run
```

---

# ☸️ Kubernetes

```bash
make k8s-deploy
make k8s-status
```

---

# ⛵ Helm

```bash
make helm-install
```

---

# 🏗️ Terraform

```bash
make terraform-init
make terraform-fmt
make terraform-validate
make terraform-plan
```

Apply only after reviewing the plan:

```bash
make terraform-apply
```

---

# 📊 Monitoring

Install the Prometheus/Grafana stack:

```bash
make monitoring-install
```

Check monitoring components:

```bash
make monitoring-status
```

---

# 🧰 Makefile

The repository includes a Makefile to standardize common development and deployment commands.

Examples:

```bash
make help
make install
make test
make train
make tune
make threshold
make evaluate
make api
make docker-build
make docker-run
make k8s-deploy
make helm-install
make terraform-validate
make terraform-plan
```

See [`Makefile`](Makefile) for the complete command set.

---

# 📋 Production Readiness

| Area                   | Implementation |
| ---------------------- | -------------- |
| ML Training            | ✅              |
| Hyperparameter Tuning  | ✅              |
| Model Evaluation       | ✅              |
| Threshold Optimization | ✅              |
| MLflow Tracking        | ✅              |
| Model Registry         | ✅              |
| Production Model Alias | ✅              |
| FastAPI Serving        | ✅              |
| Docker                 | ✅              |
| Amazon ECR             | ✅              |
| AWS EC2                | ✅              |
| EC2 Image Builder      | ✅              |
| Kubernetes             | ✅              |
| Helm                   | ✅              |
| Terraform              | ✅              |
| GitHub Actions         | ✅              |
| SonarQube              | ✅              |
| Prometheus             | ✅              |
| Grafana                | ✅              |
| Alerting               | ✅              |
| Health Checks          | ✅              |

---

# 🏆 Key Achievements

* Built an end-to-end enterprise-style MLOps platform.
* Implemented complete ML training and evaluation workflow.
* Performed 5-fold hyperparameter tuning across 36 parameter combinations.
* Optimized the production decision threshold to **0.32**.
* Achieved **0.8038 ROC-AUC**.
* Implemented MLflow experiment tracking.
* Implemented MLflow Model Registry and production aliases.
* Developed a FastAPI production inference service.
* Containerized the service with Docker.
* Integrated Amazon ECR.
* Implemented AWS infrastructure using Terraform.
* Included AWS EC2 Image Builder.
* Deployed workloads using Kubernetes and Helm.
* Implemented GitHub Actions CI/CD.
* Integrated SonarQube code-quality analysis.
* Implemented Prometheus monitoring.
* Built Grafana dashboards.
* Implemented Prometheus alert rules.
* Added production health checks and observability.

---

# 💼 Resume Project Description

**Enterprise AI MLOps Platform | AWS, Python, MLflow, Docker, Kubernetes, Terraform, GitHub Actions**

Developed an end-to-end Customer Churn MLOps platform automating model training, hyperparameter tuning, MLflow experiment tracking, model registry, FastAPI inference, Docker containerization, AWS ECR/EC2 deployment, Kubernetes orchestration, Prometheus/Grafana monitoring, and CI/CD. Implemented Terraform-based AWS infrastructure, EC2 Image Builder, SonarQube quality analysis, and production decision-threshold optimization, achieving **0.8038 ROC-AUC**.

---

# 👨‍💻 Author

**Masunuri Bavajan**

DevOps & Cloud Engineer
AWS | Kubernetes | Terraform | Docker | CI/CD | MLOps

GitHub:

https://github.com/bavajanmasunuri539-hue

---

# ⭐ Final Architecture

The project combines:

```text
             MACHINE LEARNING
                    │
                    ▼
          ┌──────────────────┐
          │      MLflow      │
          │ Tracking/Registry│
          └────────┬─────────┘
                   │
                   ▼
             Production Model
                   │
                   ▼
              FastAPI API
                   │
                   ▼
                Docker
                   │
          ┌────────┴────────┐
          ▼                 ▼
     AWS ECR           Kubernetes
          │                 │
          ▼                 ▼
        EC2              Helm
          │                 │
          └────────┬────────┘
                   ▼
              Monitoring
                   │
            ┌──────┴──────┐
            ▼             ▼
       Prometheus      Grafana

Infrastructure:
Terraform + AWS EC2 Image Builder

Delivery:
GitHub Actions + SonarQube
```

This architecture represents the complete production-oriented MLOps lifecycle from **model development → registry → serving → containerization → cloud deployment → CI/CD → monitoring → alerting**.



FINAL MANUAL DEMO URLs

1. FastAPI Swagger
http://127.0.0.1:8000/docs

2. FastAPI ReDoc
http://127.0.0.1:8000/redoc

3. MLflow
http://127.0.0.1:5000

4. Prometheus
http://127.0.0.1:9090

5. Grafana
http://127.0.0.1:3000

6. GitHub Repository
https://github.com/bavajanmasunuri539-hue/ai-mlops-platform



Swagger
  ↓
ReDoc
  ↓
MLflow
  ↓
Prometheus
  ↓
Grafana
  ↓
GitHub