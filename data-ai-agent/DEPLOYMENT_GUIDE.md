# GCP Cloud Run Deployment Guide - Streamlit Data Agent

This guide outlines how to containerize and deploy the Conversational Analytics Data Agent onto **Google Cloud Run**, configuring identity permissions so that the app can securely query public BigQuery datasets.

---

## 📦 Step 1: Docker Containerization

To run Streamlit on Cloud Run, create a `Dockerfile` inside the `data-ai-agent` directory:

```dockerfile
# Use python-slim runtime
FROM python:3.11-slim

# Set environment paths
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8501

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set up secure system user
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /bin/bash appuser
RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 8501

# Streamlit uses PORT environment variable for binding
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT} --server.address=0.0.0.0"]
```

---

## 🔒 Step 2: Configure GCP Service Account & BigQuery IAM Permissions

Cloud Run services authenticate to BigQuery using a Google Service Account (GSA).

### 1. Create a Service Account for the Data Agent
```bash
gcloud iam service-accounts create bq-data-agent-sa \
    --display-name="BigQuery Data Agent service account"
```

### 2. Grant BigQuery Job User Permissions
To run query jobs in your project, the service account needs the `roles/bigquery.jobUser` role:
```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:bq-data-agent-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.jobUser"
```

### 3. Grant BigQuery Data Viewer Permissions
To query the public names dataset, the service account needs the `roles/bigquery.dataViewer` role:
```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:bq-data-agent-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataViewer"
```

---

## 🚀 Step 3: Build and Deploy using Cloud Build & Cloud Run

### 1. Build and Tag Container
Run Cloud Build to package the image directly in GCP Artifact Registry:
```bash
gcloud builds submit --tag us-central1-docker.pkg.dev/YOUR_PROJECT_ID/agentic-ai-repo/bq-data-agent:latest .
```

### 2. Deploy to Google Cloud Run
Deploy the service, linking it to the created service account (`bq-data-agent-sa`) so it has automatic IAM access to BigQuery without requiring JSON key files:
```bash
gcloud run deploy bq-data-agent-service \
    --image=us-central1-docker.pkg.dev/YOUR_PROJECT_ID/agentic-ai-repo/bq-data-agent:latest \
    --region=us-central1 \
    --port=8501 \
    --service-account="bq-data-agent-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --set-env-vars="GEMINI_API_KEY=YOUR_GEMINI_API_KEY,GCP_PROJECT_ID=YOUR_PROJECT_ID" \
    --max-instances=3 \
    --allow-unauthenticated
```
Once the command completes, navigate to the output URL to access your live English-to-SQL BigQuery dashboard!
