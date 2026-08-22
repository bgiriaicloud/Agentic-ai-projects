# Chapter 4: Foundation Models: Gemini 2.0 Flash, Pro & Multimodal Tool Calling

> *"Gemini 2.0 is built from the ground up for agentic workflows, featuring native multimodal understanding, 2M+ token contexts, and lightning-fast structured function calling."*

---

## 4.1 Gemini Model Selection Matrix for Agentic Workflows

Choosing the right foundation model determines the latency, cost, and reasoning accuracy of your agent:

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                GEMINI MODEL SELECTION MATRIX                                      │
├───────────────────────────────────────────────────────────────────────────────────────────────────┤
│  Model Name        Context Window    Latency     Optimal Agentic Use Case                         │
│  ───────────────────────────────────────────────────────────────────────────────────────────────  │
│  Gemini 2.0 Flash  1,048,576 tokens  <100ms      High-throughput tool calling, real-time agents   │
│  Gemini 2.0 Pro    2,097,152 tokens  Moderate    Complex multi-step coding, architecture planning │
│  Gemini 1.5 Pro    2,097,152 tokens  Standard    Deep document synthesis, cross-source RAG        │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4.2 Native Multimodal Tool Calling

Unlike earlier models that required separate OCR microservices, **Gemini 2.0** processes text, images, video frames, and audio waveforms directly in the token space.

### Multimodal Vision Tool Calling Example:
When an agent is presented with an architecture diagram or PDF chart:
1. Gemini extracts text and visual relationships directly.
2. Identifies a missing index or broken cloud component in the image.
3. Automatically triggers an external tool call: `terraform_apply_fix(resource="google_sql_database_instance")`.

---

## 4.3 Production Function Calling Schema in Python

```python
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, FunctionDeclaration

# 1. Define Function Signature
sql_tool_func = FunctionDeclaration(
    name="execute_bigquery_sql",
    description="Runs a SQL query against BigQuery datasets and returns tabular results.",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The standard SQL query to execute."},
            "max_rows": {"type": "integer", "description": "Max rows to return (default 100)."}
        },
        "required": ["query"]
    }
)

# 2. Bind Function to Gemini Tool
sql_tool = Tool(function_declarations=[sql_tool_func])

# 3. Initialize Gemini Model with Tool
model = GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    tools=[sql_tool],
    system_instruction="You are an autonomous Cloud Data Architect. Execute SQL queries to analyze data before answering."
)

print("✅ Gemini Model Configured for Native Function Calling!")
```

---

## 4.4 Chapter Summary & Key Takeaways

* **Gemini 2.0 Flash** is optimal for high-speed agent loops; **Gemini 2.0 Pro** is optimal for deep multi-step planning.
* **Function Calling** converts LLM reasoning into validated JSON parameters matching your API tools.
* **Next Chapter**: In [Chapter 5](chapter_05_event_driven_agentic_rag.md), we build the **Event-Driven Agentic RAG Pipeline** on Google Cloud.
