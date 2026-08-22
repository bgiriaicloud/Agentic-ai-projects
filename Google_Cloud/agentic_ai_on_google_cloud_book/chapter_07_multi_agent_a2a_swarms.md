# Chapter 7: Multi-Agent Systems & Agent-to-Agent (A2A) Protocols

> *"Complex enterprise workflows cannot be solved by a single monolithic agent; they require a swarm of specialized agents collaborating under strict governance."*

---

## 7.1 Multi-Agent Architecture Patterns

```
┌────────────────────────────────────────────────────────────────────────┐
│                        SUPERVISOR-WORKER PATTERN                       │
├────────────────────────────────────────────────────────────────────────┤
│                       ┌──────────────────────┐                         │
│                       │   SUPERVISOR AGENT   │                         │
│                       │ (Planning & Routing) │                         │
│                       └──────────┬───────────┘                         │
│             ┌────────────────────┼────────────────────┐                │
│             ▼                    ▼                    ▼                │
│   ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐       │
│   │   DEVOPS AGENT   │ │  SECURITY AGENT  │ │   FINOPS AGENT   │       │
│   │ (Terraform/CI/CD)│ │ (VPC & IAM Audit)│ │(BigQuery Billing)│       │
│   └──────────────────┘ └──────────────────┘ └──────────────────┘       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 7.2 Distributed State Management with Cloud Firestore

When multiple agents collaborate asynchronously, they share state through **Cloud Firestore** or **Cloud Spanner**:

```python
from google.cloud import firestore

db = firestore.Client()

def update_agent_workflow_state(workflow_id: str, step_name: str, status: str, payload: dict):
    """Updates shared workflow execution state across distributed agents."""
    doc_ref = db.collection("agent_workflows").document(workflow_id)
    doc_ref.set({
        "current_step": step_name,
        "status": status,
        "payload": payload,
        "updated_at": firestore.SERVER_TIMESTAMP
    }, merge=True)
    print(f"✅ Workflow State Updated: {workflow_id} -> {step_name} [{status}]")
```

---

## 7.3 Inter-Agent Communication via Cloud Pub/Sub

Agents trigger peer agents asynchronously by publishing typed JSON messages onto designated Pub/Sub topics (e.g., `projects/my-gcp/topics/security-audit-requests`), enabling event-driven agent swarms.

---

## 7.4 Chapter Summary & Key Takeaways

* **Supervisor-Worker Pattern** breaks complex cross-functional tasks into delegated sub-agent assignments.
* **Distributed State**: Centralized in Firestore/Spanner prevents race conditions and loss of state across restarts.
* **Next Chapter**: In [Chapter 8](chapter_08_loop_engineering_hitl.md), we master **Loop Engineering & Human-in-the-Loop (HITL)**.
