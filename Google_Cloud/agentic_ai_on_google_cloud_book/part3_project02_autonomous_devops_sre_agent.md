# Project 02: Autonomous Cloud DevOps & SRE Troubleshooting Agent

## 🎯 Executive Overview & Business Objective
An autonomous SRE AI Agent that monitors Cloud Logging error spikes, performs root-cause analysis (RCA), and automatically generates Terraform remediation pull requests with Human-in-the-Loop (HITL) approval.

---

## 🏗️ System Architecture

```
[Cloud Logging / Monitoring Alerts (HTTP 500 Spike)]
        │
        ▼ (Log Sink Trigger)
[Google Cloud Pub/Sub] ──> [Cloud Run SRE Agent Service]
                                  │
                                  ▼
             [Gemini 2.0 Pro: Stacktrace Analysis & RCA]
                                  │
                                  ▼
             [MCP Tool Server: GitHub PR & Terraform Fix]
                                  │
                                  ▼ (HITL Approval)
                     [Slack / Teams Approval Hook]
```

---

## 💻 Production Implementation Code (SRE Remediation Core)

```python
from vertexai.generative_models import GenerativeModel

sre_model = GenerativeModel("gemini-2.0-pro-exp")

def diagnose_cloud_run_crash(error_logs: str) -> dict:
    """Performs autonomous root-cause analysis on Cloud Run container crashes."""
    prompt = f"""
    You are a Principal SRE on Google Cloud. Analyze the following Cloud Logging stacktrace:
    {error_logs}
    
    1. Identify Root Cause.
    2. Propose Terraform memory/CPU fix or IAM adjustment.
    3. Generate GitHub PR commit message.
    """
    response = sre_model.generate_content(prompt)
    return {"analysis": response.text, "status": "REMEDIATION_PLAN_READY"}
```
