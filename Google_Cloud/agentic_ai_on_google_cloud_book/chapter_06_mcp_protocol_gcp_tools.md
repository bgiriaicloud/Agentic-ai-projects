# Chapter 6: Model Context Protocol (MCP) & Custom GCP Tool Servers

> *"Model Context Protocol (MCP) is the universal USB-C standard for LLMs—enabling agents to connect to any database, cloud service, or API with a single, uniform protocol."*

---

## 6.1 Understanding Model Context Protocol (MCP)

Before MCP, every AI agent framework (LangChain, LlamaIndex, AutoGen) required custom, fragmented tool wrappers. **MCP** standardizes tool calling and resource retrieval using **JSON-RPC 2.0**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        MODEL CONTEXT PROTOCOL (MCP)                    │
├────────────────────────────────────────────────────────────────────────┤
│  MCP Client (Host Agent) ──[JSON-RPC 2.0 over stdio/SSE]──> MCP Server │
│                                                                        │
│  • Resources : Read-only data files, schemas, and logs.                │
│  • Tools     : Executable actions (SQL query, Cloud Run deploy).       │
│  • Prompts   : Reusable prompt templates and workflows.                │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 6.2 Building a Google Cloud BigQuery MCP Server in Python

```python
import asyncio
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.types as types
from google.cloud import bigquery

app = Server("gcp-bigquery-mcp-server")
bq_client = bigquery.Client()

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """Exposes available BigQuery tools to any connected MCP Agent Client."""
    return [
        types.Tool(
            name="run_bigquery_query",
            description="Executes a standard SQL query against Google Cloud BigQuery.",
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {"type": "string", "description": "Standard SQL query string."}
                },
                "required": ["sql"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handles incoming tool execution requests from the Agent."""
    if name == "run_bigquery_query":
        sql = arguments["sql"]
        query_job = bq_client.query(sql)
        results = [dict(row) for row in query_job.result(max_results=20)]
        return [types.TextContent(type="text", text=str(results))]
    raise ValueError(f"Unknown tool: {name}")

if __name__ == "__main__":
    import mcp.server.stdio
    asyncio.run(mcp.server.stdio.stdio_server(app))
```

---

## 6.3 Chapter Summary & Key Takeaways

* **MCP** replaces ad-hoc tool integrations with a standard JSON-RPC 2.0 protocol over `stdio` or `SSE`.
* **GCP MCP Servers** can expose BigQuery, Cloud Storage, Cloud Logging, and Cloud SQL to any agent.
* **Next Chapter**: In [Chapter 7](chapter_07_multi_agent_a2a_swarms.md), we explore **Multi-Agent Systems & A2A Collaboration**.
