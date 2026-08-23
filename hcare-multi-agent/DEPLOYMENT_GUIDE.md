# Enterprise Deployment Guide: Healthcare Multi-Agent Platform (GCP)
## Production Deployment Blueprint with Google ADK 2.4 & Gemini Enterprise Agent Platform
### *Compliance: HIPAA Safe Harbor • HL7/FHIR R4 • Cloud Healthcare API • Cloud Run*

---

## 🏗️ 1. System Architecture Blueprint

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                    HEALTHCARE MULTI-AGENT ARCHITECTURE (GCP PRODUCTION)                           │
├───────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Tier 1: Infrastructure & External Systems                                                         │
│   • Cloud Healthcare API (FHIR R4 Dataset & Store)                                                │
│   • BigQuery Analytics Warehouse (7-Year Audit & Clinical Store)                                  │
│   • Cloud Pub/Sub (Event-Driven Ingestion & A2A Inter-Agent Bus)                                  │
├───────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Tier 2: Specialized Meta-Agents (ADK Skills)                                                      │
│   • Data Compliance & Privacy Agent (Cloud DLP 18 Safe Harbor PHI De-identification)              │
│   • Clinical Reasoning Agent (Gemini 2.0 Pro Grounding & FHIR Observations)                       │
│   • Communication Orchestrator (A2A Dynamic Dispatch & HITL Approval Bus)                         │
├───────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Tier 3: Master Coordination Core                                                                  │
│   • Hospital AI Assistant (Gemini Enterprise Agent Platform Runtime)                              │
├───────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Tier 4: 7 Domain Specialist Agents                                                                │
│   • Patient Agent            • Lab Test Agent          • Hospital Admin Agent                     │
│   • Doctor Agent             • Insurance Agent         • Nursing Agent      • IT Admin AI Agent   │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 2. Prerequisites & Environment Setup

### 1. Business Associate Agreement (BAA)
Before deploying workloads processing Protected Health Information (PHI):
1. Navigate to **Google Cloud Console > IAM & Admin > Compliance**.
2. Sign the **HIPAA Business Associate Agreement (BAA)**.

### 2. Required GCP APIs Enablement
Run the following commands in Cloud Shell or terminal:
```bash
gcloud services enable healthcare.googleapis.com \
                       aiplatform.googleapis.com \
                       bigquery.googleapis.com \
                       pubsub.googleapis.com \
                       dlp.googleapis.com \
                       firestore.googleapis.com \
                       run.googleapis.com \
                       artifactregistry.googleapis.com \
                       cloudbuild.googleapis.com
```

---

## 🛠️ 3. Infrastructure as Code (Terraform Provisioning)

Create `terraform/main.tf` to provision the entire healthcare infrastructure:

```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. Cloud Healthcare Dataset & FHIR R4 Store
resource "google_healthcare_dataset" "hcare_dataset" {
  name     = "hcare-production-dataset"
  location = var.region
  time_zone = "UTC"
}

resource "google_healthcare_fhir_store" "fhir_store" {
  name     = "clinical-fhir-r4-store"
  dataset  = google_healthcare_dataset.hcare_dataset.id
  version  = "R4"

  enable_update_create          = true
  disable_referential_integrity = false

  notification_configs {
    pubsub_topic = google_pubsub_topic.fhir_events.id
  }
}

# 2. Pub/Sub Topics
resource "google_pubsub_topic" "fhir_events" {
  name = "fhir-resource-change-events"
}

resource "google_pubsub_topic" "agent_dispatch" {
  name = "hcare-agent-dispatch"
}

# 3. Artifact Registry Repository
resource "google_artifact_registry_repository" "hcare_repo" {
  location      = var.region
  repository_id = "hcare-docker-repo"
  format        = "DOCKER"
}

# 4. Service Account & IAM Roles
resource "google_service_account" "agent_sa" {
  account_id   = "hcare-agent-runner"
  display_name = "Healthcare Multi-Agent Cloud Run Service Account"
}

resource "google_project_iam_member" "healthcare_user" {
  project = var.project_id
  role    = "roles/healthcare.fhirResourceUser"
  member  = "serviceAccount:${google_service_account.agent_sa.email}"
}

resource "google_project_iam_member" "vertex_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.agent_sa.email}"
}

resource "google_project_iam_member" "dlp_user" {
  project = var.project_id
  role    = "roles/dlp.user"
  member  = "serviceAccount:${google_service_account.agent_sa.email}"
}
```

---

## 🔒 4. Cloud DLP HIPAA De-Identification Template

Configure Cloud DLP to mask 18 HIPAA Safe Harbor identifiers:

```bash
gcloud dlp inspect-templates create \
    --project=YOUR_PROJECT_ID \
    --display-name="HIPAA-Safe-Harbor-DeID" \
    --description="Redacts SSN, phone numbers, emails, names, and MRNs" \
    --info-types=US_SOCIAL_SECURITY_NUMBER,PERSON_NAME,PHONE_NUMBER,EMAIL_ADDRESS,DATE_OF_BIRTH,MEDICAL_RECORD_NUMBER
```

---

## 🐳 5. Production Multi-Stage Dockerfile

Create `Dockerfile` in `hcare-multi-agent/`:

```dockerfile
# Stage 1: Build & Dependencies
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Minimal Runtime Image
FROM python:3.11-slim

WORKDIR /app

# Create non-root user for healthcare security compliance
RUN useradd -m -u 1001 appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PORT=8005
ENV ENVIRONMENT=production

EXPOSE 8005

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8005/api/healthz || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8005"]
```

---

## 🔄 6. Cloud Build CI/CD Pipeline (`cloudbuild.yaml`)

```yaml
steps:
  # Step 1: Execute Automated Unit Tests
  - name: 'python:3.11'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        pip install -r requirements.txt
        python -m unittest test_hcare_agents.py

  # Step 2: Build & Push Container to Artifact Registry
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - 'us-central1-docker.pkg.dev/$PROJECT_ID/hcare-docker-repo/hcare-multi-agent:$BUILD_ID'
      - '-t'
      - 'us-central1-docker.pkg.dev/$PROJECT_ID/hcare-docker-repo/hcare-multi-agent:latest'
      - '.'

  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - 'us-central1-docker.pkg.dev/$PROJECT_ID/hcare-docker-repo/hcare-multi-agent:$BUILD_ID'

  # Step 3: Deploy to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'hcare-multi-agent'
      - '--image=us-central1-docker.pkg.dev/$PROJECT_ID/hcare-docker-repo/hcare-multi-agent:$BUILD_ID'
      - '--region=us-central1'
      - '--platform=managed'
      - '--port=8005'
      - '--service-account=hcare-agent-runner@$PROJECT_ID.iam.gserviceaccount.com'
      - '--min-instances=1'
      - '--max-instances=10'
      - '--memory=2Gi'
      - '--cpu=2'
      - '--allow-unauthenticated'

images:
  - 'us-central1-docker.pkg.dev/$PROJECT_ID/hcare-docker-repo/hcare-multi-agent:$BUILD_ID'
```

---

## ⚡ 7. Post-Deployment Verification & Testing

### 1. Verify Health Endpoint
```bash
curl -i https://hcare-multi-agent-xyz-uc.a.run.app/api/healthz
```
*Expected Output:*
```json
{
  "status": "healthy",
  "service": "Healthcare Multi-Agent Platform",
  "port": 8005,
  "framework": "Google ADK 2.4",
  "platform": "Gemini Agent Platform (Vertex AI Agent Builder)",
  "hipaa_shield": "ACTIVE",
  "fhir_store": "CONNECTED"
}
```

### 2. Test Multi-Agent Query Dispatch
```bash
curl -X POST https://hcare-multi-agent-xyz-uc.a.run.app/api/agents/query \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "P-98421",
    "user_role": "Patient",
    "query": "What are my latest blood test and HbA1c glucose lab results?",
    "include_raw_fhir": true
  }'
```

---

## 📊 8. Observability, Logging & HITL Audit Trail

* **Cloud Logging Query**:
  ```sql
  resource.type="cloud_run_revision"
  jsonPayload.hipaa_compliant=true
  jsonPayload.routed_agent="Lab Test Agent"
  ```
* **7-Year Compliance Export**: Configure a Cloud Logging sink routing all audit logs to a dedicated BigQuery dataset (`hcare_audit_logs`) partitioned by month.
* **Human-in-the-Loop (HITL) Alert Policy**: Automatically routes escalations to on-call clinical teams if an unhandled medical edge-case arises.
