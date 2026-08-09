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
