# 🚀 Deployment Guide

This document describes how to deploy the Enterprise AI MLOps Platform locally, with Docker, on AWS EC2, and on Kubernetes.

---

# 1. Deployment Architecture

```text
GitHub
   │
   ▼
GitHub Actions
   │
   ▼
Docker Build
   │
   ▼
Amazon ECR
   │
   ├───────────────┐
   ▼               ▼
AWS EC2        Kubernetes
   │               │
   └───────┬───────┘
           ▼
       FastAPI API
           │
           ▼
      ML Production
         Model
```

---

# 2. Local Deployment

Create a virtual environment:

```bash
python -m venv .venv
```

Activate on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn ml.api.app:app --host 0.0.0.0 --port 8000
```

Open:

```text
http://localhost:8000/docs
```

---

# 3. Docker Deployment

Build the image:

```bash
docker build -t customer-churn-api:latest .
```

Run:

```bash
docker run --rm -p 8000:8000 customer-churn-api:latest
```

Verify:

```text
http://localhost:8000/docs
```

---

# 4. Amazon ECR

Authenticate Docker with Amazon ECR:

```bash
aws ecr get-login-password \
  --region ap-south-1 |
  docker login \
  --username AWS \
  --password-stdin \
  <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com
```

Tag the image:

```bash
docker tag customer-churn-api:latest \
  <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/customer-churn-api:latest
```

Push:

```bash
docker push \
  <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/customer-churn-api:latest
```

Never commit AWS credentials to the repository.

---

# 5. AWS EC2 Deployment

The EC2 deployment follows:

```text
Amazon ECR
     │
     ▼
EC2 Instance
     │
     ▼
Docker
     │
     ▼
Customer Churn API
```

The EC2 instance requires permissions to pull the ECR image.

Verify Docker:

```bash
docker --version
```

Authenticate with ECR:

```bash
aws ecr get-login-password \
  --region ap-south-1 |
  docker login \
  --username AWS \
  --password-stdin \
  <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com
```

Pull:

```bash
docker pull \
  <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/customer-churn-api:latest
```

Run:

```bash
docker run -d \
  --name customer-churn-api \
  -p 8000:8000 \
  <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/customer-churn-api:latest
```

---

# 6. AWS EC2 Image Builder

EC2 Image Builder is used to standardize machine-image creation.

```text
Base AMI
   ↓
Image Builder Recipe
   ↓
Components
   ↓
Image Build
   ↓
Customized AMI
   ↓
Distribution
   ↓
EC2
```

The Image Builder workflow reduces manual server configuration and provides repeatable deployment environments.

---

# 7. Kubernetes Deployment

Deploy:

```bash
kubectl apply -f kubernetes/
```

Verify:

```bash
kubectl get pods
kubectl get deployments
kubectl get services
```

Check logs:

```bash
kubectl logs -l app=customer-churn
```

---

# 8. Helm Deployment

Install or upgrade:

```bash
helm upgrade --install customer-churn \
  ./helm/customer-churn
```

Verify:

```bash
helm list
```

Check:

```bash
kubectl get pods
kubectl get services
```

---

# 9. Terraform Deployment

Navigate to the development environment:

```bash
cd terraform/environments/dev
```

Initialize:

```bash
terraform init
```

Format:

```bash
terraform fmt
```

Validate:

```bash
terraform validate
```

Plan:

```bash
terraform plan
```

Apply:

```bash
terraform apply
```

Always review the Terraform plan before applying infrastructure changes.

---

# 10. Monitoring Deployment

Install the monitoring stack:

```bash
helm upgrade --install kube-prometheus-stack \
  prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

Verify:

```bash
kubectl get pods -n monitoring
```

Check services:

```bash
kubectl get svc -n monitoring
```

---

# 11. Deployment Verification

After deployment, verify the following:

```text
API health
    ↓
Pod status
    ↓
Service status
    ↓
Container logs
    ↓
Prometheus targets
    ↓
Grafana dashboards
    ↓
Alert rules
```

FastAPI:

```text
/docs
/health
/openapi.json
```

Kubernetes:

```bash
kubectl get pods
kubectl get services
kubectl get deployments
```

Monitoring:

```bash
kubectl get pods -n monitoring
```

---

# 12. Rollback

For Kubernetes:

```bash
kubectl rollout history deployment/<deployment-name>
```

Rollback:

```bash
kubectl rollout undo deployment/<deployment-name>
```

For Helm:

```bash
helm history customer-churn
```

Rollback:

```bash
helm rollback customer-churn <REVISION>
```

---

# 13. Production Safety

Before deploying:

* Review Terraform plan.
* Verify AWS region.
* Verify ECR repository.
* Verify IAM permissions.
* Verify security groups.
* Verify container health.
* Verify Kubernetes health probes.
* Verify Prometheus targets.
* Verify Grafana dashboards.
* Verify application logs.
* Never commit secrets.
* Never expose private credentials in GitHub.

---

# 14. Final Deployment Flow

```text
Developer
   ↓
GitHub
   ↓
GitHub Actions
   ↓
Tests + SonarQube
   ↓
Docker Build
   ↓
Amazon ECR
   ↓
Kubernetes / EC2
   ↓
FastAPI
   ↓
Health Check
   ↓
Prometheus
   ↓
Grafana
   ↓
Production Monitoring
```
