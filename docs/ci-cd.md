# 🔄 CI/CD Documentation

## Pipeline

```text
Developer
    ↓
Git Push
    ↓
GitHub
    ↓
GitHub Actions
    ↓
┌───────────────────────┐
│ Checkout              │
│ Install Dependencies  │
│ Run Tests             │
│ SonarQube Analysis    │
│ Docker Build          │
└───────────┬───────────┘
            ↓
       Amazon ECR
            ↓
    Deployment Stage
       ┌────┴────┐
       ↓         ↓
 Kubernetes     EC2
       │         │
       └────┬────┘
            ↓
       Health Check
```

## CI Responsibilities

The CI workflow validates:

* Source code
* Python dependencies
* Unit tests
* Code quality
* Docker build
* Application configuration

## CD Responsibilities

The CD workflow handles:

* Container image delivery
* Deployment
* Environment configuration
* Health verification

## Quality Gate

SonarQube is integrated into the pipeline to provide static code analysis.

## Container Delivery

The Docker image is pushed to Amazon ECR and consumed by the deployment environment.

## Verification

After deployment, verify:

```bash
kubectl get pods
kubectl get deployments
kubectl get services
```

For the API:

```text
/health
/docs
/openapi.json
```

For monitoring:

```bash
kubectl get pods -n monitoring
```
