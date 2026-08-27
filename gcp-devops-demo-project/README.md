# Sample Google Cloud Platform (GCP) Web App Demo

A complete, production-ready DevOps demo project featuring a Node.js Express application, Infrastructure-as-Code (IaC) via HashiCorp Terraform, and pipelines for both **GitHub Actions** and **GCP Cloud Build**.

---

## 1. Project Structure

```text
gcp-devops-demo-project/
├── .github/
│   └── workflows/
│       └── gcp-deploy.yml      # GitHub Actions workflow
├── infra/
│   ├── main.tf                 # Terraform IaC script
│   ├── variables.tf            # Configuration inputs
│   └── outputs.tf              # Deployment outputs
├── src/
│   ├── views/
│   │   └── index.html          # Premium dashboard UI
│   ├── test/
│   │   └── app.test.js         # Integration tests
│   └── app.js                  # Express backend app
├── Dockerfile                  # Container packaging rules
├── cloudbuild.yaml             # GCP Cloud Build config (Root copy)
├── package.json                # Project dependencies & scripts
└── README.md                   # Setup guide (This file)
```

---

## 2. Local Development & Testing

### Prerequisites
- Install [Node.js](https://nodejs.org/) (v18 or higher).
- Install [Docker](https://www.docker.com/) (to build and test container images locally).

### Running Locally
1. Navigate to the project directory:
   ```bash
   cd gcp-devops-demo-project
   ```

2. Install packages and run tests:
   ```bash
   npm install
   npm test
   ```

3. Run the application:
   ```bash
   npm start
   ```
   Open `http://localhost:8080` in your web browser.

4. Test container build locally:
   ```bash
   docker build -t gcp-demo-local .
   docker run -p 8080:8080 gcp-demo-local
   ```

---

## 3. Manual Infrastructure Provisioning (Terraform)

### Step 1: Login to GCP CLI
Ensure you have the Google Cloud SDK installed and run:
```bash
gcloud auth login
gcloud config set project <YOUR-PROJECT-ID>
```

### Step 2: Initialize & Apply Terraform
1. Navigate to the infra directory:
   ```bash
   cd infra
   ```

2. Run Terraform:
   ```bash
   terraform init
   terraform plan
   terraform apply -var="project_id=<YOUR-PROJECT-ID>" -var="region=us-central1"
   ```
This creates the GCP Artifact Registry Docker repository and a placeholder Cloud Run service.

---

## 4. Configuring CI/CD Pipelines

### Option A: GitHub Actions (Recommended)

1. **Create a Service Account** in GCP:
   ```bash
   gcloud iam service-accounts create github-deployer-sa --display-name="GitHub Actions Deployer"
   ```

2. **Grant Roles** to the Service Account:
   Assign the following roles to the service account in your GCP project:
   - `roles/artifactregistry.admin` (Manage Docker registry)
   - `roles/run.admin` (Deploy Cloud Run services)
   - `roles/iam.serviceAccountUser` (Run containers as default service agent)
   - `roles/storage.admin` (If managing remote Terraform state buckets)

3. **Generate Key JSON**:
   ```bash
   gcloud iam service-accounts keys create gcp-key.json \
     --iam-account=github-deployer-sa@<YOUR-PROJECT-ID>.iam.gserviceaccount.com
   ```

4. **Configure GitHub Repository Secrets**:
   Go to your GitHub repo -> Settings -> Secrets -> Actions:
   - `GCP_SA_KEY`: Paste the complete contents of `gcp-key.json`.
   - `GCP_PROJECT_ID`: Your GCP project ID.
   - `GCP_REGION`: `us-central1`

5. **Deploy**: Push changes to the `main` branch. GitHub Actions will run tests, apply Terraform changes, build the container, and deploy to Cloud Run.

---

### Option B: Native GCP Cloud Build

1. **Enable Cloud Build API**:
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   ```

2. **Grant Permissions to Cloud Build Service Account**:
   Ensure the default Cloud Build Service Account (`<PROJECT-NUMBER>@cloudbuild.gserviceaccount.com`) has the following permissions:
   - **Cloud Run Admin** (`roles/run.admin`)
   - **Service Account User** (`roles/iam.serviceAccountUser`)
   - **Project Editor** (or specific permissions for Terraform actions)

3. **Create Build Trigger**:
   - Go to GCP Console -> Cloud Build -> Triggers -> **Create Trigger**.
   - Connect your GitHub Repository.
   - Set the Configuration type to **Cloud Build configuration file (yaml)** and point to `/cloudbuild.yaml` in the root.
   - Run the trigger to initiate the deployment.
