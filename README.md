# Enterprise Agentic AI Platform (ADK, MCP, & A2A) on Google Cloud

This repository contains a reference implementation for an Enterprise Agentic AI platform built on the **Google Antigravity SDK (ADK)**, utilizing the **Model Context Protocol (MCP)** for custom tools, and showcasing **Agent-to-Agent (A2A)** orchestration. It also includes a production-grade GCP planning and deployment guide.

![GCP Agentic AI Architecture Diagram](/Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/gcp_architecture_diagram.png)

## 🔄 AI Agentic User Workflow
![AI Agentic User Workflow](/Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/user_workflow_diagram.png)

---

## 📂 Repository Structure

| File | Type | Description |
| :--- | :--- | :--- |
| 📄 [agent_adk.py](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/agent_adk.py) | Python Script | Basic Antigravity agent setup demonstrating custom persona system instructions, a custom Python function tool, and streaming response and reasoning (thoughts). |
| 📄 [mcp_server.py](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/mcp_server.py) | Python Script | Custom MCP server built with `FastMCP` that exposes a tool for listing mock GCP resources. |
| 📄 [agent_mcp.py](file:///Users/biswanathgiri/GenAI%20Roadmap/agent_mcp.py) | Python Script | Agent that connects to the custom MCP server via Stdio transport to query and fetch resource listings. |
| 📄 [agent_a2a.py](file:///Users/biswanathgiri/GenAI%20Roadmap/agent_a2a.py) | Python Script | Multi-agent orchestration showcasing a Supervisor Agent that delegates subtasks to specialized subagents. |
| 🐳 [Dockerfile](file:///Users/biswanathgiri/GenAI%20Roadmap/Dockerfile) | Dockerfile | Hardened, non-root Docker build config optimized to deploy the MCP server via SSE transport on Google Cloud Run. |
| 📖 [gcp_deployment_guide.md](file:///Users/biswanathgiri/GenAI%20Roadmap/gcp_deployment_guide.md) | Markdown | Production-grade planning and deployment guide matching the phases of the GCP Agentic AI Platform Roadmap. |
| 📦 [requirements.txt](file:///Users/biswanathgiri/GenAI%20Roadmap/requirements.txt) | Requirements | List of Python dependencies required to run the scripts locally. |
| 📖 [agentic_notes.md](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/agentic_notes.md) | Markdown | Study & reference notes explaining core architectural and code concepts of ADK, MCP, and A2A. |
| 📖 [agentic_foundations_notes.md](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/agentic_foundations_notes.md) | Markdown | Study notes explaining foundations of AI Agents, Multi-Agent systems, MCP, and A2A. |
| 📖 [gcp_networking_exam_guide.md](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/gcp_networking_exam_guide.md) | Markdown | Comprehensive Google Cloud Networking Exam Preparation Guide (Chapters 1-8). |
| 📖 [forward_deployed_engineer_notes.md](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/forward_deployed_engineer_notes.md) | Markdown | Study notes outlining the Forward Deployed Engineer (FDE) role, responsibilities, and skillsets. |
| 📖 [harness_engineering_notes.md](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/harness_engineering_notes.md) | Markdown | Study notes defining Harness Engineering in 2026 across DevOps pipelines, AI evaluations, and wiring design. |
| 🖼️ [fde_path_to_impact.png](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/fde_path_to_impact.png) | Image | Infographic diagram outlining the FDE's journey from business problem discovery to delivering measurable impact. |
| 🖼️ [harness_agentic_system.png](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/harness_agentic_system.png) | Image | Infographic diagram outlining the key pillars of Harness Engineering in the context of an Agentic AI system. |
| 🖼️ [agentic_ai_project_structure.png](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/agentic_ai_project_structure.png) | Image | Infographic directory tree diagram illustrating the folder and file structure of an Enterprise Agentic AI project. |
| 🖼️ [data_ai_agent_architecture.png](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/data-ai-agent/data_ai_agent_architecture.png) | Image | Architecture diagram outlining the pipeline flow of the Conversational Analytics BigQuery Data Agent. |
| 🖼️ [enterprise_agentic_ai_architecture.png](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/Enterprise_agentic_ai_platform_project/enterprise_agentic_ai_architecture.png) | Image | Architecture diagram outlining the GCP Cloud Run container flow of the Enterprise Agentic AI Platform. |
| 🖼️ [multi_agent_architecture.png](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/ai-agent/multi_agent_architecture.png) | Image | Architecture diagram outlining the A2A Supervisor Agent delegation flow of the Multi-Agent Platform. |
| 🖼️ [gke_architecture.png](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/GKE/gke_architecture.png) | Image | Architecture diagram outlining a production GKE regional private cluster layout on Google Cloud Platform. |
| 🖼️ [docker_architecture.png](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/Docker/docker_architecture.png) | Image | Architecture diagram illustrating Docker Client, Daemon, Host resource spaces, and Registry links. |
| 🖼️ [linux_architecture.svg](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/Linux/linux_architecture.svg) | Image | High-fidelity vector architecture diagram outlining Linux OS execution rings, SCI, and hardware layers. |
| 📖 [devops_100_interview_questions.md](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/DevOps/devops_100_interview_questions.md) | Markdown | 100 essential DevOps interview questions and answers, covering culture, CI/CD, Docker, K8s, IaC, Cloud, and SRE. |
| 📖 [kubernetes_100_interview_questions.md](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/Kubernetes/kubernetes_100_interview_questions.md) | Markdown | 100 essential Kubernetes interview questions and answers, covering Control Plane, scheduling, networking, storage, configs, and RBAC security. |
| 📖 [linux_architecture.md](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/Linux/linux_architecture.md) | Markdown | Architectural diagram and description detailing Linux OS User Space, Kernel Space, and core subsystems. |
| 📖 [agentic_ai_100_interview_questions.md](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/AgenticAI/agentic_ai_100_interview_questions.md) | Markdown | 100 essential Agentic AI Architect and Engineer interview questions and answers, covering autonomy, reasoning, A2A, MCP, scaling, FinOps, and safety. |
| 📖 [gen_ai_100_interview_questions.md](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/GenAI/gen_ai_100_interview_questions.md) | Markdown | 100 essential Generative AI Engineer interview questions and answers, covering architectures, RAG, PEFT, evaluation, LLMOps, and security. |
| 📖 [fde_interview_questions_part1.md](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/FDE/fde_interview_questions_part1.md) | Markdown | Volume 1 of 200 Forward Deployed Engineer (FDE) interview questions and answers (Q1 - Q100). |
| 📖 [fde_interview_questions_part2.md](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/FDE/fde_interview_questions_part2.md) | Markdown | Volume 2 of 200 Forward Deployed Engineer (FDE) interview questions and answers (Q101 - Q200). |
| 📖 [cloud_architect_part1.md](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/Cloud_Architect/cloud_architect_part1.md) | Markdown | Volume 1 of 250 Cloud Architect interview questions and answers (Q1 - Q90). |
| 📖 [cloud_architect_part2.md](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/Cloud_Architect/cloud_architect_part2.md) | Markdown | Volume 2 of 250 Cloud Architect interview questions and answers (Q91 - Q170). |
| 📖 [cloud_architect_part3.md](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/Cloud_Architect/cloud_architect_part3.md) | Markdown | Volume 3 of 250 Cloud Architect interview questions and answers (Q171 - Q250). |
| 📖 [cloud_engineer_part1.md](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/Cloud_Engineer/cloud_engineer_part1.md) | Markdown | Volume 1 of 250 Cloud Engineer interview questions and answers (Q1 - Q90). |
| 📖 [cloud_engineer_part2.md](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/Cloud_Engineer/cloud_engineer_part2.md) | Markdown | Volume 2 of 250 Cloud Engineer interview questions and answers (Q91 - Q170). |
| 📖 [cloud_engineer_part3.md](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/Cloud_Engineer/cloud_engineer_part3.md) | Markdown | Volume 3 of 250 Cloud Engineer interview questions and answers (Q171 - Q250). |
| 📁 [Enterprise_agentic_ai_platform_project/](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/Enterprise_agentic_ai_platform_project) | Project Folder | Standalone containerized project showcasing ADK agent with Stdio FastMCP server deployed on Cloud Run using Gemini. |
| 📁 [data-ai-agent/](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/data-ai-agent) | Project Folder | Standalone containerized data agent querying BigQuery USA names public dataset using ADK and Streamlit visualization. |
| 📁 [ai-agent/](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/ai-agent) | Project Folder | Standalone containerized multi-agent project showcasing A2A supervisor delegation using ADK and Streamlit visualization. |
| 📁 [GKE/](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/GKE) | Project Folder | Standalone folder containing the production GKE regional private cluster architectural diagram. |
| 📁 [Kubernetes/](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/Kubernetes) | Project Folder | Standalone folder containing the 100 essential Kubernetes interview questions and answers guide. |
| 📁 [Docker/](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/Docker) | Project Folder | Standalone folder containing the Docker client-daemon architecture diagram. |
| 📁 [Linux/](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/Linux) | Project Folder | Standalone folder containing the Linux File System Hierarchy directory tree diagram. |

## 📂 Directory Structure

Below is the visual and text-based directory structure of a production-ready Enterprise Agentic AI project:

![Agentic AI Project Structure](/Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/agentic_ai_project_structure.png)

```text
agentic-ai-platform/
├── agents/                  # Cognitive reasoning agent files
│   ├── supervisor_agent.py  # Coordinating Supervisor agent orchestrating turns
│   └── worker_agents.py    # Specialized execution child subagents (A2A)
├── mcp_servers/             # Model Context Protocol servers
│   └── mcp_gcp_server.py    # Exposes custom tools and API connectors via stdio/SSE
├── tools/                   # Custom tool function declarations
│   └── custom_tools.py      # Core Python tool systems bound to agents
├── evals/                   # Evaluation and test harnesses
│   └── test_harness.py      # Automation pipelines auditing accuracy/groundedness
├── config.yaml              # Global orchestration parameters
├── docker-compose.yml       # Docker compose config for local multi-container environments
├── Dockerfile               # Production containerization build
├── main.py                  # CLI application entry point
├── README.md                # Platform documentation and file index
└── requirements.txt         # Pinned python library dependencies
```

---

## 🛠️ Software Installation Guide

To configure your local environment for executing and deploying this agentic platform, follow these steps:

### 1. Python Environment Setup
Ensure you have Python 3.10 or higher installed.
*   **macOS (using Homebrew)**:
    ```bash
    brew install python@3.11
    ```
*   **Debian/Ubuntu**:
    ```bash
    sudo apt update && sudo apt install python3.11 python3-pip python3.11-venv -y
    ```
*   **Virtual Environment Setup** (Recommended):
    Create and activate a virtual environment to prevent package dependency conflicts:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

### 2. Install Project Dependencies
Run pip to install the required agent libraries:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Google Cloud SDK (gcloud CLI) Setup
Since the deployment guide uses the Google Cloud CLI (`gcloud`) to manage resources, deploy to Cloud Run, and authenticate:
*   **macOS**:
    ```bash
    brew install --cask google-cloud-sdk
    ```
*   **Linux**:
    ```bash
    curl https://sdk.cloud.google.com | bash
    exec -l $SHELL
    ```
*   **Initialize and Authenticate CLI**:
    ```bash
    gcloud init
    gcloud auth application-default login
    ```
    *(Note: `application-default login` allows the `google-cloud-vertexai` library to leverage your user credentials for model access and resource querying).*

### 4. Docker Desktop Installation (Optional, for Containerization)
To build container images for the MCP server using the provided `Dockerfile`:
*   **macOS**: Install Docker Desktop via Homebrew or from the website:
    ```bash
    brew install --cask docker
    ```
*   **Verify Docker Daemon**: Ensure Docker is running by executing:
    ```bash
    docker --version
    ```

---

## ⚡ Quick Start: Running Locally

### 1. Prerequisites
Ensure you have completed the software installation steps above. Then, install the libraries in your virtual environment:
```bash
pip install -r requirements.txt
```

### 2. Set Up API Credentials
Obtain an API key from Google AI Studio: [Google AI Studio API Keys](https://aistudio.google.com/app/api-keys). Set it in your environment:
```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
```
*(Alternatively, create a `.env` file in the root of this folder containing `GEMINI_API_KEY="your-key"`).*

### 3. Run the Demos

#### 🖥️ Recommended: Interactive Web Testing Dashboard
Run our premium, Glassmorphism Web testing dashboard to run and test all three agent configurations (ADK, MCP, A2A) simultaneously in an elegant web chat interface showing agent thoughts/reasoning and final responses:
```bash
python3 app.py
```
Open your browser and navigate to `http://127.0.0.1:8000`.

#### Demo 1: Basic ADK Agent (Custom Persona + Python Function Tool)
This demo showcases a Cloud Solutions Architect persona utilizing a custom calculation tool and streaming its reasoning thoughts:
```bash
python3 agent_adk.py
```

#### Demo 2: Local MCP Integration (Stdio Connection)
This runs the agent alongside the custom local MCP server (`mcp_server.py`) using Stdio. The agent dynamically calls the MCP tool to query GCP resources:
```bash
python3 agent_mcp.py
```

#### Demo 3: Agent-to-Agent (A2A) Orchestration
This demonstrates a Supervisor Agent spawning and delegating tasks to child subagents (e.g., generating Terraform code, writing security configurations):
```bash
python3 agent_a2a.py
```

---

## ☁️ Google Cloud Platform Deployment

For scaling this layout to production on Google Cloud (Cloud Run, GKE, Pub/Sub, Workload Identity, and VPC-SC boundaries), please follow the structured, phase-by-phase roadmap in [gcp_deployment_guide.md](file:///Users/biswanathgiri/GenAI&AgenticAI%20-Learing%20Roadmap/gcp_deployment_guide.md).

### Containerizing the MCP Server
To build and publish the server image to Google Artifact Registry:
```bash
# Define your GCP Project ID
export PROJECT_ID="your-gcp-project-id"

# Submit build to Cloud Build
gcloud builds submit --tag us-central1-docker.pkg.dev/$PROJECT_ID/mcp-servers/resource-lister:latest .
```
See the deployment guide for Cloud Run commands to configure environment secrets and mount Serverless VPC networks.
