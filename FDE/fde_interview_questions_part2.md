# Forward Deployed Engineer (FDE) 200 Interview Questions & Answers - Part 2

This is Volume 2 of the FDE interview guide, containing **Questions 101 to 200**. It covers cloud containers, CI/CD and IaC automation, IAM security, observability, FinOps cost monitoring, client consulting, and core feedback loops.

---

## 📋 Table of Contents (Part 2)
1.  [GKE, Cloud Run & Container Operations for Agents (Q101 - Q125)](#1-gke-cloud-run--container-operations-for-agents-q101---q125)
2.  [DevOps pipelines & IaC (Terraform/Ansible) for FDE (Q126 - Q145)](#2-devops-pipelines--iac-terraformansible-for-fde-q126---q145)
3.  [Client-Side Security, IAM, Secrets & Compliance (Q146 - Q165)](#3-client-side-security-iam-secrets--compliance-q146---q165)
4.  [Observability, Logging, SRE & FinOps (Token Cost Control) (Q166 - Q180)](#4-observability-logging-sre--finops-token-cost-control-q166---q180)
5.  [Consultative, Case Studies & Product Feedback Loops (Q181 - Q200)](#5-consultative-case-studies--product-feedback-loops-q181---q200)

---

## 1. GKE, Cloud Run & Container Operations for Agents (Q101 - Q125)

#### Q101: What is a Container, and why do FDEs package agent workloads in Docker images?
**Answer:** A container is a lightweight, isolated process environment that shares the host OS kernel. Packaging agent workloads in Docker images ensures that all dependencies (SDKs, custom libraries, system runtimes) run identically on the client's local cluster and in their cloud staging and production environments.

#### Q102: Why is Google Cloud Run ideal for hosting SSE MCP servers?
**Answer:** Cloud Run is serverless, auto-scales based on incoming traffic, scales down to zero when idle (minimizing client costs), automatically manages SSL endpoints, and easily attaches to private VPC networks using Serverless VPC Access.

#### Q103: Explain the difference between GKE Standard and GKE Autopilot.
**Answer:** 
*   **GKE Standard**: Gives the engineer full control over node provisioning, operating systems, and custom VM size selections.
*   **GKE Autopilot**: Automatically provisions and manages nodes, scales the cluster based on active pod demands, applies security hardening, and charges only for running pod CPU/Memory footprints.

#### Q104: What is Workload Identity, and how does it secure GKE workloads?
**Answer:** A feature that maps Kubernetes Service Accounts (KSA) inside a cluster directly to Google Cloud Service Accounts (GSA), allowing GKE pods to authenticate to GCP APIs (like Vertex AI or BigQuery) using temporary, automatically rotated tokens instead of static JSON access keys.

#### Q105: How do you configure resource requests and resource limits for agent pods?
**Answer:** Under the pod specs container section, configure:
*   `requests`: CPU and Memory guarantees used by the scheduler to place pods.
*   `limits`: Maximum resource bounds; if an agent pod exceeds its memory limits, the kernel kills it with an **OOMKilled** (Out of Memory) exception.

#### Q106: What is a "Cold Start" in serverless environments, and how does an FDE mitigate it?
**Answer:** A cold start is the delay when a container spins up from zero instances to handle a request. FDEs mitigate it on Cloud Run by configuring a minimum instance parameter (e.g., `min-instances = 1`) to keep a warm container active at all times.

#### Q107: Explain the role of the Kubelet.
**Answer:** An agent running on each worker node that receives PodSpecs from the API server and ensures that the designated containers are running and healthy inside the node.

#### Q108: What is a Pod in Kubernetes?
**Answer:** The smallest deployable unit in Kubernetes, which can host one or more containers (e.g. an application container and a sidecar logging agent) sharing the same network namespace and storage volumes.

#### Q109: What is the difference between a Deployment and a StatefulSet?
**Answer:** 
*   **Deployment**: Manages stateless pods where instances are identical, exchangeable, and assigned random hostnames.
*   **StatefulSet**: Manages stateful pods where each instance gets a persistent, ordinal identifier (e.g. `agent-db-0`) and binds to its own dedicated persistent volume.

#### Q110: Explain the purpose of a DaemonSet.
**Answer:** It ensures that every single node in the cluster runs a copy of a designated pod (typically used for log forwarding, network routing, or node metrics monitoring).

#### Q111: What is a K8s Service, and what are its types?
**Answer:** An abstraction to expose an application running on a set of Pods as a network service. Types include ClusterIP (internal), NodePort (static port on nodes), LoadBalancer (cloud external load balancer), and ExternalName (DNS CNAME).

#### Q112: Explain the role of the Ingress resource and Ingress Controller.
**Answer:** The Ingress resource is a set of routing rules (HTTP/HTTPS) that exposes services to external traffic. The Ingress Controller (like NGINX or Google Cloud HTTP Load Balancer) acts as the reverse proxy that executes those routing rules.

#### Q113: What are Liveness and Readiness Probes in K8s?
**Answer:** 
*   **Liveness**: Determines if a container needs to be restarted. If it fails, Kubernetes kills the container and restarts it.
*   **Readiness**: Determines if a container is ready to accept network traffic. If it fails, the pod is removed from Service endpoint lists.

#### Q114: What is a Startup Probe, and why is it useful for heavy models?
**Answer:** A probe that checks if the application has completed its startup routine. It disables liveness and readiness checks until startup succeeds, preventing slow-starting containers (like those loading heavy weights) from getting killed during boot.

#### Q115: What is etcd?
**Answer:** A consistent, highly available distributed key-value store used as Kubernetes' storage backend for all cluster state and configuration data.

#### Q116: What is a ConfigMap vs a K8s Secret?
**Answer:** 
*   **ConfigMap**: Stores non-confidential configuration key-value blocks.
*   **Secret**: Stores sensitive data (keys, database passwords) encoded in base64, which can be encrypted at rest in etcd.

#### Q117: What is Horizontal Pod Autoscaler (HPA)?
**Answer:** A controller that automatically adjusts the replica count of a deployment or statefulset based on observed CPU utilization, memory thresholds, or custom metrics.

#### Q118: Explain Node Affinity.
**Answer:** A set of scheduling rules that constrains which nodes your Pod can schedule on, based on key-value labels defined on the nodes.

#### Q119: What are Taints and Tolerations?
**Answer:** 
*   **Taints**: Node configurations that repel sets of pods.
*   **Tolerations**: Pod configurations that allow (but do not force) pods to schedule on nodes with matching taints.

#### Q120: What is a Kubernetes Namespace?
**Answer:** A logical partition inside a single cluster used to organize resources, enforce scope boundaries, and isolate environments (e.g., dev, staging, prod).

#### Q121: What is a Sidecar Container?
**Answer:** A utility container that runs alongside the main application container inside the same pod, handling helper tasks like logging, security proxying (mTLS), or configuration syncing.

#### Q122: What is Helm?
**Answer:** A package manager for Kubernetes that templates YAML manifests into structured packages called Charts, simplifying deployment, upgrades, and versioning.

#### Q123: What is a NetworkPolicy in Kubernetes?
**Answer:** A resource that acts as a Layer 3/4 firewall inside the cluster, defining rules that control traffic flow between pod groups.

#### Q124: What is a Service Mesh (e.g., Istio)?
**Answer:** An infrastructure layer that manages service-to-service communication, providing load balancing, traffic splitting, mutual TLS encryption (mTLS), and detailed observability.

#### Q125: What is Google Artifact Registry?
**Answer:** A fully managed repository manager on Google Cloud used to store, version, and scan container images (Docker), OS packages, and language artifacts (Maven, npm).

---

## 2. DevOps pipelines & IaC (Terraform/Ansible) for FDE (Q126 - Q145)

#### Q126: What is Infrastructure as Code (IaC), and why does an FDE use it?
**Answer:** IaC is the management and provisioning of infrastructure using machine-readable configuration files instead of manual console clicks. FDEs use it to provision identical client environments (networks, buckets, databases) reliably.

#### Q127: What is the difference between Declarative and Imperative IaC?
**Answer:** 
*   **Declarative** (e.g., Terraform): You define the desired end state, and the tool calculates the steps to achieve it.
*   **Imperative** (e.g., Ansible, custom scripts): You define the step-by-step commands the tool must execute in order to build the system.

#### Q128: What is Terraform State, and why is it important?
**Answer:** The state file (`terraform.tfstate`) maps real-world infrastructure to your configuration files, tracking resource metadata and dependency relationships to calculate updates and deletions.

#### Q129: Explain the risk of keeping Terraform state files locally in production.
**Answer:** Local state blocks collaboration, can lead to state files being overwritten during concurrent runs, and can expose sensitive credentials in plain text. Use remote backends with state locking instead.

#### Q130: What is a Remote Backend in Terraform, and what GCP service supports it?
**Answer:** A remote backend stores the state file in a shared, secure location. **Google Cloud Storage (GCS)** is the default GCP service, which supports read/write encryption, versioning, and state locking.

#### Q131: What is the difference between Terraform and Ansible?
**Answer:** 
*   **Terraform**: An orchestration tool used to provision infrastructure components (networks, VMs, GKE clusters).
*   **Ansible**: A configuration management tool used to bootstrap, configure, and install software on already-running servers.

#### Q132: Explain what `terraform plan` does.
**Answer:** It compares your local code against the active state file and cloud infrastructure, generating an execution plan that lists all additions, modifications, and deletions without applying changes.

#### Q133: What is a Terraform Module?
**Answer:** A container for multiple resources used together, allowing you to package and reuse standard infrastructure patterns (like a hardened subnetwork with Cloud SQL instances) across multiple projects.

#### Q134: How do you prevent sensitive variables from leaking in Terraform CLI logs?
**Answer:** Mark the variable block as `sensitive = true`, which tells Terraform to mask the values in CLI plans, applies, and outputs.

#### Q135: What is `terraform apply -replace` (formerly taint)?
**Answer:** A command that marks a specific resource as degraded or out of sync, forcing Terraform to destroy and recreate it during the next deployment run.

#### Q136: What is a Null Resource in Terraform?
**Answer:** A resource that has no physical cloud presence, used to trigger local or remote execution scripts when specific variables or dependencies change.

#### Q137: Explain what an Ansible Playbook is.
**Answer:** A YAML configuration file where you define a sequence of configuration tasks (roles, package installs, configuration edits) to run on a set of target inventory hosts.

#### Q138: Explain the difference between agentless and agent-based configuration management.
**Answer:** 
*   **Agentless** (e.g., Ansible): Communicates directly with target nodes over standard SSH or WinRM connections without requiring local software daemons.
*   **Agent-based** (e.g., Puppet, Chef): Requires installing a local client agent on each target node to pull configuration updates from a master server.

#### Q139: What is a dynamic inventory in Ansible?
**Answer:** A script that queries cloud provider APIs (like GCP) dynamically to construct a list of target host IPs based on resource labels and tags instead of using static configuration files.

#### Q140: How does `terraform output` integrate with automated CI/CD pipelines?
**Answer:** It prints specific values (like a newly created database host IP or endpoint URL) in JSON or text formats, allowing shell scripts or subsequent pipeline stages to consume the output.

#### Q141: Explain CI/CD.
**Answer:** Continuous Integration (automated building and testing of code changes on commit) and Continuous Delivery/Deployment (automated staging and releasing of build artifacts to environments).

#### Q142: Explain the difference between Continuous Delivery and Continuous Deployment.
**Answer:** 
*   **Continuous Delivery**: The pipeline builds and tests code automatically, staging it for release, but the promotion to production requires a manual click.
*   **Continuous Deployment**: Removes manual checks; every commit that passes the pipeline gates is automatically pushed to production.

#### Q143: What is GitOps?
**Answer:** A methodology where Git is the single source of truth for infrastructure and application states, using an in-cluster controller (like ArgoCD) to sync active environments with Git definitions.

#### Q144: What is the purpose of an Artifact Repository in CI/CD?
**Answer:** It stores immutable build outputs (Docker images, zip binaries, packages), ensuring that the exact same tested code is deployed across staging and production.

#### Q145: What is a Canary Deployment?
**Answer:** A deployment strategy where updates are rolled out to a small subset of servers (e.g., 5% of traffic) to monitor error rates and performance before rolling them out to the rest of the network.

---

## 3. Client-Side Security, IAM, Secrets & Compliance (Q146 - Q165)

#### Q146: What is the Principle of Least Privilege (PoLP)?
**Answer:** A security practice where users, service accounts, and processes are granted only the minimum permissions necessary to perform their specific tasks, reducing the blast radius of a credential leak.

#### Q147: How does Google Cloud Secret Manager protect client credentials?
**Answer:** It stores sensitive strings (passwords, keys) encrypted at rest, integrates with IAM policies to restrict access, versions secrets automatically, and logs access events for audits.

#### Q148: What is the risk of hardcoding API keys in application source code?
**Answer:** Hardcoded keys are stored in plaintext and can easily be leaked to public repositories, compromised in build artifacts, or accessed by unauthorized developers. Use Secret Manager instead.

#### Q149: Explain "Confidential Computing" in Google Cloud.
**Answer:** An option that encrypts data in-memory while it is actively processed by the CPU, protecting workloads from node compromise.

#### Q150: What is IAM (Identity and Access Management)?
**Answer:** A security framework that manages digital identities and controls who (users/services) can perform what actions (roles) on which cloud resources.

#### Q151: What is the difference between Primitive, Predefined, and Custom Roles in GCP IAM?
**Answer:** 
*   **Primitive**: Broad, legacy roles (Owner, Editor, Viewer).
*   **Predefined**: Fine-grained roles managed by Google (e.g., Storage Object Creator).
*   **Custom**: Roles defined by the user that combine specific permissions for granular access control.

#### Q152: How do you secure data-in-transit?
**Answer:** Enforce TLS/HTTPS protocols for all API connections, configure SSL certificates on load balancers, and use mutual TLS (mTLS) in service meshes for secure pod-to-pod communication.

#### Q153: How do you secure data-at-rest in Google Cloud?
**Answer:** Google Cloud encrypts all customer data at rest by default using Google-managed encryption keys. You can also use Customer-Managed Encryption Keys (CMEK) via Cloud KMS for more control.

#### Q154: What is Customer-Managed Encryption Keys (CMEK) via Cloud KMS?
**Answer:** A key management service that allows customers to generate, rotate, and control their own encryption keys within GCP to encrypt data stored in services like Cloud Storage or BigQuery.

#### Q155: What is the role of an IAM Policy?
**Answer:** A JSON/YAML file attached to a resource that defines the bindings of members (identities) to roles, controlling access permissions.

#### Q156: Explain Multi-Factor Authentication (MFA).
**Answer:** A security mechanism requiring users to present two or more verification factors (something they know, have, or are) to authenticate, reducing identity compromise.

#### Q157: What is Single Sign-On (SSO)?
**Answer:** An authentication method that allows users to log in once with a single set of credentials and access multiple applications without re-authenticating.

#### Q158: Explain the purpose of OAuth 2.0.
**Answer:** An open standard authorization protocol that allows applications to access resources on behalf of a user without exposing their credentials.

#### Q159: What is "VPC Service Controls" (VPC-SC) on GCP?
**Answer:** A security service that defines a perimeter around Google Cloud APIs (such as BigQuery or Storage) to block data access requests originating from outside the perimeter.

#### Q160: What is a "Data Perimeter" in cloud security?
**Answer:** A security boundary that prevents unauthorized systems or networks from accessing data, even if they have valid IAM credentials.

#### Q161: How do you prevent prompt injection in production LLM applications?
**Answer:** Sanitize user inputs, enforce structured outputs (JSON schema), use safety filter settings, and run validation checks on tool arguments returned by the model.

#### Q162: What is "PII Sanitization," and why is it important before calling external LLMs?
**Answer:** The process of masking or removing Personally Identifiable Information (like SSNs or emails) from prompt data before sending it to public LLM APIs to maintain compliance.

#### Q163: What is SOC 2 Compliance?
**Answer:** An auditing standard that measures a service organization's controls across security, availability, processing integrity, confidentiality, and privacy.

#### Q164: Explain GDPR Compliance in AI contexts.
**Answer:** A regulation requiring organizations to protect the data privacy of EU residents, including the "right to be forgotten," which means ensuring users can request their data be removed from RAG indexes.

#### Q165: What is a "Zero Trust" security model?
**Answer:** A security framework that assumes no network or user is trusted by default, requiring continuous authentication, authorization, and validation for every access request.

---

## 4. Observability, Logging, SRE & FinOps (Token Cost Control) (Q166 - Q180)

#### Q166: What are the "Four Golden Signals" of SRE?
**Answer:** Latency (time to process requests), Traffic (demand load), Errors (rate of failed requests), and Saturation (system resource utilization).

#### Q167: What is the difference between Prometheus and Grafana?
**Answer:** 
*   **Prometheus**: A time-series database and monitoring tool that gathers metrics using a pull model.
*   **Grafana**: A visualization dashboard tool that queries data sources (like Prometheus) to build graphs and alerts.

#### Q168: Define SLI, SLO, and SLA.
**Answer:** 
*   **SLI**: A metric that measures service performance (e.g., latency < 200ms).
*   **SLO**: A target reliability goal for an SLI (e.g., 99.9% of requests meet the SLI).
*   **SLA**: The legal contract promising users a certain level of reliability, often including financial penalties if missed.

#### Q169: What is an Error Budget?
**Answer:** The maximum allowable reliability deficit of a system over a time window (e.g., if your SLO is 99.9% uptime, your error budget is 0.1% downtime). If the budget is exhausted, releases are halted to prioritize stability work.

#### Q170: Explain the difference between structured and unstructured logging.
**Answer:** 
*   **Structured**: Logs written in machine-readable formats (usually JSON) containing key-value pairs, allowing dashboards to query and aggregate metrics easily.
*   **Unstructured**: Text-based strings that are easy for humans to write but difficult for computers to parse.

#### Q171: What is APM (Application Performance Monitoring)?
**Answer:** APM tools (e.g., Dynatrace, New Relic, Datadog) monitor application code execution. They trace transaction call graphs, database queries, and function-level latencies to isolate bottlenecks.

#### Q172: What is Distributed Tracing?
**Answer:** A monitoring technique that tracks the lifecycle of a request as it flows across multiple microservices. A unique `trace_id` is passed in HTTP headers, allowing engineers to visualize call paths and identify which microservice caused a delay.

#### Q173: Explain the difference between Push and Pull metric gathering.
**Answer:** 
*   **Pull** (e.g., Prometheus): The monitor server queries target endpoints periodically to fetch metrics.
*   **Push** (e.g., StatsD, InfluxDB): The application pushed metrics directly to a collector server whenever an event occurs.

#### Q174: What is Log Rotation?
**Answer:** A process that manages the size of local log files. It archives older logs, compresses them, and eventually deletes them to prevent servers from running out of disk space.

#### Q175: What is "Alert Fatigue" in SRE, and how do you prevent it in AI platforms?
**Answer:** Alert fatigue occurs when operators are flooded with low-priority or false-positive alarms. Prevent it by using dynamic threshold alerting (anomaly detection) and grouping related alerts (e.g., grouping GKE CPU spikes with high agent token loads) instead of alerting on individual metrics.

#### Q176: Why is tracking "Thinking Tokens" critical for FinOps?
**Answer:** Reasoning models (like Gemini 3.5 Pro) use internal thinking tokens to solve complex planning tasks. Since these tokens are billed as output tokens but are not returned in the final user text, tracking them is essential for accurate cost estimation and budgeting.

#### Q177: How do you configure centralized audit logging for agents on GCP?
**Answer:** Configure Log Sinks to route all stdout/stderr logs from GKE and Cloud Run directly to **BigQuery** or **Cloud Logging**. This enables structured dashboards to monitor agent trajectories and detect anomalies.

#### Q178: What is "Cost Cap Enforcer" in agent design?
**Answer:** A guardrail logic inside the agent loop that monitors session token costs. If the cost exceeds a set limit (e.g., $2.00), the loop is terminated to prevent runaway queries.

#### Q179: What is "Confidential Computing" in Google Cloud?
**Answer:** An option that encrypts data in-memory while it is actively processed by the CPU, protecting workloads from node compromise.

#### Q180: How do you monitor API rate limits (quota limits) on Vertex AI?
**Answer:** Monitor `quota/exceeded_requests` metrics in Google Cloud Monitoring. Set up alerts at 80% quota usage to trigger automated scaling or request quota increases before failures occur.

---

## 5. Consultative, Case Studies & Product Feedback Loops (Q181 - Q200)

#### Q181: How do you handle a client stakeholder who insists on building a custom AI agent from scratch instead of using your platform?
**Answer:** I walk them through a cost-benefit analysis. I explain the maintenance overhead of building from scratch, emphasizing that using our platform saves them months of development time and allows their team to focus on core business value.

#### Q182: How do you communicate a critical platform limitation to a client?
**Answer:** I frame the limitation honestly and immediately offer alternative solutions. I explain what we can do to bypass the limitation (e.g., using an MCP bridge) and explain how the issue fits into our core product roadmap.

#### Q183: Explain the role of the FDE in the "Discover" phase of a client engagement.
**Answer:** The FDE conducts workshops, interviews stakeholders, maps out user workflows, and reviews data structures to identify the client's actual pain points and define a clear project scope.

#### Q184: How do you handle a client who requests a feature that deviates from your platform's core architecture?
**Answer:** I assess if the feature can be implemented using decoupled extensions (like custom APIs or plugins). If it requires architectural changes, I explain the maintenance risks to the client and work to align their goals with our standard design.

#### Q185: Why is the "Optimize" phase of the FDE lifecycle continuous?
**Answer:** System performance, user behavior, and data patterns change over time. Continuous monitoring during the Optimize phase allows the FDE to identify bottleneck trends, reduce token costs, and improve system accuracy iteratively.

#### Q186: How do you handle a situation where a client's security team blocks your deployment due to compliance concerns?
**Answer:** I schedule a meeting with their security team, provide detailed compliance documentation, and explain how we enforce security boundaries (e.g., using VPC-SC perimeters, Workload Identity, and CMEK encryption keys) to address their specific concerns.

#### Q187: How does an FDE feed customer learnings back to the core engineering team?
**Answer:** By documenting feature gaps, reporting bugs with reproducible test cases, and sharing client integration patterns in shared channels, helping core PMs prioritize roadmaps based on real-world usage.

#### Q188: What is a "Value Realization Dashboard"?
**Answer:** A custom dashboard (built during the Deliver Impact phase) that visualizes user adoption rates, API latencies, and business KPIs (like time saved or query accuracy) to demonstrate the ROI of the deployment to client executives.

#### Q189: How do you handle scope creep when a client asks for additional features mid-sprint?
**Answer:** I review the requested features against the SOW. If they are out of scope, I log them as future backlog items, explain the impact on the current timeline, and require a formal scope adjustment approval from the project sponsor.

#### Q190: What is a "User Acceptance Testing" (UAT) cycle?
**Answer:** A phase where the client's business users test the deployed system in a staging environment to verify that it meets all functional requirements and business objectives before it is promoted to production.

#### Q191: How do you manage a client deployment that fails during a live demo?
**Answer:** I stay calm, acknowledge the issue, pivot the presentation to walk through the system architecture or mock flows, and debug the issue immediately after the call, providing a detailed root cause analysis (RCA) to the client.

#### Q192: Why is "Developer Enablement" a key responsibility of an FDE?
**Answer:** It ensures the client's internal engineering team is trained to maintain, monitor, and extend the deployed system after the FDE transition, ensuring long-term project success and client independence.

#### Q193: How do you handle a client developer who resists adopting your platform?
**Answer:** I pair-program with them, demonstrate how the platform simplifies their workflows, address their technical concerns, and involve them in design decisions to build trust and collaboration.

#### Q194: What is a "Root Cause Analysis" (RCA) document?
**Answer:** A document created after a production incident that outlines the chronology of the failure, identifies the root cause, documents the resolution steps, and lists actions to prevent future occurrences.

#### Q195: How do you handle conflicting requirements from different client stakeholders?
**Answer:** I bring the stakeholders together in a alignment workshop, present the trade-offs of each requirement, and facilitate a consensus decision aligned with the project's core business goals.

#### Q196: What is a "Warm Handoff" to client operations?
**Answer:** A structured transition phase where the FDE delivers complete system documentation (architecture diagrams, runbooks), conducts training workshops, and monitors the client's team as they run the platform.

#### Q197: Why should an FDE track client user sentiment?
**Answer:** Technical metrics (like uptime) do not tell the whole story. If users find the interface confusing, adoption will drop, and the project will fail to deliver business value.

#### Q198: How do you design a "Rollback Runbook" for a client?
**Answer:** I write a step-by-step guide detailing how to restore the system to its previous stable state (e.g. reverting container tags, restoring database backups) if a deployment fails.

#### Q199: How do you prioritize tasks when managing multiple client engagements?
**Answer:** I prioritize based on project deadlines, contract value, and the severity of active blockers, maintaining transparent communication with project managers in each account.

#### Q200: What is the most rewarding part of being a Forward Deployed Engineer?
**Answer:** Seeing the direct impact of the software you write. Unlike core engineers who are decoupled from users, an FDE sits at the table as their code directly solves a client's business problems and improves their daily operations.
