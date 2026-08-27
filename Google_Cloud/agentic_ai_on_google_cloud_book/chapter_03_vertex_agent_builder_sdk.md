# Chapter 3: Vertex AI Agent Builder & Google Antigravity (AGY) SDK

> *"Vertex AI Agent Builder transforms natural language into enterprise-grade orchestrations backed by Google Cloud's security, compliance, and search infrastructure."*

---

## 3.1 Vertex AI Agent Builder: Architecture & Core Components

**Vertex AI Agent Builder** provides a suite of managed services for building, orchestrating, and deploying enterprise generative and agentic AI systems:

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                VERTEX AI AGENT BUILDER PLATFORM                                   │
├───────────────────────────────────────────────────────────────────────────────────────────────────┤
│  1. Agent Designer & Flows  : Multi-turn dialog trees, intent routing, and fallback handlers.      │
│  2. Data Stores & Search    : Unstructured (PDF/HTML), Structured (BigQuery), & Website indices. │
│  3. Extensions & Tools      : OpenAPI tool integrations, Cloud Functions, & BigQuery connectors. │
│  4. Enterprise Grounding    : Grounding checks, factuality evaluation, & citation verification.  │
│  5. Antigravity (AGY) SDK   : Native Python SDK for autonomous multi-agent code orchestration.   │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3.2 Google Antigravity (AGY) SDK Core Concepts

The **Google Antigravity (AGY) SDK** introduces a modular paradigm for building production agents:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        GOOGLE ANTIGRAVITY (AGY) SDK                    │
├────────────────────────────────────────────────────────────────────────┤
│  • Agents    : Autonomous entities with instructions, tools, & models. │
│  • Skills    : On-demand capability folders with SKILL.md instructions.│
│  • Rules     : Markdown behavioral constraints and style guidelines.   │
│  • Plugins   : Bundles grouping skills, subagents, and MCP configs.    │
│  • Sidecars  : Auxiliary microservices providing telemetry and tools.  │
└────────────────────────────────────────────────────────────────────────┘
```

### 1. Agents
An **Agent** defines an autonomous persona with a system prompt, configured tool calling permissions, model parameters (temperature, top_p), and active memory connections.

### 2. Skills
**Skills** are specialized cheat sheets and capability modules loaded on-demand. When an agent detects a task matching a skill's description, it reads the skill's `SKILL.md` instructions before execution.

### 3. Rules
**Rules** enforce invariant behavioral boundaries (e.g., *"Never execute DROP TABLE without user confirmation"* or *"Always return source citations in GitHub markdown links"*).

---

## 3.3 Building a Vertex AI Tool Extension in Python

```python
from google.cloud import aiplatform
from vertexai.preview.extensions import Extension

def register_bigquery_mcp_extension(project_id: str, location: str):
    """Registers an enterprise BigQuery tool extension in Vertex AI Agent Builder."""
    aiplatform.init(project=project_id, location=location)
    
    extension_spec = {
        "name": "BigQuery_Analytics_Tool",
        "description": "Executes SQL analytical queries over enterprise BigQuery datasets.",
        "openapi_spec": {
            "openapi": "3.0.0",
            "info": {"title": "BigQuery Service", "version": "1.0.0"},
            "paths": {
                "/query": {
                    "post": {
                        "summary": "Run SQL Query",
                        "operationId": "run_sql",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {"sql": {"type": "string"}},
                                        "required": ["sql"]
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    print("✅ Tool Extension Registered in Vertex AI Agent Builder!")
```

---

## 3.4 Chapter Summary & Key Takeaways

* **Vertex AI Agent Builder** provides managed dialog flows, data store connections, and grounding evaluation.
* **Google Antigravity (AGY) SDK** standardizes autonomous agent code via Agents, Skills, Rules, and Sidecars.
* **Next Chapter**: In [Chapter 4](chapter_04_gemini_models_tool_calling.md), we explore **Gemini 2.0 Flash/Pro** and multimodal tool calling.
