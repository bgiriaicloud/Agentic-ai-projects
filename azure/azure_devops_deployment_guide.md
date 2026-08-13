# Azure DevOps Deployment Guide

This guide provides step-by-step instructions and technical patterns for configuring, running, and troubleshooting automated deployments from Azure DevOps to Microsoft Azure.

---

## 1. Connecting Azure DevOps to Azure (Service Connections)

Before Azure Pipelines can deploy resources, it must be authorized to interact with your Azure subscription.

### Option A: Workload Identity Federation (Recommended / Passwordless)
Workload Identity Federation uses OpenID Connect (OIDC) to authenticate. It eliminates the need to manage, rotate, and secure Azure Client Secrets.

#### Step-by-Step Configuration:
1. **In Azure DevOps**: Go to **Project Settings** -> **Service Connections** -> **New service connection**.
2. Select **Azure Resource Manager** -> Click **Next**.
3. Choose **Workload Identity Federation (automatic)** -> Click **Next**.
4. Configure the Scope:
   - **Subscription**: Select your Subscription.
   - **Resource Group**: Select your target Resource Group (highly recommended to restrict access).
5. Name the connection (e.g., `MyAzureServiceConnection`) and select **Grant access permission to all pipelines** -> Click **Save**.
6. Behind the scenes, Azure DevOps automatically provisions an App Registration in Microsoft Entra ID and creates a **Federated Credential** linking your pipeline's organization/project to that application identity.

### Option B: Service Principal Manual (Secret-based)
If automatic configuration is blocked by Entra ID directory permissions:
1. Create a service principal manually in Azure:
   ```bash
   az ad sp create-for-rbac --name "DevOps-Deployment-SP" --role Contributor --scopes /subscriptions/<sub-id>/resourceGroups/<rg-name>
   ```
2. In Azure DevOps Service Connections, select **Service Principal (manual)**.
3. Paste the `appId` (Client ID), the `password` (Client Secret), and the `tenant` (Tenant ID) from the CLI output.

---

## 2. Environments & Release Controls

Azure DevOps **Environments** represent target groups of resources (e.g., `Development`, `Staging`, `Production`) and allow you to enforce security gates and compliance audits.

```
[Build Stage] ──> [Deploy Dev] ──> [Deploy Staging] ──> (Manual Approval Gate) ──> [Deploy Prod]
```

### Setting up Environments & Approvals:
1. In your Azure DevOps Project, go to **Pipelines** -> **Environments** -> Click **New Environment**.
2. Name it (e.g., `Production`) and select **None** for resources (we will bind it logically in YAML) -> Click **Create**.
3. Open the newly created environment -> Click the three dots in the top right -> Select **Approvals and checks**.
4. Configure:
   - **Approvals**: Add the users or groups whose explicit consent is required before deployment starts.
   - **Control Options**: Set the timeout (e.g., 2 days) after which the deployment is automatically rejected if not approved.
   - **Exclusive Lock**: Enable this check to ensure only one run deploys to the environment at a time, preventing concurrency overrides.

---

## 3. YAML Deployment Pipeline Architecture

A deployment pipeline should utilize the **`deployment` job** structure in YAML, which differs from standard agent jobs by supporting deployment strategies, lifecycle hooks, and automated history tracking.

### Recommended YAML Deployment Pattern:

```yaml
jobs:
  - deployment: DeployWeb
    displayName: 'Deploy App to Production'
    pool:
      vmImage: 'ubuntu-latest'
    # Bind to the Azure DevOps Environment and enforce approvals
    environment: 'Production'
    strategy:
      # runOnce is the default deployment strategy (deploy, wait, verify)
      runOnce:
        deploy:
          steps:
            # Step 1: Download package artifacts published by the build stage
            - download: current
              artifact: drop
              
            # Step 2: Execute the deployment task
            - task: AzureRmWebAppDeployment@4
              inputs:
                FileType: 'Zip'
                Package: '$(Pipeline.Workspace)/drop/deploy.zip'
                azureSubscription: 'MyAzureServiceConnection'
                WebAppName: 'my-production-web-app'
```

### Deployment Hook Event Cycles
For complex deployments, the `strategy` block supports lifecycle hooks:
- `preDeploy`: Run tasks before resource deployment starts (e.g., database backups or resource locks check).
- `deploy`: Execute the actual resource update commands.
- `routeTraffic`: Configure routing configurations (e.g., swapping deployment slots or updating load balancer backends).
- `postRouteTraffic`: Verify health, run integration tests.
- `on: success` / `on: failure`: Run automated rollback scripts or send alerts based on run success/failure.

---

## 4. Core Deployment Tasks Reference

### 1. Infrastructure-as-Code (Bicep/ARM)
Deploys or updates resources before deploying application code.

```yaml
- task: AzureResourceManagerTemplateDeployment@3
  inputs:
    deploymentScope: 'Resource Group'
    connectedServiceName: 'MyAzureServiceConnection'
    action: 'Create Or Update Resource Group'
    resourceGroupName: 'my-production-rg'
    location: 'eastus'
    templateLocation: 'Linked artifact'
    csmFile: '$(Pipeline.Workspace)/infra/main.bicep'
    overrideParameters: '-webAppName my-prod-app -skuName B1'
    deploymentMode: 'Incremental'
  displayName: 'Provision Infrastructure via Bicep'
```

### 2. Web App Deployment (App Service)
Deploys zipped application binaries (Node.js, .NET, Python, etc.) to Azure Web Apps.

```yaml
- task: AzureRmWebAppDeployment@4
  inputs:
    connectedServiceName: 'MyAzureServiceConnection'
    WebAppName: 'my-prod-app'
    Package: '$(Pipeline.Workspace)/drop/deploy.zip'
    enableCustomDeployment: true
    DeploymentType: 'zipDeploy'
  displayName: 'Deploy Application Package'
```

### 3. Container Deployments (AKS)
Deploys built container images to Azure Kubernetes Service clusters using manifests.

```yaml
- task: KubernetesManifest@1
  inputs:
    action: 'deploy'
    connectionType: 'kubernetesServiceConnection'
    kubernetesServiceConnection: 'MyAKSConnection'
    namespace: 'production'
    manifests: '$(Pipeline.Workspace)/manifests/deployment.yml'
    containers: 'myacr.azurecr.io/myapp:$(Build.BuildId)'
  displayName: 'Deploy Manifests to AKS'
```

### 4. Serverless Functions (Azure Functions)
Deploys serverless code packages directly onto Function Apps.

```yaml
- task: AzureFunctionApp@1
  inputs:
    azureSubscription: 'MyAzureServiceConnection'
    appType: 'functionAppLinux'
    appName: 'my-prod-function-app'
    package: '$(Pipeline.Workspace)/drop/functions.zip'
  displayName: 'Deploy Function App'
```

---

## 5. Secret & Variable Management

Secrets must never be stored in plaintext within YAML files. Use Azure Key Vault integrated with **Variable Groups**.

### Linking Key Vault to Azure Pipelines:
1. In Azure DevOps, go to **Pipelines** -> **Library** -> Click **+ Variable group**.
2. Name the group (e.g., `KeyVault-Prod-Secrets`).
3. Toggle on **Link secrets from an Azure key vault as variables**.
4. Select your **Azure service connection** and select your **Key Vault Name**.
5. Click **Add** to select the specific secrets you want to import -> Click **Save**.
6. Reference the variable group in your pipeline YAML:

```yaml
variables:
  - group: KeyVault-Prod-Secrets

steps:
  - script: echo "Database password is $(db-password)" # db-password is read dynamically from Key Vault
```

---

## 6. Common Deployment Troubleshooting

### Error: "AuthorizationFailed: The client with object id... does not have authorization to perform action..."
* **Cause**: The service connection's service principal does not have enough permissions (e.g., Contributor or Owner) on the target Resource Group or Subscription.
* **Resolution**: Go to the Azure portal, navigate to the target Resource Group -> Access Control (IAM) -> Add Role Assignment. Assign the **Contributor** role to the service principal name used in your service connection.

### Error: "Failed to deploy web package to App Service." (Timeout / 403 Forbidden)
* **Cause**: The target Web App has network restrictions configured (IP restrictions or Private Endpoint), blocking public Microsoft-hosted agents from reaching the deployment endpoint.
* **Resolution**:
  - Open firewalls temporarily during deployment using deployment slots with private access overrides.
  - Or, deploy using a **Self-hosted agent** hosted on a VM inside the same Virtual Network (VNet) as the Web App.

### Error: "Conflict: The resource write operation failed... Resource is locked."
* **Cause**: A resource lock (ReadOnly or CanNotDelete) is applied to the resource group or individual resource, blocking the Bicep template deployment from performing updates.
* **Resolution**: Temporarily delete the resource lock via the Azure portal or CLI before running the pipeline, or adjust your Bicep deployment scope to exclude the locked resources.
