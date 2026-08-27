# ☁️ Azure Harness Engineering Demo Project

This project demonstrates **Harness Engineering** in a production-grade Azure AI ecosystem. It showcases how to wrap non-deterministic LLM agents with deterministic cloud guardrails, sandboxed runtimes, circuit breakers, trajectory telemetry, and automated evaluation suites.

---

## 🏗️ Architecture & Core Components

```
User Prompt / Goal
       │
       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       AZURE HARNESS LAYER                                   │
│                                                                             │
│  [1. Input Guardrail]                                                       │
│      ├── Azure AI Content Safety (Toxicity, Hate, Violence)                │
│      └── Azure Prompt Shield (Direct / Indirect Prompt Injection Filter)    │
│                                                                             │
│  [2. Control & Circuit Breaker]                                             │
│      ├── Max Step Limiter (Stops non-terminating loops)                     │
│      ├── Token Budget Ledger (Prevents budget runaways)                     │
│      └── Consecutive Failure Halting                                        │
│                                                                             │
│  [3. Sandboxed Execution]                                                   │
│      └── Azure Container Apps (ACA) Dynamic Sessions (Isolated MicroVM)     │
│                                                                             │
│  [4. Output Guardrail]                                                      │
│      ├── PII Redaction / Secret Detection                                   │
│      └── Groundedness & Hallucination Verifier                              │
│                                                                             │
│  [5. Observability & Continuous Evals]                                      │
│      ├── Azure Application Insights (OpenTelemetry Trajectory Spans)        │
│      └── Azure AI Studio Evaluation SDK (Relevance, Groundedness, Pass@k)   │
└─────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
Safe, Verified Output & Telemetry Report
```

---

## 📂 Project Structure

```
azure_harness_demo/
├── config.py                 # Azure endpoints, safety thresholds, and circuit breaker policies
├── agent.py                  # Agent planning and multi-step reasoning layer
├── demo.py                   # Runnable script showing 4 real-world test scenarios
├── requirements.txt          # Python dependencies
├── harness/
│   ├── __init__.py
│   ├── controller.py         # Master AzureAgentHarness execution wrapper
│   ├── guardrails.py         # Azure Content Safety, Prompt Shield & Groundedness checks
│   ├── sandbox.py            # Azure Container Apps (ACA) Dynamic Sessions runner
│   ├── telemetry.py          # Trajectory recording, App Insights OpenTelemetry & Circuit Breaker
│   └── evals.py              # Azure AI Studio automated evaluation harness
└── README.md                 # Documentation
```

---

## 🚦 4 Production Scenarios Demonstrated

1. **Happy Path Execution**: An agent analyzes revenue data, writes Python code, executes it inside the ACA Dynamic Session sandbox, logs trajectory spans, passes output guardrails, and receives a high score from Azure AI Studio Evaluator.
2. **Prompt Injection Defense**: A malicious prompt injection (`"Ignore previous instructions..."`) is intercepted by Azure Prompt Shield *before* any LLM tokens or agent cycles are consumed.
3. **Sandbox Isolation & Hypervisor Intercept**: An agent attempt to execute unauthorized system calls (`rm -rf /`) is blocked by the Sandbox hypervisor policy.
4. **Circuit Breaker Termination**: An agent caught in an infinite loop or exceeding token budgets is immediately halted by the Harness Circuit Breaker.

---

## 🚀 Quickstart & Execution

```bash
# 1. Navigate to repository root
cd "/Users/biswanathgiri/GenAI&AgenticAI -Learing Roadmap"

# 2. Run the demo runner
python3 -m azure_harness_demo.demo
```
