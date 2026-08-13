# Enterprise Agentic AI Platform on Google Cloud: Planning & Deployment Guide

This guide provides an enterprise planning and deployment framework for implementing the **Agent Development Kit (ADK)**, **Model Context Protocol (MCP) Tools**, and **Agent-to-Agent (A2A) Integration** on Google Cloud Platform (GCP). It is structured directly around the phases of the **Implementation Roadmap: Enterprise Agentic AI Platform on Google Cloud**.

---

## 1. System Architecture

Below is the production-grade target architecture for deploying ADK Agents, MCP Servers, and A2A orchestration on GCP:

![GCP Agentic AI Architecture Diagram](/Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/gcp_architecture_diagram.png)

### Architectural Components Flowchart (Mermaid)
```mermaid
graph TD
    subgraph Enterprise Security Boundary (VPC Service Controls)
        subgraph Shared VPC / Subnets
            subgraph Google Kubernetes Engine (GKE Cluster)
                Supervisor[Supervisor Agent Core<br/>google-antigravity SDK]
                SubagentRegistry[A2A Agent Engine / Registry]
                K8sPod[Worker Agent Pods]
            end
            
            subgraph Serverless Network (Cloud Run)
                MCP_Jira[MCP Server: Jira Bridge]
                MCP_Slack[MCP Server: Slack Bridge]
            end
        end

        subgraph GCP Managed Services
            VertexAI[Vertex AI Gemini API<br/>gemini-3.5-flash]
            SecretManager[Secret Manager<br/>API Keys / Tool Credentials]
            PubSub[Cloud Pub/Sub<br/>A2A Asynchronous Task Delegation]
            BigQuery[BigQuery<br/>Observability & Audit Logs]
            ArtifactRegistry[Artifact Registry<br/>Container Images]
        end
    end

    %% Network Connections
    User([Platform Operator / Frontend]) -->|gRPC/HTTP| Supervisor
    Supervisor -->|Local RPC / REST| SubagentRegistry
    SubagentRegistry -->|Publish / Subscribe| PubSub
    PubSub -->|Trigger Task| K8sPod
    K8sPod -->|mTLS / SSE| MCP_Jira
    K8sPod -->|mTLS / SSE| MCP_Slack
    Supervisor -->|Vertex AI API| VertexAI
    MCP_Jira -->|IAM / Service Account| SecretManager
    Supervisor -->|Log Export| BigQuery
```

### AI Agentic User Workflow Sequence
![AI Agentic User Workflow](/Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/user_workflow_diagram.png)

---

## 2. Planning & Deployment Phases

### Phase 1: Foundation (Infrastructure Setup)
Before writing agent code, establish the GCP organizational hierarchy, networking, and storage components:
*   **Projects & Folders**: Separate your workloads into `agent-ai-dev`, `agent-ai-stage`, and `agent-ai-prod` under an `Agentic-Platform` folder.
*   **Shared VPC**: Build a Shared VPC with subnets dedicated to GKE worker nodes and Serverless VPC Access connectors (for Cloud Run to access internal networks).
*   **AlloyDB & BigQuery**:
    *   Deploy **AlloyDB** as the primary metadata database to store agent states and session histories.
    *   Initialize **BigQuery** datasets to serve as the destination for long-term token monitoring and execution logs.

---

### Phase 2: Agent Development (ADK)
Using the Google Antigravity SDK, we build our agents to run in containerized environments.

#### Key Principles:
1.  **Model Selection**: Default to `gemini-3.5-flash` for multi-agent routing and light reasoning due to its low latency and high context window. Utilize `gemini-3.5-pro` only for high-complexity planning tasks at the supervisor level.
2.  **Persona Configuration**: Custom personas are injected via `system_instructions` within `LocalAgentConfig`.
3.  **Local Tool Testing**: Run agents locally with environment variables before deploying to Kubernetes.

#### Sample Local Configuration (`config.py`):
```python
import os
from google.antigravity import LocalAgentConfig, types

def get_platform_agent_config(persona_instructions: str) -> LocalAgentConfig:
    return LocalAgentConfig(
        model="gemini-3.5-flash",  # Default and recommended model
        system_instructions=persona_instructions,
        capabilities=types.CapabilitiesConfig(
            enable_subagents=True  # Enables A2A spawning
        )
    )
```

---

### Phase 3: MCP Tool Integration (Deploying Custom Tools)
Model Context Protocol (MCP) servers run as decoupled microservices on Google Cloud Run. They expose enterprise integrations (Jira, Slack, databases) to the agent.

#### Deployment Checklist:
1.  **Transport Selection**: Locally, we test using Stdio. In GCP Production, we run MCP servers using **SSE (Server-Sent Events)** transport over HTTPS.
2.  **Secret Manager Setup**: Secure API keys, OAuth tokens, and database passwords in Secret Manager.
3.  **Artifact Registry**: Push Docker container images to a secure, regional Artifact Registry repo.
4.  **Cloud Run Deployment**: Run containers serverless with strict IAM controls.

#### GCP Commands:
```bash
# 1. Create Artifact Registry repository
gcloud artifacts repositories create mcp-servers \
    --repository-format=docker \
    --location=us-central1 \
    --description="Registry for MCP Server Docker images"

# 2. Store a secret (e.g. Jira API Token) in Secret Manager
gcloud secrets create JIRA_API_TOKEN --replication-policy="automatic"
echo -n "your-jira-api-token-value" | gcloud secrets versions add JIRA_API_TOKEN --data-file=-

# 3. Build and push container using Cloud Build
gcloud builds submit --tag us-central1-docker.pkg.dev/your-project-id/mcp-servers/jira-bridge:v1 .

# 4. Deploy the MCP server to Cloud Run, mounting the secret
gcloud run deploy mcp-jira-bridge \
    --image=us-central1-docker.pkg.dev/your-project-id/mcp-servers/jira-bridge:v1 \
    --region=us-central1 \
    --no-allow-unauthenticated \
    --set-env-vars=TRANSPORT=sse \
    --set-secrets=JIRA_API_TOKEN=JIRA_API_TOKEN:latest
```

---

### Phase 4: A2A Integration (Multi-Agent Orchestration)
To handle complex enterprise workloads, implement an Agent-to-Agent (A2A) delegation pattern using a **Supervisor Agent** that spawns specialized worker subagents.

```
                  ┌────────────────────┐
                  │  Supervisor Agent  │
                  └─────────┬──────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
    ┌──────────────────┐        ┌──────────────────┐
    │ Subagent: Coder  │        │ Subagent: SecOps │
    └──────────────────┘        └──────────────────┘
```

#### Pub/Sub Task Delegation Pattern:
For long-running tasks, synchronous API waits lead to timeouts. Implement asynchronous task routing:
1.  The **Supervisor Agent** parses the user request.
2.  Instead of blocking, the Supervisor publishes a structured payload containing the subtask instruction to a **Cloud Pub/Sub** topic.
3.  **Worker Pods** subscribing to the topic pull the messages, instantiate a specialized worker agent via the ADK, execute the task, and publish results to a response topic.
4.  The Supervisor aggregates responses from the topic to formulate the final result.

#### Terraform Definition for A2A Pub/Sub Topics:
```hcl
resource "google_pubsub_topic" "subagent_tasks" {
  name    = "subagent-task-delegation"
  project = var.project_id
}

resource "google_pubsub_subscription" "worker_subscription" {
  name                 = "worker-agent-sub"
  topic                = google_pubsub_topic.subagent_tasks.name
  ack_deadline_seconds = 600 # Extended deadline for deep thinking tasks
}
```

---

### Phase 6: Enterprise Security
Security is critical when giving LLM agents tool execution capabilities.

#### Hardening Strategies:
*   **VPC Service Controls (VPC-SC)**: Place Vertex AI APIs, Cloud Run, GKE, and BigQuery inside a single VPC-SC Service Perimeter to prevent data exfiltration.
*   **Workload Identity Federation**: Map Kubernetes Service Accounts (KSA) in GKE directly to Google Service Accounts (GSA). Eliminate static service account JSON keys.
    ```bash
    # Bind KSA to GSA
    gcloud iam service-accounts add-iam-policy-binding KSA_NAME@your-project-id.iam.gserviceaccount.com \
        --role roles/iam.workloadIdentityUser \
        --member "serviceAccount:your-project-id.svc.id.goog[agent-namespace/ksa-agent-runner]"
    ```
*   **Tool Permission Boundaries**: Use Antigravity SDK safety policies to enforce human-in-the-loop approvals on destructive actions (e.g. running scripts or modifying database tables).
    ```python
    # Example safety policy restriction
    from google.antigravity import policy

    # Force confirmation prompt for run_command but allow mcp tool execution
    security_policies = [
        policy.confirm_run_command(),
    ]
    ```

---

### Phase 8 & 9: CI/CD and Production Deployment
Standardize agent and tool rollouts using GitOps:
*   **Infrastructure as Code (IaC)**: Deploy Cloud Run, GKE nodes, Pub/Sub, and IAM bindings via Terraform.
*   **Canary Deployments**: Configure Google Cloud Deploy to roll out new MCP servers or agent images using a progressive canary delivery strategy (10% -> 50% -> 100%) to mitigate regression risks.
*   **Dev/Stage/Prod Separation**: Ensure staging configurations connect to mock MCP integrations, while prod endpoints require mutual TLS (mTLS) authentication.

---

### Phase 10: Observability and Optimization (Day 2+)
To run an agentic platform efficiently, implement metrics and logging:
*   **Token Consumption Tracking**: Extract token logs (specifically separating input tokens, output tokens, and **Gemini reasoning/thinking tokens**) from the Antigravity SDK response.
*   **Vertex AI Model Monitoring**: Monitor prompt/response drift, safety violations, and execution latencies.
*   **Log Audit in BigQuery**: Configure GKE and Cloud Run log sinks to write directly to BigQuery for cost analytics and threat hunting.

> [!TIP]
> Ensure all active agents capture token metrics at the end of each turn and write them to structural logs:
> ```python
> # Example observability dump
> usage = await response.usage_metadata()
> print(f"Tokens Used: Input={usage.input_token_count}, Output={usage.output_token_count}")
> ```

---

## 3. Deployment Walkthrough (Quickstart)

### Step 1: Deploy MCP server on GCP Cloud Run
Use the provided `Dockerfile` to build and deploy the custom resource-listing MCP server:
```bash
gcloud builds submit --config=cloudbuild.yaml .
# Or build locally and push:
docker build -t us-central1-docker.pkg.dev/your-project-id/mcp-servers/resource-lister:latest .
docker push us-central1-docker.pkg.dev/your-project-id/mcp-servers/resource-lister:latest

# Deploy to Cloud Run
gcloud run deploy mcp-resource-lister \
    --image us-central1-docker.pkg.dev/your-project-id/mcp-servers/resource-lister:latest \
    --region us-central1 \
    --no-allow-unauthenticated
```

### Step 2: Configure and Run the Supervisor Agent on GKE
Configure your GKE Deployment with the necessary environment variables and the mounted Workload Identity service account. The agent will read its configuration and connect to the Cloud Run MCP server over the Server-Sent Events (SSE) channel:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: supervisor-agent-deployment
  namespace: agent-namespace
spec:
  replicas: 2
  selector:
    matchLabels:
      app: supervisor-agent
  template:
    metadata:
      labels:
        app: supervisor-agent
    spec:
      serviceAccountName: ksa-agent-runner
      containers:
      - name: agent-core
        image: us-central1-docker.pkg.dev/your-project-id/agent-images/supervisor:latest
        env:
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: gemini-secrets
              key: api-key
        - name: MCP_SERVER_URL
          value: "https://mcp-resource-lister-x7uq.a.run.app/sse"
```
