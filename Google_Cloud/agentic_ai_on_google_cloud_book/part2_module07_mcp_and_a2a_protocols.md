# Module 07: Protocols: Model Context Protocol (MCP) on GCP & Agent-to-Agent (A2A)

> *"Model Context Protocol (MCP) and Agent-to-Agent (A2A) standards establish universal interoperability across distributed tools and multi-agent swarms."*

---

## 7.1 Model Context Protocol (MCP) on Google Cloud

MCP provides a standardized **JSON-RPC 2.0** protocol connecting agent host clients to Google Cloud backend tools and resources:

```
┌─────────────────┐       MCP Protocol        ┌─────────────────┐
│   MCP Client    │  ──────────────────────>  │   MCP Server    │
│ (Antigravity/   │    (JSON-RPC 2.0 over     │ (BigQuery, GCS, │
│  Vertex Agent)  │  <──────────────────────  │  Cloud Run API) │
└─────────────────┘      stdio / SSE)         └─────────────────┘
```

---

## 7.2 Agent-to-Agent (A2A) Swarm Coordination

In multi-agent systems, agents discover and negotiate task execution using typed protocol payloads and distributed state stored in **Cloud Firestore** or **Cloud Spanner**.
