# GCP Cloud Run Deployment Guide

This guide details the step-by-step instructions to build, package, and deploy the Enterprise Agentic AI Platform demo onto **Google Cloud Run** using the Google Cloud SDK (`gcloud` CLI).

---

## 📋 Prerequisites
1.  A Google Cloud Platform (GCP) account.
2.  The Google Cloud SDK (`gcloud` CLI) installed and authenticated on your local machine.
3.  An active Gemini API Key from [Google AI Studio](https://aistudio.google.com/app/api-keys).

---

## 🛠️ Step 1: Configure Your GCP Environment

### 1. Initialize and Set Your Project
Authenticate your session and set your target GCP Project ID:
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 2. Enable Required APIs
Enable the APIs for Cloud Run, Artifact Registry, and Vertex AI (which ADK uses under the hood):
```bash
gcloud services enable \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    aiplatform.googleapis.com
```

---

## 📦 Step 2: Create Artifact Registry & Push Container

We will use Google Artifact Registry to host our container image.

### 1. Create a Repository
Create a Docker repository in your preferred GCP region (e.g., `us-central1`):
```bash
gcloud artifacts repositories create agentic-ai-repo \
    --repository-format=docker \
    --location=us-central1 \
    --description="Repository for hosting Agentic AI Platform container images"
```

### 2. Configure Docker Authentication
Authenticate your local Docker daemon to write to the Artifact Registry repository:
```bash
gcloud auth configure-docker us-central1-docker.pkg.dev
```

### 3. Build and Tag the Image
From the `Enterprise_agentic_ai_platform_project` root directory, build and tag the Docker image:
```bash
docker build -t us-central1-docker.pkg.dev/YOUR_PROJECT_ID/agentic-ai-repo/agentic-app:latest .
```

### 4. Push the Image to Artifact Registry
Push the tagged container image to your GCP repository:
```bash
docker push us-central1-docker.pkg.dev/YOUR_PROJECT_ID/agentic-ai-repo/agentic-app:latest
```

*(Alternative: You can use **Google Cloud Build** to build and push the container directly in the cloud with a single command without running local Docker daemon)*:
```bash
gcloud builds submit --tag us-central1-docker.pkg.dev/YOUR_PROJECT_ID/agentic-ai-repo/agentic-app:latest .
```

---

## 🚀 Step 3: Deploy to Google Cloud Run

Deploy the pushed container image as a Cloud Run service.

### 1. Execute the Deployment Command
We will deploy the container, configure it to listen on port `8080`, inject the `GEMINI_API_KEY` environment variable, set scaling boundaries for budget safety, and configure CPU allocation:
```bash
gcloud run deploy agentic-ai-service \
    --image=us-central1-docker.pkg.dev/YOUR_PROJECT_ID/agentic-ai-repo/agentic-app:latest \
    --region=us-central1 \
    --port=8080 \
    --set-env-vars="GEMINI_API_KEY=YOUR_GEMINI_API_KEY" \
    --min-instances=1 \
    --max-instances=5 \
    --cpu=2 \
    --memory=2Gi \
    --allow-unauthenticated
```

> [!IMPORTANT]
> *   `--min-instances=1`: Ensures there is always 1 warm container active to prevent cold start latency, ensuring instant chat response times.
> *   `--max-instances=5`: Restricts scaling limits to protect your billing account from runaway token or computation expenses.
> *   `--allow-unauthenticated`: Makes the dashboard endpoint publicly accessible. For internal corporate environments, omit this flag and configure Cloud IAP (Identity-Aware Proxy).

---

## 🔒 Step 4: Security Hardening (Production Standards)

For production enterprise compliance, instead of passing the API key in plain text environment variables, you should store it in **GCP Secret Manager** and mount it.

### 1. Store API Key in Secret Manager
```bash
echo -n "YOUR_GEMINI_API_KEY" | gcloud secrets create gemini-api-key \
    --data-file=- \
    --replication-policy="automatic"
```

### 2. Grant Secret Access to the Cloud Run Service Account
Find your Cloud Run service identity account (default: `[project-number]-compute@developer.gserviceaccount.com`) and grant it permission to read the secret:
```bash
gcloud secrets add-iam-policy-binding gemini-api-key \
    --member="serviceAccount:YOUR_PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

### 3. Redeploy Cloud Run Referencing the Secret
Update the Cloud Run service to map the Secret Manager secret directly to the container's environment variables:
```bash
gcloud run services update agentic-ai-service \
    --region=us-central1 \
    --update-secrets="GEMINI_API_KEY=gemini-api-key:latest"
```

---

## 🔍 Step 5: Verification
Once the deployment finishes, the terminal will print the service URL (e.g. `https://agentic-ai-service-xxxxxx-uc.a.run.app`). Open this URL in your web browser to test the live Agentic AI platform!
