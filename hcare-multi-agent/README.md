# Healthcare Multi-Agent Platform (GCP Production)
## 4-Tier Cognitive Multi-Agent Architecture for Healthcare Systems

This repository contains the complete production-grade implementation of the **Healthcare Multi-Agent Architecture on Google Cloud Platform**, incorporating Cloud Healthcare API (FHIR R4), HIPAA De-identification, and specialized Meta-Agents and Domain Agents.

---

## 🏥 Architecture & Tier Hierarchy

```
Tier 1: Infrastructure & External Systems (Cloud Healthcare API, FHIR R4, BigQuery, Payer API)
    │
    ▼
Tier 2: Specialized Meta-Agents
    ├── Data Compliance & Privacy Agent (HIPAA Safe Harbor PHI Redaction)
    ├── Clinical Reasoning Agent (Medical Guideline & FHIR Observation Synthesis)
    └── Communication Orchestrator (A2A Dynamic Routing & HITL Workflow Bus)
    │
    ▼
Tier 3: Hospital AI Assistant (Master Coordinator on Gemini 2.0 Pro)
    │
    ▼
Tier 4: Specialized Domain Agents (7)
    ├── 1. Patient Agent (Inquiries, Appointments, Patient Portal)
    ├── 2. Lab Test Agent (LIS & FHIR Observation Queries)
    ├── 3. Hospital Admin Agent (ICU Bed & Staff Occupancy Management)
    ├── 4. Doctor Agent (Physician Clinical Notes & Electronic Prescriptions)
    ├── 5. Insurance Agent (Payer Claims Verification EDI 270/278 Pre-Auth)
    ├── 6. Nursing Agent (Nurse Station Messaging & eMAR Medication Schedules)
    └── 7. IT Admin AI Agent (System Diagnostics, FHIR API Latency & Health Logs)
```

---

## ⚡ Quick Start & Verification

### 1. Run Automated Unit Tests
```bash
python3 test_hcare_agents.py
```

### 2. Launch FastAPI Server Locally (Port 8005)
```bash
python3 app.py
```
* **Interactive Healthcare Dashboard**: `http://localhost:8005`
* **Health Check API**: `http://localhost:8005/api/healthz`

---

## 📚 Complete Deployment Guide
For complete step-by-step GCP infrastructure provisioning (Terraform, Cloud Healthcare API, Cloud DLP, Dockerfile, Cloud Build CI/CD, and Cloud Run), see:
📄 [**`DEPLOYMENT_GUIDE.md`**](DEPLOYMENT_GUIDE.md)
