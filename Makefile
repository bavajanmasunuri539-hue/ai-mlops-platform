.PHONY: help install test lint format train tune evaluate threshold mlflow api docker-build docker-run docker-stop terraform-init terraform-fmt terraform-validate terraform-plan k8s-apply k8s-delete helm-install helm-upgrade helm-delete monitoring-up monitoring-down clean

PROJECT_NAME := ai-mlops-platform
IMAGE_NAME := customer-churn-api
IMAGE_TAG ?= latest
CONTAINER_NAME := customer-churn-api

PYTHON := python
PIP := pip

TERRAFORM_DIR := terraform/environments/dev
HELM_DIR := helm/customer-churn
K8S_DIR := kubernetes

help:
	@echo "Enterprise AI MLOps Platform"
	@echo "============================"
	@echo "make install        - Install dependencies"
	@echo "make test           - Run tests"
	@echo "make lint           - Run lint checks"
	@echo "make format         - Format Python"
	@echo "make train          - Train model"
	@echo "make tune           - Tune model"
	@echo "make evaluate       - Evaluate model"
	@echo "make threshold      - Optimize threshold"
	@echo "make mlflow         - Start MLflow"
	@echo "make api            - Start FastAPI"
	@echo "make docker-build   - Build Docker image"
	@echo "make docker-run     - Run Docker container"
	@echo "make docker-stop    - Stop Docker container"
	@echo "make terraform-init - Initialize Terraform"
	@echo "make terraform-fmt  - Format Terraform"
	@echo "make terraform-validate - Validate Terraform"
	@echo "make terraform-plan - Terraform plan"
	@echo "make k8s-apply      - Apply Kubernetes"
	@echo "make k8s-delete     - Delete Kubernetes"
	@echo "make helm-install   - Install Helm"
	@echo "make helm-upgrade   - Upgrade Helm"
	@echo "make helm-delete    - Delete Helm"
	@echo "make monitoring-up  - Start monitoring"
	@echo "make monitoring-down - Stop monitoring"
	@echo "make clean          - Clean generated files"

install:
	$(PIP) install -r requirements.txt

test:
	$(PYTHON) -m pytest -v

lint:
	$(PYTHON) -m ruff check .

format:
	$(PYTHON) -m ruff format .

train:
	$(PYTHON) -m ml.training.train_model

tune:
	$(PYTHON) -m ml.training.tune_model

evaluate:
	$(PYTHON) -m ml.training.model_comparison

threshold:
	$(PYTHON) -m ml.training.optimize_threshold

mlflow:
	mlflow server --backend-store-uri sqlite:///mlflow.db --host 0.0.0.0 --port 5000

api:
	uvicorn ml.api.app:app --host 0.0.0.0 --port 8000 --reload

docker-build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

docker-run:
	docker run -d --name $(CONTAINER_NAME) -p 8000:8000 $(IMAGE_NAME):$(IMAGE_TAG)

docker-stop:
	-docker stop $(CONTAINER_NAME)
	-docker rm $(CONTAINER_NAME)

terraform-init:
	cd $(TERRAFORM_DIR) && terraform init

terraform-fmt:
	terraform fmt -recursive

terraform-validate:
	cd $(TERRAFORM_DIR) && terraform validate

terraform-plan:
	cd $(TERRAFORM_DIR) && terraform plan

k8s-apply:
	kubectl apply -f $(K8S_DIR)/

k8s-delete:
	kubectl delete -f $(K8S_DIR)/

helm-install:
	helm install customer-churn $(HELM_DIR)

helm-upgrade:
	helm upgrade --install customer-churn $(HELM_DIR)

helm-delete:
	helm uninstall customer-churn

monitoring-up:
	kubectl apply -f monitoring/prometheus/
	kubectl apply -f monitoring/grafana/

monitoring-down:
	-kubectl delete -f monitoring/prometheus/
	-kubectl delete -f monitoring/grafana/

clean:
	-powershell -Command "Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force"
	-powershell -Command "Get-ChildItem -Recurse -File -Filter *.pyc | Remove-Item -Force"
