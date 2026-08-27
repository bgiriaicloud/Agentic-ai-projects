# Module 02: Developer Setup: Google Cloud Project, Vertex AI Studio & SDKs

> *"A robust, secure developer environment is the foundation for deploying production-grade AI agents on Google Cloud."*

---

## 2.1 Google AI Studio vs. Vertex AI: When to Use Which?

```
┌────────────────────────────────────────────────────────────────────────┐
│                   AI STUDIO VS. VERTEX AI COMPARISON                   │
├────────────────────────────────────────────────────────────────────────┤
│ Feature             Google AI Studio          Vertex AI Platform       │
│ ────────────────────────────────────────────────────────────────────── │
│ Target Audience     Prototyping & Fast POCs   Enterprise Production    │
│ Authentication      API Key (`GEMINI_API_KEY`) Google Cloud IAM / OAuth│
│ Data Privacy        Standard Cloud Policy     VPC-SC, Zero Data Egress │
│ Enterprise RAG      Basic File Upload         Vertex AI Vector Search  │
│ SLA & Compliance    Developer Preview SLA     99.9% Enterprise SLA     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2.2 Setting Up Your Google Cloud Project & SDK

### 1. Enable Vertex AI & Compute APIs via gcloud CLI
```bash
# Set your active GCP project
gcloud config set project YOUR_PROJECT_ID

# Enable required AI and Data APIs
gcloud services enable aiplatform.googleapis.com \
                       compute.googleapis.com \
                       bigquery.googleapis.com \
                       pubsub.googleapis.com \
                       run.googleapis.com
```

### 2. Python Environment Installation
```bash
pip install google-cloud-aiplatform \
            google-genai \
            google-cloud-bigquery \
            google-cloud-pubsub \
            google-cloud-storage
```

---

## 2.3 Initializing the Vertex AI SDK in Python

```python
import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = "your-gcp-project-id"
LOCATION = "us-central1"

# Initialize Vertex AI Context
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Load Gemini 2.0 Flash Model
model = GenerativeModel("gemini-2.0-flash-exp")

response = model.generate_content("Hello Google Cloud AI! What are the 4 pillars of Agentic AI?")
print(response.text)
```
