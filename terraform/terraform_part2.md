# Terraform 250 Interview Questions & Answers - Part 2 (Q91 - Q170)

This document is Part 2 of the comprehensive Terraform interview questions series, covering State Management, Providers, Modules, and intermediate HCL loops and graphs.

---

## 📋 Table of Contents
*   [State Management & Backends (Q91 - Q120)](#state-management--backends-q91---q120)
*   [Providers & Registry (Q121 - Q140)](#providers--registry-q121---q140)
*   [Module Architecture & Best Practices (Q141 - Q170)](#module-architecture--best-practices-q141---q170)

---

## State Management & Backends (Q91 - Q120)

#### Q91: What is the primary purpose of the Terraform state file?
**Answer:** To store metadata about your infrastructure resources, mapping your HCL configurations to actual physical resources, tracking dependencies, and caching resource attributes.

#### Q92: Why should you never edit the state file (`.tfstate`) manually?
**Answer:** The state file uses a strict JSON schema tracked by checksum hashes. Manual modifications can break references, desynchronize state mappings, or corrupt the file, crashing Terraform commands.

#### Q93: How do you configure a GCS (Google Cloud Storage) remote backend?
**Answer:**
```hcl
terraform {
  backend "gcs" {
    bucket = "my-tf-state-bucket"
    prefix = "terraform/state"
  }
}
```

#### Q94: How do you configure an AWS S3 remote backend with DynamoDB locking?
**Answer:**
```hcl
terraform {
  backend "s3" {
    bucket         = "my-tf-state-s3"
    key            = "global/s3/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

#### Q95: What happens when you migrate backends?
**Answer:** Running `terraform init` detects the backend change and prompts the user to copy their existing local state data to the new remote storage backend.

#### Q96: What does the `terraform state push` command do?
**Answer:** Manually writes a state file to a backend, overriding checksum protections. Primarily used during disaster recovery or state restorations.

#### Q97: What is a state lock timeout, and how do you configure it?
**Answer:** The time Terraform waits for a lock to clear if another run is active. Configured via the `-lock-timeout` flag: `terraform apply -lock-timeout=3m`.

#### Q98: Can you disable state locking during a run?
**Answer:** Yes, by adding `-lock=false`, but this is highly discouraged because it risks state corruption.

#### Q99: How do you force release a stuck state lock?
**Answer:** Retrieve the Lock Info ID from the terminal error and run: `terraform force-unlock <LOCK_ID>`.

#### Q100: How do you reference outputs from another independent Terraform configuration?
**Answer:** Using the `terraform_remote_state` data source:
```hcl
data "terraform_remote_state" "network" {
  backend = "gcs"
  config = {
    bucket = "network-state-bucket"
    prefix = "env/prod"
  }
}
# Reference via: data.terraform_remote_state.network.outputs.vpc_id
```

#### Q101: What is the threat of storing secrets in state files, and how do you secure them?
**Answer:** The state file stores sensitive values (like passwords, keys) in plain text JSON. You must encrypt the backend bucket (GCS/S3) and restrict read access using IAM permissions.

#### Q102: How do you remove a provider from the state file?
**Answer:** Run `terraform state replace-provider <old_provider> <new_provider>` or remove its resources using `terraform state rm`.

#### Q103: Does Terraform state store the history of changes?
**Answer:** No. It only stores the current actual state. Version history must be configured on the backend storage bucket (e.g., enabling Object Versioning in GCS or S3).

#### Q104: What is the purpose of the `moved` block in HCL?
**Answer:** To refactor code (like renaming resources or moving them into modules) without destroying and recreating them:
```hcl
moved {
  from = aws_instance.old_name
  to   = aws_instance.new_name
}
```

#### Q105: How does the `-refresh-only` flag affect planning?
**Answer:** It compares state to cloud infrastructure and updates the state file to reflect drift without proposing any infrastructure modifications.

#### Q106: What is a "partial configuration" backend?
**Answer:** Omitting backend parameters from code and passing them via environment variables or command-line files during `terraform init -backend-config=path/to/backend.hcl`.

#### Q107: Can a single Terraform workspace manage multiple state files?
**Answer:** No. Each workspace maintains exactly one isolated state file, though switching workspaces changes which state file is active.

#### Q108: How do you clean up local backup state files?
**Answer:** If using a remote backend, local backups are not created. For local backends, they can be deleted manually once the main state file is verified.

#### Q109: What does the `terraform state pull` command do?
**Answer:** Downloads the current state from the remote backend and outputs it directly to the terminal stdout.

#### Q110: Explain the purpose of state metadata in JSON state files.
**Answer:** It stores the schema version, Terraform CLI version, serial count (incremented each write), and lineage UUID to track state identity.

#### Q111: How do you handle a scenario where cloud resources are deleted outside Terraform?
**Answer:** Running `terraform plan` queries the APIs, detects the missing resources, and updates the plan to recreate them to match your configuration.

#### Q112: What does the command `terraform state mv` do?
**Answer:** Renames a resource address within the state file, helping with code refactoring: `terraform state mv aws_instance.web aws_instance.server`.

#### Q113: Is state locking supported by all backends?
**Answer:** No. Basic backends (like HTTP or local storage) may not support state locking. Services like GCS, S3 (with DynamoDB), and Terraform Cloud support locking.

#### Q114: How does the `.terraform.tfstate.lock.info` file work locally?
**Answer:** When running a command on a local backend, Terraform creates this file on disk to lock changes, deleting it once the operation completes.

#### Q115: What is "Drift Detection" in Terraform?
**Answer:** Identifying differences between the declared configuration, the state file, and the actual real-world infrastructure resources.

#### Q116: How do you run drift detection without applying changes?
**Answer:** Run `terraform plan`. It automatically refreshes state and shows any drift between code and cloud.

#### Q117: What does the serial number in a state file indicate?
**Answer:** An integer that increments on each successful state update. It is used to identify the sequence of state modifications.

#### Q118: How do you handle merge conflicts on state files managed in Git?
**Answer:** **Never store state files in Git**. Use remote backends. Git cannot automatically merge concurrent state JSON files.

#### Q119: What is the risk of using local state file backups in dynamic teams?
**Answer:** Desynchronization, where different developers overwrite each other's changes, leading to resource collisions or orphaned configurations.

#### Q120: Can you override the backend configuration in a sub-module?
**Answer:** No. Backends are configured at the root module level. Sub-modules cannot contain `backend` blocks.

---

## Providers & Registry (Q121 - Q140)

#### Q121: Where does Terraform look for provider plug-ins by default?
**Answer:** In the official HashiCorp Registry at `registry.terraform.io`.

#### Q122: How do you declare required provider requirements in HCL?
**Answer:**
```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}
```

#### Q123: Explain the `version = "~> 5.0"` syntax.
**Answer:** Pessimistic constraint: allows updates to patch and minor versions (e.g., `5.1`, `5.2`) but blocks upgrades to major versions (e.g., `6.0`).

#### Q124: What is the difference between official, partner, and community providers?
**Answer:** 
*   **Official**: Maintained directly by HashiCorp.
*   **Partner**: Maintained by the technology vendor (e.g., Datadog, Cloudflare).
*   **Community**: Maintained by individual open-source developers.

#### Q125: How do you install providers in environments without internet access?
**Answer:** Using a provider mirror (local directory caching) and configuring the filesystem mirror path in `.terraformrc`.

#### Q126: What is a "multi-provider" configuration?
**Answer:** Having resource blocks configured for different providers in the same file (e.g., creating a VM in GCP and attaching an AWS DNS route).

#### Q127: Explain the provider configuration block.
**Answer:** Configures provider credentials and regions:
```hcl
provider "google" {
  project = "my-gcp-project"
  region  = "us-central1"
}
```

#### Q128: What is a provider `alias` and how do you use it?
**Answer:** Used to declare multiple configurations for the same provider:
```hcl
provider "aws" {
  region = "us-east-1"
}
provider "aws" {
  alias  = "west"
  region = "us-west-2"
}
# Reference: provider = aws.west
```

#### Q129: What are provider custom plugins?
**Answer:** Custom compiled binaries executing custom API commands, stored in local folders (`~/.terraform.d/plugins/`).

#### Q130: What is the purpose of the `.terraform.lock.hcl` file?
**Answer:** A dependency lock file that locks the specific version and checksum hash of downloaded providers, ensuring team runs are identical.

#### Q131: Should `.terraform.lock.hcl` be committed to version control (Git)?
**Answer:** Yes. It ensures that everyone in the team downloads the exact same versions of providers.

#### Q132: What happens if you run `terraform init` and the lock file checksums mismatch?
**Answer:** Terraform raises a security warning and halts, protecting the system from running unverified provider binaries.

#### Q133: How do you update the dependency lock file for a new platform?
**Answer:** Run `terraform providers lock -platform=linux_amd64 -platform=darwin_arm64`.

#### Q134: How do you clean up cached provider plugins locally?
**Answer:** Delete the local `.terraform/` directory and run `terraform init` again to redownload them.

#### Q135: What is the difference between a resource schema and a provider schema?
**Answer:** 
*   **Resource Schema**: Defines the inputs/outputs of a specific resource.
*   **Provider Schema**: Defines the configurations needed to authenticate and initialize the provider itself.

#### Q136: How does Terraform manage provider binaries under the hood?
**Answer:** It runs them as separate background processes, communicating with them over gRPC channels.

#### Q137: Can you pass provider configurations dynamically from modules?
**Answer:** In modern Terraform, providers should be passed explicitly using the `providers` block mapping in module calls.

#### Q138: How do you find what provider versions are available?
**Answer:** Check the provider's page on the HashiCorp Terraform Registry.

#### Q139: Explain the `version = ">= 3.0, < 4.0"` constraint.
**Answer:** Restricts the provider version to be at least `3.0` but strictly lower than `4.0`.

#### Q140: What happens if you do not define a version constraint for a provider?
**Answer:** Terraform automatically downloads the latest available stable version of that provider during initialization.

---

## Module Architecture & Best Practices (Q141 - Q170)

#### Q141: What is the root module?
**Answer:** The primary directory containing the `.tf` configuration files executed by the Terraform CLI commands.

#### Q142: What is a child module?
**Answer:** A separate configuration folder called by the root module using a `module` block, allowing for code reusability.

#### Q143: How do you call a module located in a local directory?
**Answer:**
```hcl
module "vpc" {
  source = "./modules/vpc"
  cidr   = "10.0.0.0/16"
}
```

#### Q144: How do you call a module located on GitHub?
**Answer:**
```hcl
module "web" {
  source = "github.com/hashicorp/example"
}
```

#### Q145: How do you reference specific versions of a module from the Terraform Registry?
**Answer:**
```hcl
module "consul" {
  source  = "hashicorp/consul/aws"
  version = "0.1.0"
}
```

#### Q146: Why should you pin module versions?
**Answer:** To prevent accidental breaking changes if the module owner publishes a new version with incompatible schemas.

#### Q147: Explain the concept of "Module Inputs".
**Answer:** Input variables defined within the child module that must be passed by the calling parent configuration.

#### Q148: Explain "Module Outputs".
**Answer:** Outputs declared inside the child module, exposing attributes of the child module's internal resources to the parent configuration.

#### Q149: How do you reference resources created inside a child module?
**Answer:** You cannot access internal attributes directly. The child module must explicitly expose the attribute as an `output` block, referenced via `module.<name>.<output>`.

#### Q150: What is the main design pattern for building reusable modules?
**Answer:** Keep modules focused on a single architectural component (e.g., a "database module" or a "networking module"), rather than combining the entire infrastructure into one module.

#### Q151: How do you pass a provider to a child module?
**Answer:**
```hcl
module "gcp_infra" {
  source    = "./modules/infra"
  providers = {
    google = google.beta
  }
}
```

#### Q152: Explain the `count` meta-argument inside a module call.
**Answer:** Allows you to instantiate the entire module multiple times:
```hcl
module "app_server" {
  source = "./modules/server"
  count  = 3
}
# Access outputs via: module.app_server[0].ip
```

#### Q153: Explain the `for_each` meta-argument inside a module call.
**Answer:** Similar to `count`, but uses a map or set to create multiple module instances with distinct keys:
```hcl
module "env_subnets" {
  source   = "./modules/subnet"
  for_each = toset(["dev", "staging", "prod"])
}
```

#### Q154: Can you use both `count` and `for_each` in a single resource block?
**Answer:** No. They are mutually exclusive. You must choose one strategy to replicate resources.

#### Q155: What is the difference between `count.index` and `each.key`?
**Answer:** 
*   `count.index`: Represents the integer offset (0, 1, 2) when using `count`.
*   `each.key` / `each.value`: Represents the key or value of the current iteration when using `for_each`.

#### Q156: How do you handle dynamic resource properties (e.g., security group rules)?
**Answer:** Using the `dynamic` block pattern to generate nested blocks dynamically:
```hcl
dynamic "ingress" {
  for_each = var.ports
  content {
    from_port   = ingress.value
    to_port     = ingress.value
    protocol    = "tcp"
  }
}
```

#### Q157: What does the `path.module` expression represent?
**Answer:** The filesystem path where the current module configuration file is located.

#### Q158: What is the difference between `path.module`, `path.root`, and `path.cwd`?
**Answer:** 
*   `path.module`: The path of the module where the expression resides.
*   `path.root`: The path of the root module.
*   `path.cwd`: The current working directory from which Terraform was executed.

#### Q159: What is a "flat" module design?
**Answer:** Placing all resource configurations in a single directory without nested sub-directories, keeping files easy to trace.

#### Q160: Explain "Module Composition".
**Answer:** Combining multiple small, focused modules together inside a root configuration to build a complex target system.

#### Q161: How do you create an optional input variable inside a module?
**Answer:** By defining a `default` value (such as `null` or an empty string) in the variable declaration block.

#### Q162: What is the benefit of publishing modules to a private registry?
**Answer:** Enables organization-wide governance, sharing secure templates, and tracking code ownership.

#### Q163: How does Terraform download remote modules?
**Answer:** The `terraform init` command clones the module source code from its VCS target (e.g., Git) and caches it in local folders.

#### Q164: Can a module output reference resources created in other modules?
**Answer:** Only if those attributes are passed in as input variables first. Modules have isolated scopes.

#### Q165: What is the risk of having too many nested modules?
**Answer:** High complexity, making configurations hard to read, debug, and maintain.

#### Q166: Explain the difference between `var` and `local` scopes in modules.
**Answer:** 
*   `var`: Passed by the calling code to customize the module run.
*   `local`: Internal module computations hidden from the calling parent.

#### Q167: How do you configure a module source from a private Git repository?
**Answer:** Use SSH git paths: `git::ssh://git@github.com/myorg/myrepo.git`.

#### Q168: How do you target a specific tag in a Git module source?
**Answer:** Append `?ref=tag_name` to the source path: `source = "git::https://github.com/org/repo.git?ref=v1.2.0"`.

#### Q169: Can a module contain a backend configuration?
**Answer:** No. Backends must only be configured in the root module.

#### Q170: What does the `terraform get` command do?
**Answer:** Downloads and updates child modules referenced in the root module without initializing other backend structures.
