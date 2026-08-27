# Agentic AI Architect & Engineer 100 Interview Questions and Answers

This comprehensive reference contains 100 essential interview questions and answers for **Agentic AI Architects** and **AI Engineers**. It covers conceptual foundations, multi-agent orchestrations, Model Context Protocol (MCP), production scaling on GCP, observability, and safety.

---

## 📋 Table of Contents
1.  [Foundations of Agentic AI (Q1 - Q15)](#1-foundations-of-agentic-ai-q1---q15)
2.  [Agent Architectures & Reasoning Patterns (Q16 - Q30)](#2-agent-architectures--reasoning-patterns-q16---q30)
3.  [Multi-Agent Systems & A2A Orchestration (Q31 - Q50)](#3-multi-agent-systems--a2a-orchestration-q31---q50)
4.  [Tooling & Model Context Protocol (MCP) (Q51 - Q65)](#4-tooling--model-context-protocol-mcp-q51---q65)
5.  [Production Scaling & GCP Infrastructure (Q66 - Q80)](#5-production-scaling--gcp-infrastructure-q66---q80)
6.  [Observability, Cost, & FinOps (Q81 - Q90)](#6-observability-cost--finops-q81---q90)
7.  [Safety, Security, & Guardrails (Q91 - Q100)](#7-safety-security--guardrails-q91---q100)

---

## 1. Foundations of Agentic AI (Q1 - Q15)

#### Q1: What is Agentic AI, and how does it differ from generative AI?
**Answer:** Generative AI is passive; it takes a prompt and generates a static output in a single "zero-shot" transaction. Agentic AI is active and goal-driven. It operates in an autonomous loop—analyzing a goal, planning subtasks, executing tools to query databases or invoke APIs, observing outcomes, and self-correcting until the objective is reached.

#### Q2: What is the core execution loop of an AI Agent?
**Answer:** The core loop is generally referred to as the **Perceive-Plan-Act-Learn** loop. The agent perceives its environment (receives inputs/logs), plans its reasoning steps, acts by calling external tools or querying APIs, and learns or updates its state based on the feedback/observation before proceeding to the next turn.

#### Q3: What is the role of the Large Language Model (LLM) inside an Agent?
**Answer:** The LLM acts as the **central cognitive brain**. It is responsible for parsing unstructured prompts, selecting the next best action, synthesizing inputs, formatting tool arguments, and deciding when the goal has been achieved.

#### Q4: Explain the difference between Short-Term and Long-Term Agent Memory.
**Answer:** 
*   **Short-Term**: The context window of the active LLM turn. It tracks the message history and tool outputs of the current chat session.
*   **Long-Term**: Persistent storage (e.g., Vector Databases, SQL stores) that allows the agent to recall facts, user preferences, and past execution logs across separate sessions.

#### Q5: What is "Autonomy" in the context of AI agents?
**Answer:** Autonomy is the degree to which an agent can make decisions, plan actions, and invoke tools to achieve a target goal without human intervention or step-by-step guidance.

#### Q6: Explain what "Tool Calling" is.
**Answer:** Tool calling is the process where an LLM determines that it cannot answer a question without external data, parses the schemas of available tools (provided as JSON schemas in the prompt), and outputs a structured request (usually JSON) containing the tool name and arguments to be executed by the client application.

#### Q7: What is the "Grounding" problem in AI agents?
**Answer:** Grounding is the practice of anchoring the agent's responses in verifiable, real-world data sources (like databases or documents) rather than relying on the LLM's internal pre-trained weights, reducing hallucinations.

#### Q8: What is a "System Instruction" or "System Prompt"?
**Answer:** A system instruction is a high-priority system directive that sets the boundary rules, persona, formatting guidelines, and safety constraints of the agent's behavior. It is processed before any user message.

#### Q9: What is the difference between an Agent and a Workflow?
**Answer:** 
*   **Workflow**: A deterministic, step-by-step programmatic chain (e.g., `If X, then call API Y, then write to database Z`).
*   **Agent**: A non-deterministic system where the LLM dynamically decides the execution order, tool choices, and loop counts based on runtime feedback.

#### Q10: What are "Thinking/Reasoning Tokens"?
**Answer:** Some advanced models (like reasoning-focused LLMs) generate internal thought chains before presenting the final answer. These thought processes consume "thinking tokens" which help the model solve complex logic, coding, and planning tasks.

#### Q11: Explain what a "Human-in-the-Loop" (HITL) pattern is.
**Answer:** HITL is a design pattern where the agent pauses execution and requests human authorization before performing high-risk actions (such as sending emails, executing shell commands, or writing to production databases).

#### Q12: What is the difference between stateless and stateful agent sessions?
**Answer:** 
*   **Stateless**: Every prompt transaction is independent. The agent has no memory of previous turns.
*   **Stateful**: The agent maintains conversation history and state variables across multiple turns, creating a continuous session.

#### Q13: What is "Context Decay"?
**Answer:** Context decay occurs in long-running agent chats when the size of the history approaches the LLM's context limit, causing the model to lose track of early instructions or execute incorrect tool calls.

#### Q14: Explain "Context Compaction."
**Answer:** A technique used to prevent context decay. The agent platform automatically prunes early chat messages, summarizes old turns, or extracts key facts to keep the active context window size small and relevant.

#### Q15: What is an "Agent Persona"?
**Answer:** The designated role configured for the agent (e.g., "GCP Database Auditor" or "Terraform Script Developer") that shapes the tone, vocabulary, tool utilization strategies, and formatting of its outputs.

---

## 2. Agent Architectures & Reasoning Patterns (Q16 - Q30)

#### Q16: What is the ReAct (Reasoning and Acting) prompting framework?
**Answer:** ReAct combines reasoning and acting in a loop:
`Thought -> Action -> Observation -> Thought -> Action...`
The agent thinks about the problem, decides to take an action (call a tool), receives the observation (tool output), and evaluates its progress before planning the next step.

#### Q17: What is the "Plan-and-Solve" prompting strategy?
**Answer:** A framework where the agent first generates an explicit step-by-step plan to solve the target user request, and then executes the sub-steps sequentially, updating the plan dynamically if a step fails.

#### Q18: Explain the "Self-Reflection" (or Self-Correction) loop.
**Answer:** A pattern where the agent generates an initial draft output, analyzes it against target rules or a separate evaluation prompt, identifies flaws or bugs, and refactors the output before returning it to the user.

#### Q19: What is "Chain of Thought" (CoT) prompting?
**Answer:** CoT prompts the model to write out its intermediate reasoning steps explicitly rather than just outputting the final answer, which significantly increases accuracy in logical and mathematical tasks.

#### Q20: What is "Tree of Thoughts" (ToT)?
**Answer:** ToT is an extension of Chain of Thought where the agent explores multiple reasoning paths simultaneously (as branches of a tree). It evaluates the progress of each branch and uses backtracking to find the optimal solution path.

#### Q21: How do you implement memory persistence in the Google Antigravity SDK?
**Answer:** You configure a `save_dir` and pass a unique `conversation_id` in the `LocalAgentConfig`. The SDK automatically saves and loads the conversation trajectory history from that directory:
```python
config = LocalAgentConfig(conversation_id="session-123", save_dir="/path/to/storage")
```

#### Q22: What is the purpose of `ToolContext` in custom tool definitions?
**Answer:** `ToolContext` is automatically injected into custom Python tool functions. It allows tools to read and write state variables (e.g. tracking counters, session keys) that persist across subsequent chat turns.

#### Q23: What is "State Machine Routing" in agent design?
**Answer:** An architecture where the agent transitions between predefined states (e.g., `DISCOVER -> PLAN -> CODE -> AUDIT`). The transition criteria are determined dynamically by LLM outputs or system checks.

#### Q24: What is the "Retrieval-Augmented Generation" (RAG) pattern?
**Answer:** A pattern where the agent queries a vector database using semantic search to retrieve relevant document chunks matching the user prompt, injecting these chunks into the LLM context to ground the response.

#### Q25: Explain "Re-ranking" in RAG pipelines.
**Answer:** Re-ranking is a secondary evaluation step. After a vector search retrieves top document chunks, a re-ranker model evaluates their relevance against the query, sorting and filtering the list to insert only the most accurate context.

#### Q26: What is a "Semantic Router"?
**Answer:** A lightweight classification layer that evaluates the user prompt's semantic meaning and immediately routes it to a specific agent, workflow, or database query without calling a heavy LLM.

#### Q27: How does "Function-Calling" latency impact agent design?
**Answer:** Each tool call require a round-trip to the model (User Prompt -> LLM tool call -> Client executes tool -> LLM analyzes tool output). Designing lightweight tools and batching parallel tool calls minimizes execution latency.

#### Q28: What is "Structured Parsing" of agent outputs?
**Answer:** Forcing the agent to output data strictly matching a schema (like JSON matching a Pydantic class), allowing backend microservices to parse and consume the agent's decisions reliably.

#### Q29: Explain the "Least-to-Most" prompting pattern.
**Answer:** A technique where the agent decomposes a complex problem into a sequence of simpler subproblems, solves them in order, and uses the solution of the previous subproblem to solve the next one.

#### Q30: What is the "Critic Agent" pattern?
**Answer:** An architecture where an output generated by a Creator Agent is passed to a Critic Agent. The Critic evaluates the work (e.g. checking for security vulnerabilities or formatting errors) and provides feedback for refinement.

---

## 3. Multi-Agent Systems & A2A Orchestration (Q31 - Q50)

#### Q31: What is Agent-to-Agent (A2A) orchestration?
**Answer:** A architecture where a main coordinator agent (Supervisor) delegates tasks to specialized subagents, facilitating communication, task routing, and data sharing between autonomous agents.

#### Q32: Explain the "Supervisor-Worker" multi-agent topology.
**Answer:** A hierarchical layout where a single **Supervisor Agent** receives user prompts, plans the required actions, spawns specialized **Worker Agents** (e.g., Code Developer, DB Optimizer) for subtasks, and consolidates their outputs.

#### Q33: How do you enable subagent spawning in the Google Antigravity SDK?
**Answer:** You configure the `CapabilitiesConfig` inside `LocalAgentConfig` with `enable_subagents=True`:
```python
config = LocalAgentConfig(
    capabilities=types.CapabilitiesConfig(enable_subagents=True)
)
```

#### Q34: What is the "Peer-to-Peer" (P2P) agent collaboration model?
**Answer:** A decentralized layout where agents communicate directly with one another in a shared chat channel, negotiating tasks and sharing resources without a central controller.

#### Q35: What is an "Agent Registry"?
**Answer:** A directory service where agents register their schemas, descriptions, endpoints, and credentials. Other agents query this registry to locate and call specialized subagents dynamically.

#### Q36: How do you prevent "Infinite Agent Loops" in multi-agent discussions?
**Answer:** Implement execution boundaries: cap the maximum number of A2A turns, define strict stop sequences, monitor token spends, and enforce human-in-the-loop approvals if a loop is detected.

#### Q37: What is "State Sharing" in A2A systems?
**Answer:** The mechanism by which subagents access a common state store or memory database, allowing a worker agent to read variables written by a previous agent in the workflow chain.

#### Q38: Explain the difference between synchronous and asynchronous A2A orchestration.
**Answer:** 
*   **Synchronous**: The supervisor agent blocks and waits for a subagent to complete its task before moving to the next step.
*   **Asynchronous**: The supervisor publishes tasks to a queue (e.g. Pub/Sub) and goes idle. Worker agents pick up tasks, execute them, and publish results back, allowing long-running tasks to execute in parallel.

#### Q39: What is "Agent Negotiation"?
**Answer:** A pattern where two agents with conflicting rules (e.g. a "Feature Developer" pushing fast code and a "Security Auditor" enforcing strict policies) chat iteratively until they find a solution that satisfies both rule sets.

#### Q40: What is the role of an "Orchestration Domain" in enterprise AI?
**Answer:** An architectural boundary that groups related agents (e.g. Financial Agents) together, ensuring they only share memory databases and tools within their designated security domain.

#### Q41: Explain the "Sequential Chain" multi-agent flow.
**Answer:** A linear pipeline where Agent A completes its task, and its output is forwarded as the input for Agent B, which passes its output to Agent C, acting like an assembly line.

#### Q42: What is the risk of "Instruction Collision" in multi-agent chats?
**Answer:** When agents share a single chat history, one agent's system instructions might contradict or overwrite another agent's directives, causing the model to get confused. Keeping separate history buffers for each agent prevents this.

#### Q43: How do you model a "Dynamic Subagent"?
**Answer:** An agent that is instantiated on the fly with customized system instructions generated dynamically by the supervisor based on the specific requirements of the user's prompt.

#### Q44: What is the "Router Agent" pattern?
**Answer:** A routing agent that acts as a traffic controller. It receives user prompts, selects the single most appropriate specialized agent from a pool, and hands off the session to that agent.

#### Q45: Explain what "Context Swapping" is in A2A.
**Answer:** The process of copying, formatting, and transferring relevant variables and memory blocks from one agent's context window to another when handing off tasks.

#### Q46: What is a "Debate Team" pattern?
**Answer:** Spawning multiple agents configured with opposing personas to analyze a problem from different perspectives, helping to identify biases and hidden edge cases.

#### Q47: How does the "Agent Engine" manage task lists?
**Answer:** The Agent Engine tracks active and completed tasks in a dynamic task sheet (e.g., `task.md`), updating the status (`[ ]`, `[/]`, `[x]`) as agents execute subtasks.

#### Q48: What is "Agent Hand-off"?
**Answer:** A design pattern where an active agent decides it cannot proceed further (e.g. a support agent needs to process a refund), terminates its session, and invokes a different agent, passing along the session state.

#### Q49: What is a "Synthesizer Agent"?
**Answer:** A specialized agent whose sole task is to receive raw, verbose output dumps from multiple worker agents, clean up redundancies, format tables, and compile a clear executive summary.

#### Q50: How do you handle file transfers between subagents?
**Answer:** Subagents write files to a shared scratch space (e.g., an absolute path in GCP Cloud Storage or a shared local `app_data_dir`) and pass the file URI or reference link to the next agent.

---

## 4. Tooling & Model Context Protocol (MCP) (Q51 - Q65)

#### Q51: What is the Model Context Protocol (MCP)?
**Answer:** An open standard protocol designed to standardize how client applications and AI agents connect to external data sources, prompts, and tools hosted on decoupled MCP servers.

#### Q52: What problem does MCP solve?
**Answer:** Previously, developers had to write custom tool integrations for every specific agent framework (LangChain, AutoGen, etc.). MCP provides a unified standard: you build one MCP server, and any compliant agent client can immediately query and consume its tools.

#### Q53: What are the two primary transport modes supported by MCP?
**Answer:** 
1.  **Stdio**: Communication happens over standard input/output streams of a local subprocess launched by the agent.
2.  **SSE (Server-Sent Events)**: Communication happens over HTTP web endpoints, where the client connects to a remote web service.

#### Q54: What is FastMCP?
**Answer:** A high-level Python framework built on top of the python-mcp library that simplifies creating MCP servers, allowing you to define tools using a simple `@mcp.tool()` decorator.

#### Q55: How do you configure an MCP server in the Google Antigravity SDK?
**Answer:** You register the server configuration in the `mcp_servers` list of `LocalAgentConfig`:
```python
from google.antigravity import LocalAgentConfig, types

config = LocalAgentConfig(
    mcp_servers=[
        types.McpStdioServer(command="python3", args=["mcp_server.py"])
    ]
)
```

#### Q56: Explain the difference between MCP Tools, Resources, and Prompts.
**Answer:** 
*   **Tools**: Executable functions that allow the agent to perform actions (e.g., writing a file, querying a database).
*   **Resources**: Read-only data sources (such as documentation files, database schemas) the agent can query.
*   **Prompts**: Standardized system prompt templates exposed by the server.

#### Q57: How do you secure tool permissions in an MCP integration?
**Answer:** By default, the SDK allows all tools exposed by the MCP server. If using a strict safety policy, you can use a deny-by-default setup and explicitly whitelist allowed tools by name:
```python
policies = [policy.deny_all(), policy.allow("list_gcp_resources")]
```

#### Q58: What is "Schema Extraction" in MCP?
**Answer:** The process where the MCP client queries the server endpoint (e.g. `/tools` or `/resources`) to retrieve the JSON schemas of all registered tools, translating them into formats the LLM can parse for tool-calling.

#### Q59: Why is the docstring critical in FastMCP tool definitions?
**Answer:** FastMCP parses the function's docstring and arguments to auto-generate the JSON tool description sent to the LLM. If the docstring is missing or unclear, the LLM will not understand when or how to use the tool.

#### Q60: How does the SSE transport handle state?
**Answer:** SSE transport uses HTTP endpoints. The client connects to an initial endpoint, receives an event stream, and is assigned a unique session ID to post tool execution requests.

#### Q61: What is a "Tool Permission Boundary"?
**Answer:** A security configuration that restricts an agent's tool execution scope (e.g., allowing read-only database queries but blocking insert/delete calls).

#### Q62: What is the risk of "Blocking Tools" in MCP servers?
**Answer:** If an MCP tool blocks or runs a long calculation synchronously, it can cause the customization server to time out, freezing the agent loop. Tools should run asynchronously or leverage timeout boundaries.

#### Q63: Can an MCP server run in a container?
**Answer:** Yes. A common production pattern is containerizing the MCP server (e.g. using a Dockerfile) and deploying it to Google Cloud Run as a serverless SSE endpoint.

#### Q64: What is "Tool Discovery"?
**Answer:** The handshake process when an agent session initializes. The client queries the connected MCP servers to dynamically discover, validate, and register all available tools, resources, and templates.

#### Q65: How do you handle network failure in remote SSE MCP connections?
**Answer:** Implement retry mechanisms, set connection timeouts, and configure fallback behaviors (e.g., alerting the user or reverting to alternative local tools if the remote server is unreachable).

---

## 5. Production Scaling & GCP Infrastructure (Q66 - Q80)

#### Q66: Where should you host containerized MCP servers on GCP?
**Answer:** **Google Cloud Run** is the recommended serverless target. It scales down to zero when not in use, handles SSL offloading, and exposes HTTPS endpoints suitable for SSE transport.

#### Q67: How do you configure GKE to run agent workloads securely without static keys?
**Answer:** Use **Workload Identity**. It maps Kubernetes Service Accounts (KSA) inside the GKE cluster directly to Google Cloud Service Accounts (GSA), allowing pods to dynamically request temporary OAuth tokens to access Google APIs (Vertex AI, BigQuery).

#### Q68: How do you implement asynchronous multi-agent task queues on GCP?
**Answer:** Use **Cloud Pub/Sub**. The Supervisor Agent publishes task payloads (in JSON) to a Pub/Sub topic. GKE worker pods subscribe to the topic, pull tasks, instantiate a worker agent, execute the work, and publish the result back to a response topic.

#### Q69: What is the benefit of using VPC Service Controls (VPC-SC) for AI agents?
**Answer:** VPC-SC creates a security perimeter around Google APIs (Vertex AI, Cloud SQL, BigQuery) to prevent data exfiltration. Even if an agent gets compromised or runs untrusted tool code, it cannot copy data to projects outside the perimeter.

#### Q70: How do you handle API key management for agents on GCP?
**Answer:** Store keys (like Gemini API keys or external SaaS keys) in **GCP Secret Manager**. Inject them into the agent container as environment variables or mount them as secure volumes at runtime.

#### Q71: Explain the purpose of a Serverless VPC Access Connector in agent deployments.
**Answer:** It enables serverless workloads (such as Cloud Run hosting MCP servers) to access resources inside a private VPC network (like Cloud SQL databases or private GKE clusters) over internal IPs.

#### Q72: How do you deploy an agentic platform with High Availability (HA) on GCP?
**Answer:** Deploy GKE worker nodes across multiple zones, run agent deployments with replica sets greater than 1, and configure an External Load Balancer with Cloud Armor to distribute inbound user requests.

#### Q73: What is "Canary Deployment" for agents, and how do you do it on GCP?
**Answer:** Canary deployment rolls out new agent versions or MCP servers to a small subset of traffic. On GCP, you configure **Google Cloud Deploy** or use **Cloud Run Traffic Tagging** to split traffic (e.g., 90% stable, 10% canary) and verify error rates.

#### Q74: Why is a Shared VPC recommended for enterprise agent platforms?
**Answer:** It allows a central network team to manage core infrastructure (subnets, VPNs, perimeters) in a Host Project, while development teams deploy GKE clusters and VMs in Service Projects, maintaining strict separation of concerns.

#### Q75: How do you connect an on-premises enterprise database to a GCP-hosted agent?
**Answer:** Deploy **HA VPN** or **Cloud Interconnect** (Dedicated or Partner) to establish a secure, low-latency private connection between the GCP Shared VPC and the on-premises data center.

#### Q76: What is a "Warm Start" configuration for serverless agents?
**Answer:** Configuring a minimum instance count on Cloud Run (e.g., `min-instances = 1`) to eliminate cold start latencies, ensuring the agent responds immediately to user prompts.

#### Q77: How does GKE Autopilot simplify agent deployment?
**Answer:** It manages cluster provisioning, node scaling, OS patching, and security hardening automatically, allowing engineers to focus solely on packaging their agent deployments in YAML manifests.

#### Q78: What is "Least Privilege" IAM configuration for agents?
**Answer:** Assign GSAs specific, granular roles (e.g. only `roles/aiplatform.user` and `roles/pubsub.publisher`) rather than broad admin roles, ensuring the agent can only access the resources it needs.

#### Q79: What is the role of Cloud Build in the agent CI/CD pipeline?
**Answer:** It automates building Docker images from Dockerfiles on commit, running unit tests, scanning for vulnerabilities, and pushing images to Google Artifact Registry.

#### Q80: How do you configure a GCS bucket as an agent's long-term scratchpad?
**Answer:** Bind a Google Service Account with `roles/storage.objectAdmin` permissions to the agent container, allowing the agent to read and write documents, logs, and metadata directly to the Cloud Storage bucket.

---

## 6. Observability, Cost, & FinOps (Q81 - Q90)

#### Q81: What metrics should be monitored in a production agentic system?
**Answer:** Latency per turn, total execution time per task, task success/failure rate, total token count (split by input, output, and thinking tokens), tool execution success rate, and total cost per session.

#### Q82: How do you track Gemini token usage in the Google Antigravity SDK?
**Answer:** You retrieve usage metrics from the response object after a chat turn:
```python
usage = await response.usage_metadata()
input_tokens = usage.input_token_count
output_tokens = usage.output_token_count
```

#### Q83: Why is tracking "Thinking Tokens" critical for FinOps?
**Answer:** Reasoning models (like Gemini 3.5 Pro) use internal thinking tokens to solve complex planning tasks. Since these tokens are billed as output tokens but are not returned in the final user text, tracking them is essential for accurate cost estimation and budgeting.

#### Q84: How do you configure centralized audit logging for agents on GCP?
**Answer:** Configure Log Sinks to route all stdout/stderr logs from GKE and Cloud Run directly to **BigQuery** or **Cloud Logging**. This enables structured dashboards to monitor agent trajectories and detect anomalies.

#### Q85: What is "Alert Fatigue" in SRE, and how do you prevent it in AI platforms?
**Answer:** Alert fatigue occurs when operators are flooded with low-priority or false-positive alarms. Prevent it by using dynamic threshold alerting (anomaly detection) and grouping related alerts (e.g., grouping GKE CPU spikes with high agent token loads) instead of alerting on individual metrics.

#### Q86: Explain what an "Execution Trajectory" log is.
**Answer:** A step-by-step log of the agent's reasoning steps, tool calls, and observations during a session, which is vital for debugging logical failures.

#### Q87: How do you monitor API rate limits (quota limits) on Vertex AI?
**Answer:** Monitor `quota/exceeded_requests` metrics in Google Cloud Monitoring. Set up alerts at 80% quota usage to trigger automated scaling or request quota increases before failures occur.

#### Q88: What is "Trace ID Propagation" in multi-agent systems?
**Answer:** Passing a unique trace identifier in metadata headers across all A2A transitions and tool calls, allowing tools like **Cloud Trace** to visualize the entire distributed workflow.

#### Q89: How do you calculate the ROI of an automated agent workflow?
**Answer:** Compare the total API token and hosting costs of running the agent against the human labor cost and time required to complete the same tasks manually.

#### Q90: What is "Cost Cap Enforcer" in agent design?
**Answer:** A guardrail logic inside the agent loop that monitors session token costs. If the cost exceeds a set limit (e.g., $2.00), the loop is terminated to prevent runaway queries.

---

## 7. Safety, Security, & Guardrails (Q91 - Q100)

#### Q91: What is a "Prompt Injection" attack?
**Answer:** An attack where a user inputs malicious text designed to hijack the LLM's control flow, causing it to ignore system instructions and perform unauthorized actions (e.g., deleting data or leaking system secrets).

#### Q92: How do you defend against prompt injection?
**Answer:** 
1.  Enforce strict output schemas (structured outputs).
2.  Use safety filters and guardrail layers (like Vertex AI Safety Settings).
3.  Implement Least Privilege IAM rules for tools.
4.  Sanitize user inputs before forwarding them to tools or shell environments.
5.  Enforce human-in-the-loop approvals for high-risk actions.

#### Q93: What is "Data Leakage" in GenAI, and how do you prevent it?
**Answer:** Data leakage occurs when sensitive user data (like PII or corporate secrets) is sent to external LLM APIs. Prevent it by using private enterprise perimeters (VPC-SC), sanitizing PII locally, and using models with zero data-retention policies.

#### Q94: Explain the difference between whitelist and blacklist safety policies in the ADK.
**Answer:** 
*   **Blacklist**: Allows all actions by default, blocking only specific forbidden commands (e.g., blocking `rm -rf`).
*   **Whitelist**: Denies all actions by default, allowing only explicitly permitted tools and commands. (Recommended for production).

#### Q95: What is "jailbreaking" an agent?
**Answer:** Tricking the agent's LLM into bypassing its system safety instructions by using creative scenarios (e.g., "Pretend you are a developer bypass engine...").

#### Q96: What are "Vertex AI Safety Settings"?
**Answer:** Configurable filters on GCP that block prompts or model outputs containing hate speech, harassment, sexually explicit content, or dangerous content based on probability thresholds.

#### Q97: What is the "Confidential Computing" feature on GCP, and when should you use it?
**Answer:** An option for GKE and GCE that encrypts data in memory while it is being processed by the CPU, which is crucial for handling highly confidential healthcare or financial data.

#### Q98: How do you validate that an agent's custom tool is secure?
**Answer:** Sanitize all parameters, enforce strict type checking (e.g., using Pydantic validation), prevent string interpolation in SQL or shell commands, and run static code analysis (SAST) on the tool code.

#### Q99: What is "Model Drift" in production systems?
**Answer:** When changes to the underlying LLM weights (e.g., an automatic model update by the provider) cause the model to interpret prompts differently, leading to broken tool calls or format mismatches.

#### Q100: How do you defend against "Hallucinated Tool Calls"?
**Answer:** Ensure your custom tool schemas are highly descriptive, run validation checks on tool arguments returned by the LLM, and configure the agent to handle tool errors gracefully, allowing it to retry or ask for clarification.
