# ☁️ Google Cloud Platform (GCP) Harness Engineering Demo Project

This project demonstrates **Harness Engineering** in a production-grade Google Cloud Platform (GCP) ecosystem. It showcases how to wrap non-deterministic Vertex AI Gemini agents with deterministic Google Cloud guardrails, gVisor sandboxed runtimes, circuit breakers, Cloud Trace telemetry, and Vertex AI Gen AI Evaluation suites.

---

## 🏗️ GCP Harness Architecture & Core Components

```
User Prompt / Task
       │
       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GCP HARNESS LAYER                                   │
│                                                                             │
│  [1. Input Guardrail]                                                       │
│      ├── Google Cloud Model Armor (Prompt Injection & Jailbreak Shields)    │
│      └── Vertex AI Safety Settings (Harassment, Hate, Dangerous Content)    │
│                                                                             │
│  [2. Control & Circuit Breakers]                                            │
│      ├── Max Step Quota Limiter (Stops unbounded reasoning loops)           │
│      ├── Vertex AI Token Budget Ledger (Prevents budget runaways)           │
│      └── Consecutive Error Halting (Stops cascading tool failures)          │
│                                                                             │
│  [3. Sandboxed Execution]                                                   │
│      └── Cloud Run with gVisor Kernel Isolation (MicroVM Sandbox)           │
│                                                                             │
│  [4. Output Guardrail]                                                      │
│      ├── Cloud Sensitive Data Protection (DLP) (PII & Secret Redaction)     │
│      └── Vertex AI Groundedness Check (Search / Knowledge Base Grounding)   │
│                                                                             │
│  [5. Observability & Continuous Evals]                                      │
│      ├── Google Cloud Trace & Logging (OpenTelemetry Spans)                 │
│      └── Vertex AI Gen AI Evaluation Service (Groundedness, QA, Pass@k)     │
└─────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
Safe, Verified Output & Cloud Trace Report
```

---

## 📂 Project Structure

```
gcp_harness_demo/
├── README.md               # Architecture documentation & scenario guide
├── config.py               # Google Cloud project settings & circuit breaker policies
├── agent.py                # Vertex AI Gemini Agent with BigQuery/Python tool reasoning
├── demo.py                 # Runnable demo suite testing all 4 GCP production scenarios
├── requirements.txt        # Google Cloud SDK dependencies
└── harness/
    ├── __init__.py
    ├── controller.py       # Master GCPAgentHarness orchestrator
    ├── guardrails.py       # Model Armor, Vertex AI Safety & Cloud DLP guardrails
    ├── sandbox.py          # Google Cloud Run / gVisor sandboxed execution runner
    ├── telemetry.py        # Cloud Trace / Cloud Logging OpenTelemetry spans & circuit breakers
    └── evals.py            # Vertex AI GenAI Evaluation Service harness
```

---

## 🚦 4 Production Scenarios Demonstrated

1. **Happy Path Execution**: Gemini 1.5 Pro analyzes BigQuery data, executes Python in the gVisor sandbox, logs Cloud Trace spans, passes output guardrails, and receives high scores from Vertex AI Gen AI Evaluator.
2. **Prompt Injection Defense**: A malicious prompt injection (`"System prompt override..."`) is intercepted by **Google Cloud Model Armor** *before* reaching the Vertex AI reasoning engine.
3. **gVisor Syscall Intercept**: An agent attempt to execute unauthorized system operations (`subprocess.Popen`) is blocked at the gVisor application kernel boundary.
4. **GCP Circuit Breaker Termination**: An agent caught in an infinite retry loop or exceeding token budgets is immediately halted by the GCP Harness Circuit Breaker.

---

## 🚀 Quickstart & Execution

```bash
# 1. Navigate to repository root
cd "/Users/biswanathgiri/GenAI&AgenticAI -Learing Roadmap"

# 2. Run the demo runner
python3 -m gcp_harness_demo.demo
```
