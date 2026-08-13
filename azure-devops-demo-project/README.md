# Sample Azure DevOps Web App Demo

A complete, production-ready sample DevOps demo project featuring a Node.js Express application, Infrastructure-as-Code (IaC) via Azure Bicep, and dual CI/CD pipeline definitions for both **GitHub Actions** and **Azure DevOps Pipelines**.

---

## 1. Project Structure

```text
azure-devops-demo-project/
├── .github/
│   └── workflows/
│       └── azure-deploy.yml    # GitHub Actions workflow
├── infra/
│   ├── main.bicep              # Azure Bicep IaC script
│   └── main.parameters.json    # Bicep parameters template
├── src/
│   ├── views/
│   │   └── index.html          # Premium dashboard UI
│   ├── test/
│   │   └── app.test.js         # Integration tests
│   └── app.js                  # Express backend app
├── azure-pipelines.yml         # Azure DevOps Pipelines config
├── package.json                # Project dependencies & scripts
└── README.md                   # Setup guide (This file)
```

---

## 2. Local Development & Testing

Run the application locally before deploying it to Azure.

### Prerequisites
- Install [Node.js](https://nodejs.org/) (v18 or higher recommended).
- A terminal (Bash, PowerShell, or command prompt).

### Step-by-Step Execution
1. Navigate to the project directory:
   ```bash
   cd azure-devops-demo-project
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the unit test suite:
   ```bash
   npm test
   ```

4. Start the local server:
   ```bash
   npm start
   ```

5. Open your browser and navigate to `http://localhost:3000` to see the live dashboard.

---

## 3. Provisioning Azure Infrastructure (IaC)

Before deploying, you can manually test the infrastructure creation using the Azure CLI.

### Step 1: Login to Azure & Set Subscription
```bash
az login
az account set --subscription <Your-Subscription-ID>
```

### Step 2: Create a Resource Group
```bash
az group create --name my-devops-demo-rg --location eastus
```

### Step 3: Deploy using Bicep
```bash
az deployment group create \
  --resource-group my-devops-demo-rg \
  --template-file ./infra/main.bicep \
  --parameters webAppName="my-unique-webapp-name"
```
Once completed, the deployment output will display the live URL of your Web App (e.g., `https://my-unique-webapp-name.azurewebsites.net`).

---

## 4. Configuring CI/CD Pipelines

### Option A: GitHub Actions (Recommended)

1. **Create an Azure Service Principal** for authorization:
   ```bash
   az ad sp create-for-rbac \
     --name "GitHub-Actions-Deployer" \
     --role Contributor \
     --scopes /subscriptions/<Subscription-ID>/resourceGroups/my-devops-demo-rg \
     --json-auth
   ```

2. **Save Secrets in GitHub**:
   Go to your GitHub Repository -> Settings -> Secrets and variables -> Actions, and add the following repository secrets:
   - `AZURE_CREDENTIALS`: Paste the complete JSON output from the command in Step 1.
   - `AZURE_SUBSCRIPTION_ID`: Your Azure Subscription ID.
   - `AZURE_RESOURCE_GROUP`: `my-devops-demo-rg`
   - `AZURE_WEBAPP_NAME`: The globally unique name of your web app.

3. **Deploy**: Push changes to the `main` branch. GitHub Actions will build, test, and deploy the application.

---

### Option B: Azure DevOps Pipelines

1. **Import Code**: Push this repository to your Azure DevOps Project Git Repo.
2. **Create Service Connection**:
   - Go to Project Settings -> Service Connections -> New Service Connection -> **Azure Resource Manager**.
   - Select **Service Principal (automatic)**, scope it to your subscription and target Resource Group, and name it `MyAzureServiceConnection`.
3. **Configure Variables**:
   Update the variable values at the top of `azure-pipelines.yml` to match your Azure environment names.
4. **Create Pipeline**:
   - Navigate to Pipelines -> New Pipeline -> **Azure Repos Git**.
   - Select your repo and point it to the existing `azure-pipelines.yml` file.
   - Click **Run**.
