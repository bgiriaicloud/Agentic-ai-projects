# Google Cloud Enterprise Agent Platform - Build, Scale, Govern & Optimize

This repository provides a complete, production-grade demo project for the **Google Cloud Agent Platform** (Vertex AI Agent Builder / Enterprise Agent Engine), demonstrating how to **Build, Scale, Govern, and Optimize** enterprise-grade AI agents.

---

## 🌟 The 4 Core Pillars of Google Cloud Agent Platform

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                             Google Cloud Agent Platform                                                    │
│                                                                                                                            │
│    ┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐    │
│    │        1. BUILD         │  │        2. SCALE         │  │        3. GOVERN        │  │       4. OPTIMIZE       │    │
│    │ Reasoning Engine &      │  │ Serverless Runtime &    │  │ Grounding Verification  │  │ Chain-of-Thought Trace  │    │
│    │ Vertex AI Extensions    │  │ Isolated Session State  │  │ & Safety Guardrails     │  │ & Token Cost Calculator │    │
│    └─────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘    │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **BUILD (Agent & Extensions Engine)**:
   - Powered by Gemini 2.0 / 3.6 Flash & Pro reasoning models.
   - Integrates Vertex Extensions: `vertex_ai_search` (Datastore grounding), `bigquery_finops_tool` (SQL billing exports), and `vertex_code_interpreter` (Safe Python sandbox).
2. **SCALE (Runtime & Session Isolation)**:
   - Manages serverless session container execution (`session_id`) with persistent state isolation.
3. **GOVERN (Enterprise Governance & Responsible AI)**:
   - Grounding Confidence Evaluation (scores factual alignment against enterprise datastores).
   - Responsible AI Safety Filters (checks toxicity, PII redaction, and IAM policy compliance).
4. **OPTIMIZE (Observability & Cost Management)**:
   - Full telemetry trace logging per pillar step.
   - Real-time token counter and Gemini Flash cost optimizer.

---

## 📁 Project Structure

```
Agent-platform-gcp/
├── gcp_agent_platform_sdk.py   # GCP Agent Platform SDK primitives (Build, Scale, Govern, Optimize)
├── agent.py                    # GCP Cloud Ops & FinOps AI Agent
├── app.py                      # FastAPI Backend REST Server (Port 8002)
├── test_gcp_platform.py        # Unit Test Suite for 4 Pillars
├── requirements.txt            # Python Dependencies
├── .env.example                # Environment Template for GCP Project & Vertex AI
├── README.md                   # Technical Documentation
└── static/
    ├── index.html              # Glassmorphic GCP Dashboard UI
    ├── style.css               # Google Cloud Dark-Mode Styling
    └── app.js                  # Client Application Logic
```

---

## 🚀 Quick Start (Simulated / Mock Mode)

Run locally without requiring an active GCP billing project or API keys!

### 1. Install Dependencies
```bash
cd Agent-platform-gcp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Unit Tests
```bash
python3 test_gcp_platform.py
```

### 3. Launch Web Dashboard & REST Server
```bash
python3 app.py
```
Open **`http://localhost:8002`** in your browser.

---

## ⚡ Connecting to Live GCP Vertex AI

To connect to your live GCP project (`gcp-10-project`):

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Update `.env` with your GCP details:
   ```ini
   GCP_PROJECT_ID=gcp-10-project
   GCP_LOCATION=us-central1
   VERTEX_AI_MODEL=gemini-2.0-flash-001
   EXECUTION_MODE=gcp
   ```

---

## 📜 Official References & Links
- [Google Cloud Vertex AI Agent Builder Documentation](https://cloud.google.com/vertex-ai/docs/agent-builder)
- [Google Cloud Enterprise AI Agents Overview](https://cloud.google.com/use-cases/ai-agents)
