# Amazon AgentCore - Production AI Agent Platform & Implementation

This repository provides a complete, production-ready demo project for **Amazon AgentCore** (AWS Bedrock AgentCore), AWS's managed infrastructure platform designed to deploy, run, and observe AI agents at scale.

---

## 🌟 What is Amazon AgentCore?

**Amazon AgentCore** is an infrastructure platform that provides composable services to run AI agents built with any framework (LangChain, LangGraph, LlamaIndex, CrewAI, or custom SDKs) in a secure, scalable AWS environment.

### Key AgentCore Primitives Demonstrated

1. **AgentCore Runtime**: A serverless, session-isolated execution environment (`session_id`) that manages agent state transitions and auto-scaling.
2. **AgentCore Memory**: Handles both short-term conversation context across multi-turn interactions and long-term persistent fact storage.
3. **AgentCore Gateway**: Connects agents to external tools, databases, and APIs using the **Model Context Protocol (MCP)**.
4. **AgentCore Code Interpreter**: Provides a secure, containerized Python code execution sandbox for mathematical operations, data transformation, and financial calculations.
5. **AgentCore Observability**: Built-in monitoring and Chain-of-Thought telemetry tracing to inspect prompt planning, tool call inputs/outputs, and latency metrics.

---

## 🏗 Architecture Diagram

```
                               ┌────────────────────────────────────────────────────────┐
                               │             User / Client Application                  │
                               └───────────────────────────┬────────────────────────────┘
                                                           │
                                                           ▼
                               ┌────────────────────────────────────────────────────────┐
                               │           AgentCore Gateway (MCP Protocol)             │
                               └───────────────────────────┬────────────────────────────┘
                                                           │
                                                           ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                              Amazon AgentCore Platform                                               │
│                                                                                                                      │
│   ┌────────────────────────┐      ┌──────────────────────────────────┐      ┌────────────────────────────────────┐   │
│   │   AgentCore Runtime    │ <--> │         AgentCore Memory         │ <--> │       AgentCore Gateway Tools      │   │
│   │ (Session Container)    │      │ (Short & Long-Term Persistence)  │      │  - aws_cloud_cost_calculator       │   │
│   └───────────┬────────────┘      └──────────────────────────────────┘      │  - s3_log_analyzer                 │   │
│               │                                                             │  - code_interpreter_sandbox        │   │
│               │                                                             └────────────────────────────────────┘   │
│               ▼                                                                                                      │
│   ┌────────────────────────┐                                                                                         │
│   │ AgentCore Observability│                                                                                         │
│   │ (Telemetry & Traces)   │                                                                                         │
│   └────────────────────────┘                                                                                         │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Agentcore-aws/
├── agentcore_sdk.py       # Amazon AgentCore Platform Primitives (Runtime, Memory, Gateway, Sandbox, Tracing)
├── agent.py               # Cloud FinOps AI Agent using AgentCore primitives & MCP Tools
├── app.py                 # FastAPI Web Server & REST API Endpoints
├── test_agentcore.py      # Unit Test Suite
├── requirements.txt       # Dependencies
├── .env.example           # AWS Credentials & Bedrock Configuration Template
├── README.md              # Project Documentation
└── static/
    ├── index.html         # Interactive Web Dashboard
    ├── style.css          # Glassmorphic AWS-inspired CSS Styling
    └── app.js             # Client Application Logic
```

---

## 🚀 Quick Start (Simulated / Mock Mode)

Run the AgentCore platform locally without requiring an active AWS account!

### 1. Install Dependencies
```bash
cd Agentcore-aws
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Unit Tests
```bash
python3 test_agentcore.py
```

### 3. Launch Web Dashboard & REST Server
```bash
python3 app.py
```
Open **`http://localhost:8001`** in your browser.

---

## ⚡ Connecting to Live AWS Bedrock / AgentCore

To connect to live AWS Bedrock model deployments:

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Configure your AWS credentials:
   ```ini
   AWS_REGION=us-east-1
   AWS_ACCESS_KEY_ID=<your-aws-key-id>
   AWS_SECRET_ACCESS_KEY=<your-aws-secret-key>
   BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0
   EXECUTION_MODE=aws
   ```

---

## 📜 Official References & Links
- [AWS Amazon Bedrock AgentCore Official Overview](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Samples GitHub - Getting Started with AgentCore](https://github.com/aws-samples/sample-getting-started-with-amazon-agentcore)
