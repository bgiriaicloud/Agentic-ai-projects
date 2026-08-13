# Sample Amazon Web Services (AWS) Web App Demo

A complete, production-ready DevOps demo project featuring a Node.js Express application, Infrastructure-as-Code (IaC) via HashiCorp Terraform, and pipelines for both **GitHub Actions** and **AWS CodeBuild**.

---

## 1. Project Structure

```text
aws-devops-demo-project/
├── .github/
│   └── workflows/
│       └── aws-deploy.yml      # GitHub Actions workflow
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
├── buildspec.yml               # AWS CodeBuild specification config
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
   cd aws-devops-demo-project
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
   docker build -t aws-demo-local .
   docker run -p 8080:8080 aws-demo-local
   ```

---

## 3. Manual Infrastructure Provisioning (Terraform)

### Step 1: Login to AWS CLI
Ensure you have the AWS CLI installed and configured:
```bash
aws configure
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
   terraform apply -var="region=us-east-1"
   ```
This creates the Amazon ECR repository and a placeholder AWS App Runner service.

---

## 4. Configuring CI/CD Pipelines

### Option A: GitHub Actions (Recommended)

1. **Create an IAM User** or Role in AWS:
   - Create a user (e.g. `github-deployer`).
   - Assign policies: `AmazonEC2ContainerRegistryFullAccess`, `AWSAppRunnerAdministrator`, and permissions to manage IAM roles (needed for Terraform to create App Runner's execution role).

2. **Generate Access Keys**:
   - Go to IAM -> Users -> `github-deployer` -> Security Credentials -> **Create access key**.

3. **Configure GitHub Repository Secrets**:
   Go to your GitHub repo -> Settings -> Secrets -> Actions:
   - `AWS_ACCESS_KEY_ID`: Your IAM user access key ID.
   - `AWS_SECRET_ACCESS_KEY`: Your IAM user secret access key.
   - `AWS_REGION`: `us-east-1`
   - `AWS_ACCOUNT_ID`: Your 12-digit AWS Account ID.

4. **Deploy**: Push changes to the `main` branch. GitHub Actions will run tests, apply Terraform changes, build the container, and redeploy App Runner.

---

### Option B: Native AWS CodeBuild

1. **Create an ECR Repository** (via console or Terraform).
2. **Create a CodeBuild Project**:
   - Source: Connect to your GitHub repository.
   - Environment: Select **Managed Image**, Operating System: **Amazon Linux**, Runtime: **Standard**, Image: **latest version**.
   - Enable the **Privileged flag** (required to build Docker container images).
   - Buildspec: Select **Use a buildspec file** (it will auto-detect the `buildspec.yml` in the project root).
3. **IAM Service Role Permissions**:
   Ensure the service role created for CodeBuild has the `AmazonEC2ContainerRegistryFullAccess` policy attached to push images to ECR.
4. **Environment Variables**:
   In your CodeBuild project configuration, add these environment variables:
   - `AWS_ACCOUNT_ID`: Your 12-digit account ID.
   - `AWS_DEFAULT_REGION`: `us-east-1`
5. **Run Build**: Trigger the build manually or configure Webhooks to run on git push.
