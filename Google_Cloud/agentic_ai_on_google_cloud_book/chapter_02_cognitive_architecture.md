# Chapter 2: The Agent Cognitive Architecture

> *"An agent without memory is amnesic; an agent without tools is paralyzed; an agent without planning is chaotic."*

---

## 2.1 The Four Pillars of Cognitive Agent Architecture

Every autonomous AI agent deployed in production is constructed upon **Four Core Pillars**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        COGNITIVE AGENT ARCHITECTURE                    │
├────────────────────────────────────────────────────────────────────────┤
│  1. BRAIN (LLM Reasoning Core)  : Parse, reason, plan, & synthesize.   │
│  2. MEMORY (State & Retrieval)  : Short-term (Context) & Long-term.    │
│  3. PLANNING (Decomposition)    : Sub-tasks, ReAct, Self-Reflection.   │
│  4. TOOLS (Action & Execution)  : APIs, SQL, Shell, Filesystem, Web.   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2.2 Deep Dive into the 4 Pillars

### 1. The Brain (Reasoning & Decision Engine)
* **Function**: Interprets incoming objectives, resolves ambiguities, generates structured function calling arguments, and validates output quality.
* **Google Cloud Implementation**: Powered by **Gemini 2.0 Pro** or **Gemini 2.0 Flash** hosted on Vertex AI.

### 2. Memory Systems (Short-Term vs. Long-Term)
* **Short-Term Memory (Working Context)**:
  * Lives in the active LLM context window.
  * Preserves immediate conversational turns, system instructions, and recent tool outputs.
* **Long-Term Memory (Episodic & Semantic Store)**:
  * Stored in **Vertex AI Vector Search** (semantic document vectors) and **Cloud Firestore / Spanner** (chat session history and state snapshots).
  * Enables agents to recall past interactions and domain knowledge across sessions.

### 3. Planning & Task Decomposition
* **ReAct Loop (Reasoning + Acting)**:
  ```
  User Goal ──> Thought ──> Action (Tool Call) ──> Observation ──> Reflection ──> Final Output
  ```
* **Plan-and-Solve**:
  * Agent first drafts an explicit multi-step execution plan before calling any tools.
  * Dynamically updates the remaining plan if an intermediate step fails.
* **Self-Consistency & Reflection**:
  * Agent reviews tool responses (e.g., a Python traceback or SQL syntax error) and generates a revised query without human intervention.

### 4. Tools & Environment Interaction
* **Standardized Interfaces**: Tools exposed via JSON Schema or **Model Context Protocol (MCP)**.
* **Examples**:
  * `query_bigquery_analytics(sql: str)`
  * `fetch_gcs_blob(bucket: str, path: str)`
  * `execute_cloud_function(payload: dict)`

---

## 2.3 Production Python Implementation of a ReAct Loop

```python
import json
from typing import Dict, Any, List

class AgentCognitiveCore:
    def __init__(self, llm_client, tools: Dict[str, Any]):
        self.llm = llm_client
        self.tools = tools
        self.memory: List[Dict[str, str]] = []

    def run_react_loop(self, user_goal: str, max_iterations: int = 5) -> str:
        self.memory.append({"role": "user", "content": user_goal})
        
        for iteration in range(1, max_iterations + 1):
            # 1. Thought & Decision
            decision = self.llm.generate_plan(self.memory)
            
            if decision.get("type") == "FINAL_ANSWER":
                return decision["answer"]
            
            # 2. Action (Tool Execution)
            tool_name = decision["tool_name"]
            tool_args = decision["tool_args"]
            
            print(f"[Iter {iteration}] Executing Tool: {tool_name} with args: {tool_args}")
            tool_fn = self.tools.get(tool_name)
            
            if not tool_fn:
                observation = f"Error: Tool '{tool_name}' not found."
            else:
                try:
                    observation = tool_fn(**tool_args)
                except Exception as e:
                    observation = f"Execution Error: {str(e)}"
            
            # 3. Observation & Reflection into Memory
            self.memory.append({
                "role": "tool",
                "tool_name": tool_name,
                "content": str(observation)
            })
            
        return "Failed to resolve goal within iteration limit."
```

---

## 2.4 Chapter Summary & Key Takeaways

* **The 4 Pillars**: Every agent requires Brain (Gemini), Memory (Context + Vector), Planning (ReAct), and Tools (APIs).
* **Next Chapter**: In [Chapter 3](chapter_03_vertex_agent_builder_sdk.md), we explore **Vertex AI Agent Builder** and the **Google Antigravity (AGY) SDK**.
