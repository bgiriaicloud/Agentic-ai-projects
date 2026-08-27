# Terraform CLI Command Cheat Sheet

This document compiles the essential Terraform commands and flags used in daily cloud infrastructure administration.

---

## 📋 Table of Contents
1.  [Core Execution Lifecycle](#1-core-execution-lifecycle)
2.  [State File Management (`terraform state`)](#2-state-file-management-terraform-state)
3.  [Advanced Workflow & Refactoring](#3-advanced-workflow--refactoring)
4.  [Workspace Management](#4-workspace-management)
5.  [Command-Line Flags & Parameters](#5-command-line-flags--parameters)
6.  [Global Environment Variables](#6-global-environment-variables)

---

## 1. Core Execution Lifecycle

### `terraform init`
Initializes a working directory containing Terraform configuration files. Downloads provider plugins and configures backend storage.
```bash
# Upgrade downloaded providers/modules to the latest versions matching HCL constraints
terraform init -upgrade

# Re-configure the backend, ignoring existing state migrations
terraform init -reconfigure

# Pass backend configuration parameters dynamically (partial backend setup)
terraform init -backend-config="bucket=my-tf-state-bucket"
```

### `terraform validate`
Validates the syntax and consistency of HCL files in the directory.
```bash
terraform validate
```

### `terraform fmt`
Rewrites configuration files to canonical formatting and style.
```bash
# Formats all HCL files recursively in subdirectories
terraform fmt -recursive

# Checks if files are formatted, returning non-zero code if diffs exist
terraform fmt -check
```

### `terraform plan`
Generates an execution plan, comparing configuration with cloud infrastructure.
```bash
# Save the execution plan to a binary file
terraform plan -out=tfplan

# Refresh state and identify drift without showing infrastructure updates
terraform plan -refresh-only

# Generate plan using specific variable values
terraform plan -var="instance_type=t3.medium" -var-file="prod.tfvars"
```

### `terraform apply`
Applies the configuration changes to transition target cloud systems.
```bash
# Apply a pre-saved execution plan file (guarantees exact actions)
terraform apply tfplan

# Apply changes automatically, bypassing the interactive confirmation prompt
terraform apply -auto-approve

# Apply changes but skip updating state data from cloud APIs (faster, higher risk)
terraform apply -refresh=false
```

### `terraform destroy`
Destroys all infrastructure managed by the current workspace configuration.
```bash
# Terminate all resources automatically without interactive confirmation
terraform destroy -auto-approve
```

---

## 2. State File Management (`terraform state`)

Used to inspect, modify, and repair the `terraform.tfstate` database file.

```bash
# List all resources currently tracked in the state file
terraform state list

# Show detailed attributes of a specific resource in the state file
terraform state show google_compute_instance.web_server

# Rename a resource address inside the state file (refactoring HCL names)
terraform state mv google_compute_instance.old_name google_compute_instance.new_name

# Delete a resource from the state file (retains actual resource in the cloud)
terraform state rm google_compute_instance.external_db

# Swap out provider namespaces inside the state file
terraform state replace-provider hashicorp/aws registry.example.com/org/aws
```

---

## 3. Advanced Workflow & Refactoring

### `terraform import`
Imports existing cloud infrastructure resources into the state database.
```bash
# Import an existing virtual machine by its resource address and Cloud ID
terraform import google_compute_instance.default projects/my-project/zones/us-central1-a/instances/my-vm
```

### `terraform state push` & `state pull`
```bash
# Download the remote state file directly to local terminal output
terraform state pull > backup.tfstate

# Manually upload a local state file to the configured remote backend
terraform state push backup.tfstate
```

### `terraform console`
Opens an interactive command-line shell to test HCL expressions, variables, and built-in functions.
```bash
terraform console
```

### `terraform graph`
Generates a visual representation of the configuration dependency graph in DOT format.
```bash
# Export the dependency graph to an image file (requires Graphviz installed)
terraform graph | dot -Tpng > graph.png
```

---

## 4. Workspace Management

Useful for separating states in a single codebase directory.

```bash
# List all workspaces in the current directory
terraform workspace list

# Create a new workspace and switch to it immediately
terraform workspace new staging

# Switch to a different workspace
terraform workspace select production

# Display the name of the current active workspace
terraform workspace show
```

---

## 5. Command-Line Flags & Parameters

These flags can be appended to `plan`, `apply`, and `destroy` commands:

*   **`-var='key=value'`**: Sets an input variable value.
*   **`-var-file="filename.tfvars"`**: Loads variable values from a specific file.
*   **`-target=resource_address`**: Limits operations to a single resource and its dependencies.
*   **`-replace=resource_address`**: Forces recreation (destroy & create) of a specific resource.
*   **`-parallelism=N`**: Sets the maximum number of concurrent operations (default: `10`).
*   **`-lock=false`**: Disables state locking (high risk of state corruption).
*   **`-lock-timeout=duration`**: Sets how long to wait for a state lock to clear (e.g., `-lock-timeout=5m`).

---

## 6. Global Environment Variables

Define these variables in your shell environment to control Terraform's behavior:

```bash
# Enable verbose debugging logs (TRACE, DEBUG, INFO, WARN, ERROR)
export TF_LOG=DEBUG

# Save verbose debugging logs directly to a file
export TF_LOG_PATH="./terraform-run.log"

# Define an input variable value (equivalent to -var)
export TF_VAR_project_id="my-gcp-project"

# Disable interactive prompts (equivalent to TF_INPUT=0, useful in CI/CD)
export TF_INPUT=0

# Prepend command-line arguments to all Terraform commands automatically
export TF_CLI_ARGS="-no-color"
```
