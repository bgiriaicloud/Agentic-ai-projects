# Terraform 250 Interview Questions & Answers - Part 1 (Q1 - Q90)

This document is Part 1 of the comprehensive Terraform interview questions series, covering core infrastructure-as-code principles, HashiCorp Configuration Language (HCL) syntax, basic CLI commands, and execution lifecycles.

---

## 📋 Table of Contents
*   [Core IaC & Terraform Foundations (Q1 - Q30)](#core-iac--terraform-foundations-q1---q30)
*   [HCL Syntax, Variables & Outputs (Q31 - Q60)](#hcl-syntax-variables--outputs-q31---q60)
*   [Execution Lifecycle & CLI Commands (Q61 - Q90)](#execution-lifecycle--cli-commands-q61---q90)

---

## Core IaC & Terraform Foundations (Q1 - Q30)

#### Q1: What is Infrastructure as Code (IaC)?
**Answer:** The practice of managing and provisioning computer data centers through machine-readable definition files, rather than physical hardware configuration or interactive configuration tools.

#### Q2: What is Terraform?
**Answer:** An open-source infrastructure as code software tool created by HashiCorp that enables users to define and provision data center infrastructure using a declarative configuration language.

#### Q3: Is Terraform declarative or imperative?
**Answer:** Declarative. Users write configurations describing the desired end-state of the infrastructure, and Terraform figures out how to achieve that state.

#### Q4: What is HashiCorp Configuration Language (HCL)?
**Answer:** A human-readable configuration language designed for use in HashiCorp tools, particularly Terraform, optimized for structural configurations.

#### Q5: What is the difference between Terraform and Ansible?
**Answer:** 
*   **Terraform**: Primarily an infrastructure provisioning tool (orchestrator) focused on creating resources.
*   **Ansible**: Primarily a configuration management and application deployment tool focused on setting up software on existing servers.

#### Q6: What is a "Resource" in Terraform?
**Answer:** The most important element in the Terraform language. Resources represent physical or virtual components of your infrastructure, such as virtual machines, VPC networks, or DNS records.

#### Q7: Explain the concept of "Data Sources" in Terraform.
**Answer:** Data sources allow data to be fetched or computed for use elsewhere in a Terraform configuration. They read read-only information from external APIs or existing infrastructure.

#### Q8: What is a "Provider" in Terraform?
**Answer:** A plug-in that translates Terraform commands into API calls for a specific platform or service (e.g., AWS, GCP, Azure, Kubernetes).

#### Q9: How does Terraform know which resources to create, update, or delete?
**Answer:** It compares the declared state in your configuration files with the actual state stored in the `terraform.tfstate` file and computes the diff plan.

#### Q10: What is the default file extension for Terraform configurations?
**Answer:** `.tf` (or `.tf.json` for JSON-formatted configurations).

#### Q11: What is the purpose of the `.terraform` directory?
**Answer:** It is a local cache directory created during initialization (`terraform init`) that holds downloaded provider plugins, module source code, and backend settings.

#### Q12: What is the Terraform Registry?
**Answer:** A centralized public repository hosted by HashiCorp containing community and official providers and modules to bootstrap configurations.

#### Q13: What is a Terraform Module?
**Answer:** A container for multiple resources that are used together. A module consists of a collection of `.tf` files in a single directory.

#### Q14: Explain the difference between local and remote backends.
**Answer:** 
*   **Local Backend**: Stores the state file on the local disk running the CLI commands.
*   **Remote Backend**: Stores the state file in a remote shared service (e.g., GCS, AWS S3, Consul) to enable collaboration and locking.

#### Q15: What is "State Locking" and why is it important?
**Answer:** A mechanism that prevents multiple users from executing Terraform commands simultaneously on the same state file, preventing state corruption.

#### Q16: What is a "Backend" in Terraform?
**Answer:** The configuration that determines where Terraform stores its state file and how it executes operations.

#### Q17: What does "Idempotency" mean in the context of Terraform?
**Answer:** The property that running the same Terraform configuration multiple times yields the exact same infrastructure state without unnecessary resource recreation.

#### Q18: What is a "Plan" in Terraform?
**Answer:** A generated execution dry-run showing what actions Terraform will take (create, modify, destroy) to align actual resources with your configuration files.

#### Q19: Explain the concept of "Implicit Dependencies" in Terraform.
**Answer:** Dependencies created automatically when a resource references an attribute of another resource (e.g., using `aws_instance.web.id` inside an IP attachment).

#### Q20: Explain the concept of "Explicit Dependencies".
**Answer:** Dependencies created manually using the `depends_on` meta-argument, telling Terraform to wait until a specific resource is ready before provisioning another.

#### Q21: What is the main advantage of using Terraform over cloud-native IaC tools?
**Answer:** It is platform-agnostic, supporting multi-cloud provisioning under a single syntax structure, whereas tools like CloudFormation (AWS) or ARM templates (Azure) are vendor-locked.

#### Q22: What is a "Variable" in Terraform?
**Answer:** Input parameters that allow configurations to be customized without editing the core code, acting like function arguments.

#### Q23: What is an "Output Value"?
**Answer:** Return parameters that expose resource attributes to the CLI console or pass data between different configurations or modules.

#### Q24: What is the role of `terraform.tfstate.backup`?
**Answer:** A backup copy of the state file created automatically by Terraform before updating the active state file during writes, facilitating recovery from errors.

#### Q25: Can you write Terraform files in JSON format?
**Answer:** Yes, files ending in `.tf.json` are parsed as JSON configurations, which is useful for programmatically generating code.

#### Q26: What is the purpose of the `locals` block?
**Answer:** To declare local values that act like private variables within a module, helping to avoid repeating complex expressions.

#### Q27: How does Terraform handle circular dependencies?
**Answer:** It raises an error. Terraform builds a Directed Acyclic Graph (DAG) to determine resource creation order; cycles make it impossible to resolve the execution path.

#### Q28: What is a "Provider Alias"?
**Answer:** A configuration that allows multiple configurations of the same provider to coexist (e.g., deploying resources to different AWS regions in a single run).

#### Q29: What is the difference between Terraform OSS and Terraform Cloud?
**Answer:** 
*   **OSS**: The free command-line interface tool.
*   **Cloud**: A hosted service providing remote state management, access controls, policy enforcement, and VCS integrations.

#### Q30: What is the purpose of the `required_version` setting?
**Answer:** Constrains the configuration to run only on approved versions of the Terraform CLI, preventing syntax incompatibility errors.

---

## HCL Syntax, Variables & Outputs (Q31 - Q60)

#### Q31: How do you declare an input variable?
**Answer:**
```hcl
variable "instance_count" {
  type    = number
  default = 2
}
```

#### Q32: What data types are supported for variables?
**Answer:** Primitive types (`string`, `number`, `bool`) and complex collection types (`list`, `set`, `map`, `object`, `tuple`).

#### Q33: How do you access a variable's value in a resource block?
**Answer:** Using the prefix `var.`, for example: `count = var.instance_count`.

#### Q34: What is the search precedence for loading variable values in Terraform?
**Answer:** 
1. Environment variables (`TF_VAR_name`).
2. The `terraform.tfvars` file.
3. The `terraform.tfvars.json` file.
4. Any `*.auto.tfvars` files.
5. Command-line flags (`-var` or `-var-file`).

#### Q35: How do you declare a sensitive variable?
**Answer:** By adding `sensitive = true` in the variable block, which prevents its value from being logged in console outputs.

#### Q36: How do you define a validation rule for a variable?
**Answer:** Using the `validation` block inside the variable definition:
```hcl
variable "ami_id" {
  type = string
  validation {
    condition     = length(var.ami_id) > 4 && substr(var.ami_id, 0, 4) == "ami-"
    error_message = "The ami_id value must start with \"ami-\"."
  }
}
```

#### Q37: What is the difference between a `list` and a `set` in Terraform?
**Answer:** 
*   **List**: An ordered sequence of values indexed by integers starting at 0.
*   **Set**: An unordered collection of unique values.

#### Q38: How do you reference an output value from a module?
**Answer:** Using `module.<MODULE_NAME>.<OUTPUT_NAME>`.

#### Q39: What are local values (`locals`)?
**Answer:** Temporary expressions assigned to a local name inside a module, declared using a `locals` block:
```hcl
locals {
  service_name = "forum"
  owner        = "community-team"
}
```

#### Q40: How do you reference a local value?
**Answer:** Using the `local.` prefix (e.g., `name = local.service_name`).

#### Q41: Explain string interpolation in HCL.
**Answer:** Embedding variable values or expressions inside a double-quoted string using the `${expression}` syntax.

#### Q42: What is the conditional operator in HCL?
**Answer:** The ternary operator: `condition ? true_val : false_val`.

#### Q43: How do you convert a string to uppercase in HCL?
**Answer:** Using the built-in function `upper(string)`.

#### Q44: What does the `lookup` function do?
**Answer:** Retrieves a value from a map given a key. If the key doesn't exist, it returns a default value: `lookup(map, key, default)`.

#### Q45: What does the `element` function do?
**Answer:** Retrieves a single element from a list at a given index: `element(list, index)`.

#### Q46: How do you declare a map variable?
**Answer:**
```hcl
variable "tags" {
  type = map(string)
  default = {
    environment = "prod"
    department  = "engineering"
  }
}
```

#### Q47: What is the purpose of the `output` block?
**Answer:** Exposes values to the terminal screen after `terraform apply` runs successfully, or exposes resource attributes to external scripts or parent modules.

#### Q48: How do you access values of a map variable?
**Answer:** Using square brackets or dot notation: `var.tags["environment"]` or `var.tags.environment`.

#### Q49: What is the difference between a tuple and an object?
**Answer:** 
*   **Tuple**: A sequence of fixed length where each element can have a different type.
*   **Object**: A structural map of key-value pairs where each key has a predefined type.

#### Q50: How do you comment code in Terraform files?
**Answer:** Single-line comments using `#` or `//`, and multi-line comments using `/* ... */`.

#### Q51: How do you join a list of strings into a single string?
**Answer:** Using the `join(separator, list)` function.

#### Q52: What is the result of `merge(map1, map2)`?
**Answer:** A single map containing keys and values from both inputs. If a key exists in both, the value from the second map overwrites the first.

#### Q53: Explain the `keys` and `values` functions.
**Answer:** 
*   `keys(map)` returns a list of keys in the map.
*   `values(map)` returns a list of values in the map.

#### Q54: What does the `coalesce` function do?
**Answer:** Returns the first non-empty/non-null value from a list of arguments.

#### Q55: Can you define nested modules?
**Answer:** Yes, modules can call other modules recursively to build hierarchical architecture patterns.

#### Q56: What does the `file` function do?
**Answer:** Reads the content of a local file at a given path as a string: `file("${path.module}/config.json")`.

#### Q57: What is the purpose of `templatefile`?
**Answer:** Reads a template file, renders variables into it using string templates, and returns the result as a string.

#### Q58: How do you handle default variable values if you do not specify a default in HCL?
**Answer:** Terraform halts execution and interactively prompts the user for inputs at the command line.

#### Q59: How do you pass variables via environment flags?
**Answer:** Export them with the `TF_VAR_` prefix: `export TF_VAR_instance_type="t3.medium"`.

#### Q60: Explain the `any` type constraint.
**Answer:** A placeholder type indicating that any value type is acceptable, letting Terraform deduce the structure dynamically.

---

## Execution Lifecycle & CLI Commands (Q61 - Q90)

#### Q61: What is the `terraform init` command?
**Answer:** The initialization step that reads configuration files, sets up backend storage drivers, and downloads required provider plug-ins.

#### Q62: What happens if you run `terraform init -upgrade`?
**Answer:** Terraform checks the registry for newer versions of providers and modules that fit the configuration bounds and upgrades them.

#### Q63: What does `terraform plan` do?
**Answer:** Generates a read-only execution plan outlining the steps to transition the target infrastructure to match the configuration files.

#### Q64: What is the benefit of the `-out` flag in `terraform plan`?
**Answer:** Saves the execution plan to a file, ensuring that the subsequent `terraform apply` executes the exact plan generated during analysis.

#### Q65: What does `terraform apply` do?
**Answer:** Executes the steps outlined in the plan to create, modify, or destroy infrastructure, updating the state file.

#### Q66: How do you bypass the interactive approval prompt during `terraform apply`?
**Answer:** By adding the `-auto-approve` flag: `terraform apply -auto-approve`.

#### Q67: What does `terraform destroy` do?
**Answer:** Evicts and terminates all infrastructure resources tracked in the current configuration's state file.

#### Q68: What does `terraform validate` do?
**Answer:** Verifies the configuration's HCL syntax and internal references, ensuring formatting is correct without querying APIs.

#### Q69: Explain the `terraform fmt` command.
**Answer:** Rewrites Terraform configuration files into a canonical format to maintain style consistency across files.

#### Q70: What does `terraform show` do?
**Answer:** Displays a human-readable summary of the current state file or a saved execution plan file.

#### Q71: What is the purpose of the `terraform output` command?
**Answer:** Extracts and prints defined output variables from the current state file.

#### Q72: Explain the command `terraform refresh`.
**Answer:** Queries active cloud provider APIs to update the state file with the actual current state of resources, without applying updates.

#### Q73: Why is `terraform refresh` deprecated in newer versions?
**Answer:** Its functionality has been integrated into plan operations. Use `terraform plan -refresh-only` to update state safe states.

#### Q74: What does the command `terraform console` do?
**Answer:** Opens an interactive command-line console to test HCL expressions, variables, and built-in functions.

#### Q75: How do you limit a Terraform execution to a specific resource?
**Answer:** Using the `-target` flag: `terraform apply -target=aws_instance.web`.

#### Q76: Why is using `-target` discouraged in production?
**Answer:** It bypasses dependency checks and can create inconsistencies in the state file.

#### Q77: What does `terraform graph` do?
**Answer:** Outputs a visual representation of the dependency graph of your configuration in DOT format.

#### Q78: Explain the `terraform providers` command.
**Answer:** Dumps a schema list of the provider plug-ins required by the current configuration.

#### Q79: How do you delete a specific resource from the state file without deleting the cloud resource?
**Answer:** Run `terraform state rm <resource_address>`.

#### Q80: What does `terraform import` do?
**Answer:** Imports existing real-world cloud resources into your Terraform state file, letting you manage existing infrastructure via IaC.

#### Q81: Does `terraform import` write configuration code automatically?
**Answer:** No. It only imports the resource state. The user must manually write the matching resource configuration code.

#### Q82: How do you check if your local files have correct formatting before committing?
**Answer:** Run `terraform fmt -check`, which returns an exit code of 0 if formatted correctly, or prints unformatted files.

#### Q83: What is the purpose of `terraform state show`?
**Answer:** Prints the detailed attribute configuration of a specific resource tracked inside the state file.

#### Q84: What does `terraform state list` do?
**Answer:** Outputs a list of all resource addresses currently tracked in the state file.

#### Q85: What happens if a command crashes during `terraform apply`?
**Answer:** Terraform saves the state of all successfully created resources up to that point. The next run will attempt to finish the remaining tasks.

#### Q86: What is the function of the `-var-file` flag?
**Answer:** Loads variable values from a specific file: `terraform apply -var-file="prod.tfvars"`.

#### Q87: What is the purpose of `terraform workspace`?
**Answer:** Manages multiple isolated states in a single directory, useful for managing development, staging, and production environments.

#### Q88: How do you list active workspaces?
**Answer:** Run `terraform workspace list`.

#### Q89: What is the command to create a new workspace?
**Answer:** Run `terraform workspace new <workspace_name>`.

#### Q90: How do you switch to a different workspace?
**Answer:** Run `terraform workspace select <workspace_name>`.
