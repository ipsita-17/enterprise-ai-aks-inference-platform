# Enterprise AI AKS Inference Platform

An end-to-end MLOps and DevOps project demonstrating how machine learning models can be trained, versioned, containerized, secured, tested, and deployed on Kubernetes using modern cloud-native practices.

The project implements a complete CI/CD workflow using GitHub Actions and deploys a FastAPI-based AI inference service on Kubernetes with Helm and Horizontal Pod Autoscaling (HPA).

---

## Table of Contents

- [Architecture](#architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [CI/CD Pipeline](#cicd-pipeline)
- [Docker Deployment](#docker-deployment)
- [API Endpoints](#api-endpoints)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Helm Deployment](#helm-deployment)
- [Autoscaling](#autoscaling)
- [Prometheus Metrics](#prometheus-metrics)
- [Challenges Solved](#challenges-solved)
- [Results](#results)
- [Future Enhancements](#future-enhancements)
- [Author](#author)

---

## Architecture

```text
                    GitHub Repository
                           │
                           ▼
                  GitHub Actions CI/CD
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
      ▼                    ▼                    ▼
   Testing             SonarQube            Trivy Scan
      │                    │                    │
      └────────────────────┴────────────────────┘
                           │
                           ▼
                    Model Training
                           │
                           ▼
                    Docker Build
                           │
                           ▼
                     Docker Hub
                           │
                           ▼
                   Kubernetes Cluster
                           │
                           ▼
                   Helm Deployment
                           │
                           ▼
                 FastAPI Inference Pods
                           │
                           ▼
                   Horizontal Pod Autoscaler
                           │
                           ▼
                     Metrics Server
```

---

## Features

### Machine Learning
- Iris Classification Model
- Scikit-Learn based training
- Model artifact generation
- Model version endpoint
- Prediction API

### MLOps
- MLflow integration
- Dataset management
- Model artifact management
- Automated model training

### DevOps
- GitHub Actions CI/CD
- Automated testing
- Code quality analysis
- Security scanning
- Docker image publishing

### Kubernetes
- Namespace isolation
- ConfigMaps & Secrets
- Deployments & Services
- Horizontal Pod Autoscaler
- Metrics Server
- Helm Charts

---

## Technology Stack

| Category            | Tools              |
|---------------------|--------------------|
| Programming         | Python             |
| API Framework       | FastAPI            |
| ML Framework        | Scikit-Learn       |
| Experiment Tracking | MLflow             |
| Version Control     | GitHub             |
| CI/CD               | GitHub Actions     |
| Code Quality        | SonarQube          |
| Security Scanning   | Trivy              |
| Containerization    | Docker             |
| Container Registry  | Docker Hub         |
| Orchestration       | Kubernetes         |
| Package Management  | Helm               |
| Autoscaling         | HPA                |
| Monitoring          | Prometheus Metrics |

---

## Project Structure

```text
enterprise-ai-aks-inference-platform/
│
├── api/
│   ├── app/
│   │   └── main.py
│   └── tests/
│
├── model/
│   ├── training/
│   │   ├── train.py
│   │   └── requirements.txt
│   └── artifacts/
│       ├── model.pkl
│       └── model_metadata.json
│
├── scripts/
│   └── create_dataset.py
│
├── kubernetes/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── hpa.yaml
│
├── helm/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│
├── argocd/
├── mlruns/
├── Dockerfile
│
└── .github/
    └── workflows/
        └── ci.yml
```

---

## CI/CD Pipeline

The GitHub Actions pipeline runs the following stages in order:

### 1. Test
Runs automated unit tests using pytest.
```bash
pytest api/tests
```

### 2. SonarQube Analysis
Performs static code analysis and quality checks.
```bash
sonar-scanner
```

### 3. Model Training
Retrains the ML model and generates artifacts.
```bash
python model/training/train.py
```
Outputs: `model.pkl`, `model_metadata.json`

### 4. Trivy Security Scan
Scans source code and Docker images for vulnerabilities.
```bash
trivy fs .
```

### 5. Docker Build
```bash
docker build -t ai-inference-api:v2 .
```

### 6. Docker Push
```bash
docker push ipsuuu/ai-inference-api:v2
```

---

## Docker Deployment

```bash
# Build
docker build -t ipsuuu/ai-inference-api:v2 .

# Run
docker run -p 8000:8000 ipsuuu/ai-inference-api:v2

# Verify
curl http://localhost:8000/health
```

Expected response:
```json
{ "status": "healthy" }
```

---

## API Endpoints

### `GET /health`
```json
{ "status": "healthy" }
```

### `GET /version`
```json
{ "model": "iris-classifier", "version": "1.0.0" }
```

### `POST /predict`

Request:
```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

Response:
```json
{ "prediction": 0 }
```

---

## Kubernetes Deployment

```bash
# Create namespace
kubectl apply -f kubernetes/namespace.yaml

# Verify
kubectl get ns
```

---

## Helm Deployment

```bash
# Validate chart
helm lint ./helm

# Install
helm install ai-platform ./helm -n ai-platform

# Upgrade
helm upgrade ai-platform ./helm -n ai-platform

# Verify
kubectl get all -n ai-platform
```

---

## Autoscaling

```bash
# Verify node and pod metrics
kubectl top nodes
kubectl top pods -n ai-platform

# Verify HPA
kubectl get hpa -n ai-platform
```

Example output:
```text
NAME         REFERENCE                     TARGETS
ai-api-hpa   Deployment/ai-inference-api   cpu: 3%/70%
```

---

## Prometheus Metrics

**Endpoint:** `GET /metrics`

Exposes:
- `prediction_requests_total`
- `prediction_latency_seconds`

---

## Challenges Solved

### ImagePullBackOff
**Issue:** `Failed to pull image`  
**Fix:** Created Docker Hub repository, pushed the image, and updated Helm image repository reference.

### CrashLoopBackOff
**Issue:** `HTTP probe failed with statuscode: 404`  
**Fix:** Added `/health` endpoint, rebuilt and pushed the image, upgraded Helm release.

### Metrics Server Failure
**Issue:** `Metrics API not available`  
**Fix:** Installed Metrics Server with insecure TLS configuration and verified metrics collection.

---

## Results

| Component                   | Status |
|-----------------------------|--------|
| End-to-End CI/CD Pipeline   | ✅     |
| Automated Model Training    | ✅     |
| Docker Image Build & Push   | ✅     |
| SonarQube Quality Analysis  | ✅     |
| Trivy Security Scanning     | ✅     |
| Kubernetes Deployment       | ✅     |
| Helm Packaging              | ✅     |
| Horizontal Pod Autoscaling  | ✅     |
| Metrics Server Integration  | ✅     |
| FastAPI Inference Service   | ✅     |
| Docker Hub Registry         | ✅     |

---

## Future Enhancements

- ArgoCD GitOps Deployment
- Prometheus Server & Grafana Dashboards
- AKS Deployment on Azure
- Terraform Infrastructure Provisioning
- Canary Deployments
- Model Monitoring & Automated Rollbacks

---

## Author

**Ipsita Patra** — DevOps & MLOps Engineer

- GitHub: [github.com/ipsita-17](https://github.com/ipsita-17)
- Docker Hub: [hub.docker.com/u/ipsuuu](https://hub.docker.com/u/ipsuuu)
