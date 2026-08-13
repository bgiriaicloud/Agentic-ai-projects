# GCP Cloud Run Deployment Guide - Multi-Agent ADK Platform

This guide outlines the instructions to package and host the Multi-Agent ADK Platform on **Google Cloud Run** using containerization and the `gcloud` CLI.

---

## 📦 Step 1: Docker Containerization

Create a `Dockerfile` inside the `ai-agent` directory:

```dockerfile
# Use python-slim runtime
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8501

WORKDIR /app

# Install dependencies
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

# Run streamlit binding to the dynamic Cloud Run port
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT} --server.address=0.0.0.0"]
```

---

## 🚀 Step 2: Build and Deploy using Cloud Build & Cloud Run

### 1. Build the Container Image in the Cloud
Run Cloud Build to package the image directly in Google Artifact Registry:
```bash
gcloud builds submit --tag us-central1-docker.pkg.dev/YOUR_PROJECT_ID/agentic-ai-repo/multi-agent-app:latest .
```

### 2. Deploy to Google Cloud Run
Deploy the container, inject the Gemini API Key, and set budget-friendly scaling bounds:
```bash
gcloud run deploy multi-agent-service \
    --image=us-central1-docker.pkg.dev/YOUR_PROJECT_ID/agentic-ai-repo/multi-agent-app:latest \
    --region=us-central1 \
    --port=8501 \
    --set-env-vars="GEMINI_API_KEY=YOUR_GEMINI_API_KEY,GCP_PROJECT_ID=YOUR_PROJECT_ID" \
    --max-instances=3 \
    --cpu=2 \
    --memory=2Gi \
    --allow-unauthenticated
```

---

## 🔒 Step 3: Production Security Enhancements

To align with GCP Zero-Trust architecture:
1.  Store the `GEMINI_API_KEY` inside **GCP Secret Manager**.
2.  Grant the Cloud Run default compute service account (`roles/secretmanager.secretAccessor`) permissions to access the secret.
3.  Update the Cloud Run service definition to mount the secret as an environment variable:
    ```bash
    gcloud run services update multi-agent-service \
        --region=us-central1 \
        --update-secrets="GEMINI_API_KEY=gemini-api-key:latest"
    ```
Once deployed, navigate to the output URL to launch your collaborative Multi-Agent GCP planning interface!
