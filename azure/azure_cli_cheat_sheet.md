# Azure CLI (`az`) Cheat Sheet

This cheat sheet provides a comprehensive reference for the most commonly used Azure CLI (`az`) commands, organized by service categories.

---

## 1. Authentication & Configuration

Manage your Azure CLI environment, authenticate, and configure defaults.

| Command | Description |
| :--- | :--- |
| `az login` | Interactive login to Azure. |
| `az login --use-device-code` | Login via device code (useful for headless terminals). |
| `az logout` | Log out from the current session. |
| `az account list --output table` | List all subscriptions accessible to the logged-in account. |
| `az account set --subscription <Name-or-ID>` | Set the active subscription for the current session. |
| `az account show --output table` | Display details of the currently active subscription. |
| `az configure --defaults group=<rg-name> location=<region>` | Set default Resource Group and Location for subsequent commands. |
| `az version` | Show the installed version of Azure CLI and its modules. |
| `az extension add --name <extension-name>` | Install an official Azure CLI extension. |
| `az extension list --output table` | List all installed extensions. |

---

## 2. Resource Groups (`az group`)

Resource Groups are logical containers that hold related Azure resources.

```bash
# Create a new resource group
az group create --name MyResourceGroup --location eastus

# List all resource groups in a table format
az group list --output table

# Check if a resource group exists
az group exists --name MyResourceGroup

# Show details of a specific resource group
az group show --name MyResourceGroup

# Delete a resource group and all its resources (non-interactive, run in background)
az group delete --name MyResourceGroup --yes --no-wait

# Export a resource group as an ARM template
az group export --name MyResourceGroup > template.json
```

---

## 3. Compute: Virtual Machines (`az vm` & `az vmss`)

Deploy and manage Azure Virtual Machines (VMs) and Virtual Machine Scale Sets (VMSS).

### Virtual Machines (`az vm`)

```bash
# Create a simple Linux VM with SSH keys auto-generated
az vm create \
  --resource-group MyResourceGroup \
  --name MyVM \
  --image Ubuntu2204 \
  --admin-username azureuser \
  --generate-ssh-keys

# Create a Windows VM with a password
az vm create \
  --resource-group MyResourceGroup \
  --name MyWindowsVM \
  --image Win2022Datacenter \
  --admin-username azureuser \
  --admin-password "P@ssw0rd12345!"

# List all VMs in the active subscription
az vm list --output table

# Show details of a specific VM (including IP addresses)
az vm show --resource-group MyResourceGroup --name MyVM --show-details

# Get the public IP address of a VM
az vm list-ip-addresses --resource-group MyResourceGroup --name MyVM --output table

# Start, Stop, and Restart a VM
az vm start --resource-group MyResourceGroup --name MyVM
az vm stop --resource-group MyResourceGroup --name MyVM           # Stops OS but keeps resources allocated
az vm deallocate --resource-group MyResourceGroup --name MyVM     # Stops VM and releases hardware (recommended)
az vm restart --resource-group MyResourceGroup --name MyVM

# Resize a VM (requires listing available sizes first)
az vm list-sizes --resource-group MyResourceGroup --name MyVM --output table
az vm resize --resource-group MyResourceGroup --name MyVM --size Standard_D4s_v5

# Run a custom script on a Linux VM using Run Command
az vm run-command invoke \
  --resource-group MyResourceGroup \
  --name MyVM \
  --command-id RunShellScript \
  --scripts "apt-get update && apt-get install -y nginx"
```

### VM Scale Sets (`az vmss`)

```bash
# Create a VMSS with 3 instances
az vmss create \
  --resource-group MyResourceGroup \
  --name MyVMSS \
  --image Ubuntu2204 \
  --instance-count 3 \
  --admin-username azureuser \
  --generate-ssh-keys

# Scale the VMSS to 5 instances
az vmss scale --resource-group MyResourceGroup --name MyVMSS --new-capacity 5

# Update instances to the latest model
az vmss update-instances --resource-group MyResourceGroup --name MyVMSS --instance-ids "*"
```

---

## 4. Networking (`az network`)

Manage Virtual Networks (VNets), subnets, Network Security Groups (NSGs), public IPs, and Load Balancers.

### VNets & Subnets

```bash
# Create a Virtual Network (VNet) with a default subnet
az network vnet create \
  --resource-group MyResourceGroup \
  --name MyVNet \
  --address-prefixes 10.0.0.0/16 \
  --subnet-name MySubnet \
  --subnet-prefixes 10.0.1.0/24

# Create an additional Subnet in an existing VNet
az network vnet subnet create \
  --resource-group MyResourceGroup \
  --vnet-name MyVNet \
  --name MyBackendSubnet \
  --address-prefixes 10.0.2.0/24
```

### Network Security Groups (NSGs)

```bash
# Create an NSG
az network nsg create --resource-group MyResourceGroup --name MyNSG

# Associate NSG with an existing subnet
az network vnet subnet update \
  --resource-group MyResourceGroup \
  --vnet-name MyVNet \
  --name MySubnet \
  --network-security-group MyNSG

# Create a security rule allowing inbound SSH (port 22)
az network nsg rule create \
  --resource-group MyResourceGroup \
  --nsg-name MyNSG \
  --name AllowSSH \
  --priority 100 \
  --destination-port-ranges 22 \
  --protocol Tcp \
  --access Allow

# Create a security rule allowing inbound HTTP (port 80)
az network nsg rule create \
  --resource-group MyResourceGroup \
  --nsg-name MyNSG \
  --name AllowHTTP \
  --priority 110 \
  --destination-port-ranges 80 \
  --protocol Tcp \
  --access Allow
```

### Public IPs & Load Balancers

```bash
# Create a static Public IP Address (Standard SKU)
az network public-ip create \
  --resource-group MyResourceGroup \
  --name MyPublicIP \
  --sku Standard \
  --allocation-method Static

# Create a Public Azure Load Balancer
az network lb create \
  --resource-group MyResourceGroup \
  --name MyLoadBalancer \
  --sku Standard \
  --public-ip-address MyPublicIP \
  --frontend-ip-name MyFrontEndIP \
  --backend-pool-name MyBackEndPool
```

---

## 5. Storage Accounts (`az storage`)

Manage Azure Storage Accounts, blob containers, file shares, and Shared Access Signatures (SAS).

### Storage Account Management

```bash
# Create a storage account
az storage account create \
  --resource-group MyResourceGroup \
  --name mystorageaccountname \
  --location eastus \
  --sku Standard_LRS \
  --kind StorageV2

# List connection string (highly sensitive)
az storage account show-connection-string \
  --resource-group MyResourceGroup \
  --name mystorageaccountname \
  --output table

# Retrieve access keys
az storage account keys list \
  --resource-group MyResourceGroup \
  --name mystorageaccountname
```

### Blob Storage (Containers & Files)

```bash
# Create a blob container
az storage container create \
  --name mycontainer \
  --account-name mystorageaccountname

# Upload a file to a blob container
az storage blob upload \
  --account-name mystorageaccountname \
  --container-name mycontainer \
  --name myfile.txt \
  --file /path/to/local/file.txt

# List blobs in a container
az storage blob list \
  --account-name mystorageaccountname \
  --container-name mycontainer \
  --output table

# Download a blob from a container
az storage blob download \
  --account-name mystorageaccountname \
  --container-name mycontainer \
  --name myfile.txt \
  --file /path/to/downloaded/file.txt

# Generate a SAS Token for a container (valid for 2 hours)
az storage container generate-sas \
  --account-name mystorageaccountname \
  --name mycontainer \
  --permissions r \
  --expiry 2026-08-13T10:15:30Z
```

### Azure File Shares

```bash
# Create a file share
az storage share create \
  --account-name mystorageaccountname \
  --name myfileshare \
  --quota 100 # Quota in GB

# Upload a file to a file share
az storage file upload \
  --account-name mystorageaccountname \
  --share-name myfileshare \
  --source /path/to/local/file.txt
```

---

## 6. Microsoft Entra ID / Azure AD (`az ad`)

Manage users, groups, application registrations, and role-based access control (RBAC).

### Users & Groups

```bash
# List Entra ID users
az ad user list --output table

# Create a new user
az ad user create \
  --display-name "John Doe" \
  --user-principal-name "johndoe@yourtenant.onmicrosoft.com" \
  --password "P@ssw0rd12345!" \
  --force-change-password-next-sign-in

# Create a group
az ad group create --display-name "CloudEngineers" --mail-nickname "cloudengineers"

# Add a user to a group
az ad group member add --group "CloudEngineers" --member-id <user-object-id>
```

### App Registrations & Service Principals

```bash
# Create an App Registration
az ad app create --display-name "MyAPIApp" --web-redirect-uris "https://localhost:5001"

# Create a Service Principal for an App Registration
az ad sp create-for-rbac \
  --name "MyServicePrincipal" \
  --role Contributor \
  --scopes /subscriptions/<subscription-id>/resourceGroups/MyResourceGroup
```

### Role Assignments (RBAC)

```bash
# Assign "Reader" role to a user for a specific resource group
az role assignment create \
  --assignee "johndoe@yourtenant.onmicrosoft.com" \
  --role Reader \
  --resource-group MyResourceGroup

# List role assignments for a resource group
az role assignment list --resource-group MyResourceGroup --output table
```

---

## 7. App Services & Functions (`az webapp` & `az functionapp`)

Deploy web applications and serverless Azure Functions.

```bash
# Create an App Service Plan (Linux, Basic tier)
az appservice plan create \
  --resource-group MyResourceGroup \
  --name MyAppServicePlan \
  --sku B1 \
  --is-linux

# Create a Web App (Python 3.10 runtime)
az webapp create \
  --resource-group MyResourceGroup \
  --plan MyAppServicePlan \
  --name MyUniqueWebAppName \
  --runtime "PYTHON:3.10"

# List Web Apps in a Resource Group
az webapp list --resource-group MyResourceGroup --output table

# Configure Application Settings (Environment Variables)
az webapp config appsettings set \
  --resource-group MyResourceGroup \
  --name MyUniqueWebAppName \
  --settings DB_HOST="db.example.com" DB_USER="admin"

# Create a Function App (Python serverless, Consumption plan)
az functionapp create \
  --resource-group MyResourceGroup \
  --name MyUniqueFunctionAppName \
  --storage-account mystorageaccountname \
  --consumption-plan-location eastus \
  --functions-version 4 \
  --os-type Linux \
  --runtime python
```

---

## 8. Containers & Kubernetes (`az acr` & `az aks`)

Manage Azure Container Registry (ACR) and Azure Kubernetes Service (AKS).

### Azure Container Registry (`az acr`)

```bash
# Create an Azure Container Registry (Basic SKU)
az acr create \
  --resource-group MyResourceGroup \
  --name myacrregistryname \
  --sku Basic

# Log into ACR via Docker CLI
az acr login --name myacrregistryname

# List repositories in the ACR
az acr repository list --name myacrregistryname --output table
```

### Azure Kubernetes Service (`az aks`)

```bash
# Create an AKS cluster with 2 nodes and attach ACR
az aks create \
  --resource-group MyResourceGroup \
  --name MyAKSCluster \
  --node-count 2 \
  --generate-ssh-keys \
  --attach-acr myacrregistryname

# Download kubernetes credentials (updates ~/.kube/config)
az aks get-credentials --resource-group MyResourceGroup --name MyAKSCluster

# Scale the AKS cluster to 5 nodes
az aks scale \
  --resource-group MyResourceGroup \
  --name MyAKSCluster \
  --node-count 5

# Enable the cluster autoscaler
az aks update \
  --resource-group MyResourceGroup \
  --name MyAKSCluster \
  --enable-cluster-autoscaler \
  --min-count 2 \
  --max-count 10
```

---

## 9. Databases (`az sql`, `az cosmosdb` & `az postgres`)

Provision and manage Azure database engines.

```bash
# Create an Azure SQL Server
az sql server create \
  --resource-group MyResourceGroup \
  --name mysqlserverdb \
  --admin-user sqladmin \
  --admin-password "P@ssw0rd12345!"

# Create an Azure SQL Database (Basic service tier)
az sql db create \
  --resource-group MyResourceGroup \
  --server mysqlserverdb \
  --name mySampleDatabase \
  --edition Basic

# Create a Cosmos DB account (SQL API)
az cosmosdb create \
  --resource-group MyResourceGroup \
  --name mycosmosdbaccount

# Create a PostgreSQL Flexible Server
az postgres flexible-server create \
  --resource-group MyResourceGroup \
  --name mypgserver \
  --admin-user pgadmin \
  --admin-password "P@ssw0rd12345!" \
  --sku-name Standard_D2ds_v4
```

---

## 10. Monitoring & Governance (`az monitor`, `az policy` & `az lock`)

Enable continuous compliance, alerting, and monitoring of resources.

```bash
# Create a Log Analytics Workspace
az monitor log-analytics workspace create \
  --resource-group MyResourceGroup \
  --workspace-name MyWorkspace

# Create a Resource Lock to prevent deletion
az lock create \
  --name DoNotDeleteLock \
  --resource-group MyResourceGroup \
  --lock-type CanNotDelete \
  --notes "Prevent accidental deletion of this production resource group"

# Delete a Resource Lock
az lock delete --name DoNotDeleteLock --resource-group MyResourceGroup

# List Azure Policy definitions
az policy definition list --query "[?policyType=='BuiltIn'].{Name:displayName, Id:id}" --output table
```
