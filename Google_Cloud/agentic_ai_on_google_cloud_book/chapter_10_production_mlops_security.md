# Chapter 10: Production Deployment, Security & MLOps on Google Cloud

> *"An agent is only as strong as the security perimeter, deployment pipeline, and observability telemetry that surrounds it."*

---

## 10.1 Production Deployment Options: Cloud Run vs. GKE

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                PRODUCTION HOSTING PLATFORMS                                       │
├───────────────────────────────────────────────────────────────────────────────────────────────────┤
│  Cloud Run (Serverless Containers)  : Auto-scales from 0 to N, zero idle cost, built-in HTTPS.   │
│  Google Kubernetes Engine (GKE)     : Stateful agent swarms, GPU/TPU nodes, custom sidecars.      │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 10.2 Enterprise Security & IAM Hardening

1. **Workload Identity Federation**: Eliminate hardcoded service account keys; bind Kubernetes service accounts directly to IAM roles.
2. **VPC Service Controls**: Create a secure security perimeter around Vertex AI, BigQuery, and GCS to prevent data exfiltration.
3. **Guardrails & Content Filtering**: Enforce safety thresholds in Vertex AI preventing prompt injection, hate speech, and PII leakage.

---

## 10.3 Observability: Cloud Logging, Trace & Vertex Model Monitoring

* **Cloud Logging**: Structured JSON logging capturing every thought, tool name, and latency metric.
* **Cloud Trace**: Distributed tracing mapping end-to-end latency across user request $\to$ LLM generation $\to$ tool execution $\to$ response.
* **Vertex AI Model Monitoring**: Detecting distribution drift in user prompts and alerting on latency degradation.

---

## 10.4 Production Dockerfile for Agent Microservice

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

## 10.5 Book Conclusion & Practitioner's Roadmap

Congratulations on completing **Mastering Agentic AI on Google Cloud**! You now possess the foundational theory, architectural blueprints, and production engineering practices to build, test, secure, and operate world-class autonomous AI systems on Google Cloud.
