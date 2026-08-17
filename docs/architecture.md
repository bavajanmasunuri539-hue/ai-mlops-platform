                    ENTERPRISE AI MLOps PLATFORM
             Customer Churn Prediction — End-to-End


┌─────────────────────────────────────────────────────────────────────┐
│                    1. DEVELOPER & SOURCE CONTROL                    │
│                                                                     │
│   👨‍💻 Developer                                                     │
│       │                                                             │
│       ▼                                                             │
│   GitHub Repository                                                 │
│   ├── Application Code                                              │
│   ├── ML Code                                                       │
│   ├── Dockerfile                                                    │
│   ├── Kubernetes Manifests                                         │
│   ├── Terraform                                                     │
│   └── GitHub Actions Workflows                                      │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         2. SECURITY                                 │
│                                                                     │
│   GitHub Secrets ──► AWS Credentials / Tokens                       │
│                                                                     │
│   AWS IAM                                                          │
│   ├── Least-Privilege Access                                        │
│   ├── EC2 IAM Role                                                  │
│   └── ECR Access                                                    │
│                                                                     │
│   AWS Security Groups                                               │
│   ├── Controlled Network Access                                     │
│   └── Application Ports                                             │
│                                                                     │
│   🔐 Secrets / Credentials never committed to Git                   │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
╔═════════════════════════════════════════════════════════════════════╗
║                         3. CI/CD PIPELINE                          ║
║                                                                     ║
║  GitHub Actions                                                    ║
║       │                                                             ║
║       ├── Checkout                                                  ║
║       ├── Dependency Installation                                   ║
║       ├── Automated Tests                                           ║
║       ├── Code Quality / SonarQube                                  ║
║       ├── Docker Build                                              ║
║       │                                                             ║
║       ▼                                                             ║
║  Amazon ECR                                                        ║
║  Container Registry                                                 ║
║       │                                                             ║
║       ▼                                                             ║
║  Kubernetes Deployment                                              ║
╚══════════════════════════════┬══════════════════════════════════════╝
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       4. AWS INFRASTRUCTURE                         │
│                                                                     │
│                         Terraform                                   │
│                            │                                        │
│          ┌─────────────────┼──────────────────┐                     │
│          ▼                 ▼                  ▼                     │
│        AWS VPC            IAM          Security Groups              │
│          │                                                          │
│          ├── Network / Subnets                                      │
│          ├── EC2                                                     │
│          ├── ECR                                                     │
│          └── AWS EC2 Image Builder                                  │
│                                                                     │
│                    Infrastructure as Code                           │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    5. KUBERNETES PLATFORM                           │
│                                                                     │
│                       Kubernetes Cluster                            │
│                                                                     │
│   ┌──────────────────────────────┐                                  │
│   │  KUBERNETES CONTROL PLANE    │                                  │
│   │          (MASTER)            │                                  │
│   │                              │                                  │
│   │  ┌────────────────────────┐  │                                  │
│   │  │ API Server             │  │                                  │
│   │  ├────────────────────────┤  │                                  │
│   │  │ Scheduler              │  │                                  │
│   │  ├────────────────────────┤  │                                  │
│   │  │ Controller Manager     │  │                                  │
│   │  ├────────────────────────┤  │                                  │
│   │  │ etcd                   │  │                                  │
│   │  └────────────┬───────────┘  │                                  │
│   └───────────────┼──────────────┘                                  │
│                   │                                                 │
│                   │ Kubernetes API                                  │
│                   ▼                                                 │
│   ┌──────────────────────────────────────────────────────────────┐  │
│   │                    WORKER NODE(S)                            │  │
│   │                                                              │  │
│   │        Customer Churn Namespace                              │  │
│   │                                                              │  │
│   │   ┌───────────────────┐                                      │  │
│   │   │ Kubernetes        │                                      │  │
│   │   │ Service           │                                      │  │
│   │   └─────────┬─────────┘                                      │  │
│   │             │                                                │  │
│   │             ▼                                                │  │
│   │   ┌─────────────────────────┐                                │  │
│   │   │ Kubernetes Deployment   │                                │  │
│   │   └────────────┬────────────┘                                │  │
│   │                │                                             │  │
│   │                ▼                                             │  │
│   │   ┌─────────────────────────┐                                │  │
│   │   │ FastAPI Pod(s)          │                                │  │
│   │   │                         │                                │  │
│   │   │ Docker Container        │                                │  │
│   │   │ Customer Churn API      │                                │  │
│   │   └────────────┬────────────┘                                │  │
│   │                │                                             │  │
│   └────────────────┼─────────────────────────────────────────────┘  │
│                    │                                                │
└────────────────────┼────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       6. ML LIFECYCLE                               │
│                                                                     │
│ Dataset → Preprocessing → Feature Engineering → Training            │
│                                      │                              │
│                                      ▼                              │
│                          Hyperparameter Tuning                      │
│                                      │                              │
│                                      ▼                              │
│                              Evaluation                             │
│                                      │                              │
│                                      ▼                              │
│                         Threshold Optimization                      │
│                                      │                              │
│                                      ▼                              │
│                              MLflow                                 │
│                       ┌─────────────────────┐                        │
│                       │ Experiment Tracking │                        │
│                       │ Model Registry      │                        │
│                       │ Production Alias    │                        │
│                       └──────────┬──────────┘                        │
│                                  │                                   │
│                                  ▼                                   │
│                       Customer Churn Model                           │
│                       Production / Champion                          │
│                       Threshold = 0.32                               │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       7. MODEL SERVING                              │
│                                                                     │
│                         FastAPI API                                 │
│                                                                     │
│        /predict ─────► Customer Churn Prediction                    │
│        /health  ─────► Application Health                           │
│        Swagger   ─────► API Documentation                           │
│        ReDoc     ─────► API Documentation                           │
│                                                                     │
│                  Churn / No Churn Response                          │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │
                                   ▼
╔═════════════════════════════════════════════════════════════════════╗
║                      8. OBSERVABILITY                              ║
║                                                                     ║
║             FastAPI + Kubernetes Metrics                            ║
║                         │                                           ║
║                         ▼                                           ║
║                   ┌──────────────┐                                  ║
║                   │  Prometheus  │                                  ║
║                   │              │                                  ║
║                   │ Metrics      │                                  ║
║                   │ Alert Rules  │                                  ║
║                   └──────┬───────┘                                  ║
║                          │                                          ║
║                          ▼                                          ║
║                   ┌──────────────┐                                  ║
║                   │   Grafana    │                                  ║
║                   │              │                                  ║
║                   │ API Health   │                                  ║
║                   │ K8s Metrics  │                                  ║
║                   │ System       │                                  ║
║                   │ Dashboards   │                                  ║
║                   └──────────────┘                                  ║
║                                                                     ║
║                    Helm → Monitoring Stack                          ║
╚═════════════════════════════════════════════════════════════════════╝


                         END-TO-END FLOW

Developer
    ↓
GitHub
    ↓
Security / IAM / Secrets
    ↓
GitHub Actions CI/CD
    ↓
Tests + SonarQube
    ↓
Docker Build
    ↓
Amazon ECR
    ↓
Kubernetes Deployment
    ↓
Control Plane (Master)
    ↓
Worker Node(s)
    ↓
FastAPI Pod
    ↓
MLflow Production Model
    ↓
Customer Churn Prediction
    ↓
Prometheus
    ↓
Grafana
    ↓
Alerts / Dashboards




Enterprise AI MLOps Platform — Architecture

Customer Churn Prediction — End-to-End MLOps Architecture

This document describes the complete architecture of the Enterprise AI MLOps Platform, including development, source control, security, CI/CD, AWS infrastructure, Kubernetes, machine-learning lifecycle, model serving, and observability.

1. Developer & Source Control

Developer
    |
    v
GitHub Repository
    |
    +-- Application Code
    +-- ML Code
    +-- Dockerfile
    +-- Kubernetes Manifests
    +-- Terraform
    +-- GitHub Actions Workflows

GitHub acts as the central source-control and collaboration platform for application code, ML code, infrastructure-as-code, container configuration, and CI/CD workflows.

2. Security

GitHub Secrets
      |
      +---- AWS Credentials / Tokens
      |
      v
AWS IAM
      |
      +---- Least-Privilege Access
      +---- EC2 IAM Role
      +---- ECR Access

AWS Security Groups
      |
      +---- Controlled Network Access
      +---- Application Ports

Security principles:

Credentials and secrets are not committed to Git.

IAM controls access to AWS resources.

EC2 uses an IAM role for AWS resource access.

ECR permissions are controlled through IAM.

Security Groups restrict network access and application ports.

GitHub Actions uses protected secrets for CI/CD operations.

3. CI/CD Pipeline

GitHub Repository
        |
        v
GitHub Actions
        |
        +--> Checkout
        |
        +--> Install Dependencies
        |
        +--> Automated Tests
        |
        +--> Code Quality / SonarQube
        |
        +--> Docker Build
        |
        v
Amazon ECR
        |
        v
Kubernetes Deployment

CI

The Continuous Integration stage validates the code before deployment.

Source checkout

Dependency installation

Automated tests

ML/application validation

Code-quality analysis

Docker image build

CD

The Continuous Deployment stage publishes the container image to Amazon ECR and deploys the application to Kubernetes.

4. AWS Infrastructure

Infrastructure is provisioned and managed using Terraform.

                    Terraform
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
        AWS VPC        IAM      Security Groups
          |
          +---- Network / Subnets
          |
          +---- EC2
          |
          +---- ECR
          |
          +---- AWS EC2 Image Builder

Main AWS Components

AWS VPC

Network and subnets

IAM

Security Groups

EC2

Amazon ECR

AWS EC2 Image Builder

Terraform Infrastructure as Code

Terraform provides repeatable and version-controlled infrastructure provisioning.

5. Kubernetes Platform

The application is containerized and deployed to Kubernetes.

                     Kubernetes Cluster
                              |
             +----------------+----------------+
             |                                 |
             v                                 v
   Kubernetes Control Plane              Worker Node(s)
          (Master)                              |
             |                                  |
       +-----+------+                           |
       |            |                           |
       v            v                           v
   API Server   Scheduler              Customer Churn Namespace
       |            |                           |
       +------+-----+                           |
              |                                 |
        Controller Manager                      |
              |                                 |
             etcd                               |
                                                |
                                   +------------+------------+
                                   |                         |
                                   v                         v
                           Kubernetes Service       Kubernetes Deployment
                                                             |
                                                             v
                                                     FastAPI Pod(s)
                                                             |
                                                             v
                                                     Docker Container
                                                             |
                                                             v
                                                     Customer Churn API

Kubernetes Control Plane

The control plane manages the Kubernetes cluster.

API Server

Scheduler

Controller Manager

etcd

Worker Nodes

Worker nodes run the application workloads.

Customer Churn namespace

Kubernetes Service

Kubernetes Deployment

FastAPI Pod(s)

Docker container

Kubernetes Deployment Flow

Amazon ECR
    |
    v
Kubernetes Deployment
    |
    v
FastAPI Pod(s)
    |
    v
Customer Churn API

6. ML Lifecycle

Dataset
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
Hyperparameter Tuning
   |
   v
Model Evaluation
   |
   v
Threshold Optimization
   |
   v
MLflow Tracking
   |
   v
MLflow Model Registry
   |
   v
Production / Champion Model

MLflow

MLflow provides:

Experiment tracking

Model metrics

Model artifacts

Model Registry

Production model management

Production/Champion alias

Production Model

The customer churn production model uses a decision threshold of:

Decision Threshold = 0.32

7. Model Serving

The trained production model is exposed through FastAPI.

                 FastAPI
                    |
        +-----------+-----------+
        |           |           |
        v           v           v
    /predict      /health    Swagger / ReDoc
        |
        v
Customer Churn Model
        |
        v
Churn / No Churn Prediction

API Responsibilities

Serve customer churn predictions

Load the production model

Apply the production decision threshold

Provide application health information

Provide Swagger API documentation

Provide ReDoc API documentation

8. Observability & Monitoring

The application and Kubernetes environment are monitored using Prometheus and Grafana.

FastAPI + Kubernetes Metrics
             |
             v
       Prometheus
             |
       +-----+-----+
       |           |
       v           v
    Metrics    Alert Rules
       |
       v
     Grafana
       |
       +---- API Health
       +---- Kubernetes Metrics
       +---- System Metrics
       +---- Dashboards

Prometheus

Prometheus collects application and infrastructure metrics and evaluates alert rules.

Grafana

Grafana provides monitoring dashboards for:

API health

Kubernetes resources

System resources

Application metrics

Operational visibility

Helm

Helm is used for Kubernetes monitoring-stack deployment/management where applicable.

Helm
  |
  +---- Prometheus
  |
  +---- Grafana

End-to-End Architecture Flow

Developer
    |
    v
GitHub Repository
    |
    v
Security / IAM / Secrets
    |
    v
GitHub Actions CI/CD
    |
    +--> Tests
    +--> SonarQube
    +--> Docker Build
    |
    v
Amazon ECR
    |
    v
Kubernetes Deployment
    |
    v
Kubernetes Control Plane
    |
    v
Worker Node(s)
    |
    v
FastAPI Pod
    |
    v
Customer Churn Model
    ^
    |
MLflow Model Registry
    ^
    |
Training / Tuning / Evaluation
    |
    v
Customer Churn Prediction
    |
    v
Prometheus
    |
    v
Grafana
    |
    v
Dashboards / Alerts

Architecture Layers

Layer

Technologies / Components

Development

Developer, Git

Source Control

GitHub

Security

GitHub Secrets, IAM, Security Groups

CI/CD

GitHub Actions

Code Quality

SonarQube

Containerization

Docker

Container Registry

Amazon ECR

Infrastructure

Terraform

AWS

VPC, EC2, IAM, Security Groups, ECR, EC2 Image Builder

Orchestration

Kubernetes

Kubernetes

Control Plane, Worker Nodes, Namespace, Service, Deployment, Pods

ML Lifecycle

Preprocessing, Training, Tuning, Evaluation, Threshold Optimization

ML Platform

MLflow Tracking, Model Registry

Model Serving

FastAPI

API Documentation

Swagger, ReDoc

Monitoring

Prometheus

Visualization

Grafana

Kubernetes Package Management

Helm

Key Production Characteristics

End-to-end automated CI/CD pipeline

Infrastructure as Code with Terraform

Containerized ML API with Docker

Amazon ECR container registry

Kubernetes-based application deployment

Kubernetes control-plane and worker-node architecture

MLflow experiment tracking and model registry

Production/Champion model management

FastAPI model-serving layer

Prometheus metrics and alerting

Grafana dashboards

AWS IAM and Security Group controls

AWS EC2 Image Builder integration

GitHub-based source control and automation

Project Architecture Summary

The platform follows an end-to-end MLOps architecture in which developers commit application, ML, infrastructure, Docker, and Kubernetes code to GitHub. GitHub Actions performs continuous integration, testing, code-quality analysis, Docker image creation, and deployment automation.

Terraform manages the AWS infrastructure, while Amazon ECR stores container images. Kubernetes provides container orchestration through the control plane and worker nodes. The FastAPI application serves the production customer-churn model registered in MLflow.

Prometheus collects application and Kubernetes metrics, while Grafana provides operational dashboards and monitoring visibility. Security is enforced through GitHub Secrets, AWS IAM, IAM roles, and Security Groups.

The resulting architecture provides a complete development-to-production MLOps workflow for customer churn prediction.