# Module 05: Vertex AI Agent Builder & Google Antigravity (AGY) Agent Platform

> *"Vertex AI Agent Builder combined with the Google Antigravity (AGY) SDK provides the complete development and runtime lifecycle for autonomous AI agents."*

---

## 5.1 Vertex AI Agent Builder Architecture

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                VERTEX AI AGENT BUILDER PLATFORM                                   │
├───────────────────────────────────────────────────────────────────────────────────────────────────┤
│  1. Agent Studio & Designer : Visual & code-based multi-turn dialog tree orchestration.           │
│  2. Grounded Data Stores    : Direct connectors to GCS, BigQuery, SharePoint, Jira, Confluence.   │
│  3. Extensions & Tools      : OpenAPI integrations, Cloud Functions, and external REST APIs.     │
│  4. Grounding with Search   : Turn-key grounding against Google Search for real-time web facts.   │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5.2 Google Antigravity (AGY) SDK Architecture

The **Google Antigravity (AGY) SDK** introduces standardized abstractions for engineering autonomous multi-agent software:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        GOOGLE ANTIGRAVITY (AGY) SDK                    │
├────────────────────────────────────────────────────────────────────────┤
│  • Agents     : Autonomous LLM entities with personas & tool access.   │
│  • Skills     : On-demand capability folders with SKILL.md rules.      │
│  • Rules      : Behavioral constraints and safety invariants.          │
│  • Plugins    : Namespaced bundles of skills, subagents, and tools.    │
│  • Sidecars   : Observability, telemetry, and background services.     │
└────────────────────────────────────────────────────────────────────────┘
```
