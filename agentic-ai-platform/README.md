# Enterprise Agentic AI Platform (ADK, MCP, & A2A)

This repository provides a reference implementation of an **Enterprise Agentic AI Platform** built on the **Google Antigravity SDK (ADK)** architecture, utilizing the **Model Context Protocol (MCP)** for custom tools, and showcasing **Agent-to-Agent (A2A)** orchestration.

---

## 🏗 Architecture Overview

```
                               ┌────────────────────────────────────────────────────────┐
                               │           User / Web Client / CLI Entrypoint           │
                               └───────────────────────────┬────────────────────────────┘
                                                           │
                                                           ▼
                               ┌────────────────────────────────────────────────────────┐
                               │             Supervisor Master Architect Agent          │
                               │          (agents/supervisor_agent.py - ADK Engine)     │
                               └───────────────────────────┬────────────────────────────┘
                                                           │
                                   ┌───────────────────────┴───────────────────────┐
                                   │  Agent-to-Agent (A2A) Task Delegation Loop    │
                                   ▼                                               ▼
                       ┌───────────────────────┐                       ┌───────────────────────┐
                       │ CloudOps Worker Agent │                       │ FinOps Worker Agent   │
                       │ (Infrastructure/IAM)  │                       │ (Billing Analytics)   │
                       └───────────┬───────────┘                       └───────────┬───────────┘
                                   │                                               │
                                   ▼                                               ▼
                       ┌───────────────────────┐                       ┌───────────────────────┐
                       │  Custom Tools Module  │                       │ FastMCP Stdio Server  │
                       │ (tools/custom_tools)  │                       │(mcp_servers/mcp_gcp)  │
                       └───────────────────────┘                       └───────────────────────┘
```

---

## 📁 Directory Structure

```text
agentic-ai-platform/
├── agents/                  # Cognitive reasoning agent files
│   ├── supervisor_agent.py  # Coordinating Supervisor agent orchestrating turns (ADK Engine)
│   └── worker_agents.py     # Specialized execution child subagents (A2A)
├── mcp_servers/             # Model Context Protocol servers
│   └── mcp_gcp_server.py    # Exposes custom GCP tools via FastMCP Stdio/SSE
├── tools/                   # Custom tool function declarations
│   └── custom_tools.py      # Cloud cost calculators & code interpreter sandbox
├── evals/                   # Evaluation and test harnesses
│   └── test_harness.py      # Automation pipelines auditing accuracy/groundedness
├── config.yaml              # Global orchestration parameters
├── docker-compose.yml       # Docker compose config for local multi-container environments
├── Dockerfile               # Production containerization build
├── main.py                  # CLI application entry point
├── app.py                   # FastAPI Web Server & Web UI (Port 8003)
├── README.md                # Platform documentation and file index
└── requirements.txt         # Pinned python library dependencies
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd agentic-ai-platform
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Automated Evaluation Harness
```bash
python3 -m unittest evals/test_harness.py
```

### 3. Run CLI Application Entry Point
```bash
python3 main.py --query "Run full infrastructure audit and calculate BigQuery billing spend"
```

### 4. Launch Web Testing Dashboard
```bash
python3 app.py
```
Open **`http://localhost:8003`** in your web browser.
