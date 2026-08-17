# 📊 Monitoring & Observability

The platform uses Prometheus and Grafana to monitor application and Kubernetes infrastructure.

## Architecture

```text
FastAPI
   │
   ▼
Application Metrics
   │
   ▼
Prometheus
   │
   ├───────────────┐
   ▼               ▼
Grafana       Alert Rules
```

## Monitoring Components

### Prometheus

Prometheus collects metrics from the application and Kubernetes environment.

### Grafana

Grafana provides dashboards for visualizing metrics.

### Alerting

Prometheus alert rules detect operational conditions such as:

* Application availability
* Pod availability
* Resource utilization
* Target health
* Service failures

## Kubernetes Monitoring

Check monitoring pods:

```bash
kubectl get pods -n monitoring
```

Check services:

```bash
kubectl get svc -n monitoring
```

## Evidence

Recommended screenshots:

```text
docs/screenshots/prometheus.png
docs/screenshots/grafana.png
docs/screenshots/api-swagger.png
docs/screenshots/kubernetes.png
```

The screenshots should show actual successful project execution rather than placeholder images.
