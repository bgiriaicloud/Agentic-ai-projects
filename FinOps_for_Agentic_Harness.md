# FinOps for the Agentic Harness
## The Hidden Cost of Non-Functional LLM Calls: Memory, Evals & Guardrails

---

### Executive Summary

In enterprise Agentic AI engineering, organizations frequently experience severe **"Token Shock"** when transitioning autonomous agents from prototype to production. Prototyping cost models typically assume a simplistic linear equation:

$$\text{Estimated Cost} = \text{User Prompts} \times (\text{Input Tokens} \times P_{\text{in}} + \text{Output Tokens} \times P_{\text{out}})$$

In reality, production bills are routinely **5× to 15× higher** than these naive estimates. 

The cause is not runaway user adoption, but **Non-Functional LLM Calls** executed under the hood by the **Agentic Harness**. To make an agent safe, stateful, reliable, and compliant, the harness executes a dense web of auxiliary LLM calls for **Guardrails**, **Memory consolidation**, **Trajectory self-reflection**, and **Continuous automated evaluations (LLM-as-a-Judge)**.

This guide establishes the **FinOps Framework for Agentic AI**, deconstructs the mathematical anatomy of non-functional token consumption, and provides actionable architectural patterns to slash non-functional spend by **60% to 80%** without sacrificing safety or enterprise reliability.

---

### Architecture & Non-Functional Cost Dynamics

![FinOps for Agentic Harness Architecture Diagram](file:///Users/biswanathgiri/GenAI%26AgenticAI%20-Learing%20Roadmap/finops_agentic_harness_architecture_diagram.png)

---


```
                       THE TOKEN AMPLIFICATION FACTOR (TAF)
                       
     1 User Message ("Book the cheapest flight to Chicago")
                              │
                              ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │                        THE AGENTIC HARNESS                             │
  │                                                                        │
  │  [PRE-EXECUTION GUARDRAIL]                                             │
  │  ├── 1. Prompt Injection & Jailbreak Classifier       (450 tokens)     │
  │  ├── 2. PII Detection & De-identification Scan        (600 tokens)     │
  │  └── 3. Policy & Intent Whitelist Router              (350 tokens)     │
  │                                                                        │
  │  [STATE & CONTEXT ENGINEERING]                                         │
  │  ├── 4. Episodic Memory Fact Extraction               (1,200 tokens)   │
  │  ├── 5. Semantic Memory Reranker (Candidate Scoring)  (2,500 tokens)   │
  │  └── 6. Short-term Working Memory Rolling Summary     (1,800 tokens)   │
  │                                                                        │
  │  [CORE AGENT TRAJECTORY (FUNCTIONAL)]                                  │
  │  ├── 7. Planning & Reasoning Loop (Turn 1)           (3,200 tokens)    │
  │  ├── 8. Tool Output Synthesizer & Schema Repair       (1,500 tokens)   │
  │  └── 9. Final Answer Generation                       (1,200 tokens)   │
  │                                                                        │
  │  [POST-EXECUTION GUARDRAIL]                                            │
  │  ├── 10. Groundedness & Hallucination Auditor         (4,500 tokens)   │
  │  └── 11. PII Egress & Tone Consistency Verifier       (800 tokens)     │
  │                                                                        │
  │  [EVALUATION & OBSERVABILITY (OBSERVE)]                                │
  │  ├── 12. LLM-as-a-Judge: Context Relevance Score      (3,800 tokens)   │
  │  └── 13. LLM-as-a-Judge: Trajectory Fidelity Score    (5,200 tokens)   │
  └────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
  Total Billable Tokens: ~27,100 Tokens  (Functional: 5,900 | Non-Functional: 21,200)
  Non-Functional Token Ratio (NFTR): 78.2%
  Token Amplification Factor (TAF): 11.3x
```

---

## 1. Anatomy of Non-Functional LLM Calls

Non-functional calls are interactions with foundation models that **do not directly produce user-facing answers or execute domain business logic**, but are strictly required to ensure **system safety, memory continuity, auditability, and governance**.

### 1.1 Guardrails Pipeline (Pre & Post Execution)

Modern enterprise harnesses (such as NeMo Guardrails, Guardrails AI, Azure AI Content Safety, Bedrock Guardrails, or custom LLM judges) place guardrail inspections at both ingress and egress:

| Stage | Inspection Type | Typical Mechanism | Cost Impact |
| :--- | :--- | :--- | :--- |
| **Pre-Flight** | **Prompt Injection & Jailbreak** | LLM Classifier with security system prompt | High frequency (100% of turns), low-to-medium token count. |
| **Pre-Flight** | **PII & Sensitive Data Redaction** | LLM or SLM entity detector | Runs on every user input before reaching agent memory. |
| **Pre-Flight** | **Domain / Topic Restriction** | LLM classifier ("Is this query in-scope?") | Rejects off-topic queries, but burns tokens doing so. |
| **Post-Flight** | **Groundedness / Hallucination** | LLM-as-a-judge comparing Answer vs Retrieved Documents | **Massive Cost Driver**: Must pass the entire retrieved context (4k–32k tokens) to evaluate claims. |
| **Post-Flight** | **PII Leakage & Corporate Tone** | LLM scan on final output | Adds output token latency and costs. |

> **The Groundedness Trap:** If your RAG retrieval pulls 5 documents totaling 8,000 tokens, your core agent reads 8,000 tokens to draft an answer. Then, your post-execution guardrail re-submits those same 8,000 tokens along with the answer to a judge model to verify factual consistency. **Context input cost is immediately doubled.**

---

### 1.2 Memory & Context Management Overhead

Stateful multi-turn agents cannot simply append messages forever without exceeding context windows and increasing latency. The harness manages state dynamically using background LLM passes:

1. **Working Memory Summarization:**
   When the conversation exceeds a sliding token threshold (e.g., 4,000 tokens), the harness invokes an LLM to generate an updated concise summary of turns $1 \dots N-4$.
2. **Episodic Memory Extraction:**
   Every turn or task conclusion triggers an LLM extraction pass: *"Extract persistent user facts, preferences, and project entities from this exchange."*
3. **Context Reranking (LLM-as-a-Reranker):**
   When vector search returns 20 candidate chunks, high-precision harnesses run an LLM listwise or pairwise reranker pass across all 20 candidates before injecting them into the agent prompt.
4. **Metacognitive Reflection & Consolidation:**
   Autonomous agents (e.g., MemGPT, Letta, Reflexion) perform periodic background passes to organize long-term memories, update scratchpads, and discard obsolete facts.

---

### 1.3 Continuous Evals (LLM-as-a-Judge)

In regulated enterprise environments (Finance, Healthcare, Legal), product teams require automated regression monitoring. Rather than running evals offline in a staging pipeline, many architectures evaluate **100% of live production traffic inline**:

- **Context Relevance Judge:** Evaluates if retrieved chunks were relevant to user query.
- **Answer Groundedness Judge:** Evaluates if output is derived from context.
- **Answer Relevance Judge:** Evaluates if output answered the user's intent.
- **Trajectory Correctness Judge:** Evaluates if the agent's intermediate tool selection sequence was optimal.

If each judge prompt contains system instructions, rubrics, context, and the full transcript, **a single user query can trigger 10,000 to 20,000 evaluation tokens**.

---

### 1.4 Agent Trajectory Loops (Internal Overhead)

Autonomous agents operate via iterative reasoning loops (e.g., ReAct, Plan-and-Solve):

$$\text{Thought} \longrightarrow \text{Action} \longrightarrow \text{Observation} \longrightarrow \text{Thought}$$

- **Scratchpad Accumulation:** Each iteration re-submits the entire conversation history, tool definitions, plus all previous Thoughts and Observations. An agent taking 5 hops to solve a problem submits the initial context **5 separate times**.
- **JSON Repair & Validation:** When a tool call fails JSON parsing, the harness prompts the model to repair its formatting, adding unexpected roundtrips.
- **Multi-Agent Consensus:** Multi-agent architectures (e.g., Supervisor $\leftrightarrow$ Worker $\leftrightarrow$ Critic) multiply token volumes by the number of participating agents.

---

## 2. Mathematical Modeling & The Cost Equation

### 2.1 The Unit Economics Formulation

Let a single user conversation session consist of $T$ user turns. For each turn $t$, total cost $C(t)$ is modeled as:

$$C(t) = C_{\text{functional}}(t) + C_{\text{guardrails}}(t) + C_{\text{memory}}(t) + C_{\text{evals}}(t) + C_{\text{trajectory\_overhead}}(t)$$

Where for any LLM call $i$:

$$C_i = (\text{Tokens}_{\text{in}}^{(i)} \times P_{\text{in}}^{(m_i)}) + (\text{Tokens}_{\text{out}}^{(i)} \times P_{\text{out}}^{(m_i)})$$

- $P_{\text{in}}^{(m_i)}$: Price per input token for model $m_i$.
- $P_{\text{out}}^{(m_i)}$: Price per output token for model $m_i$.

### 2.2 Key FinOps AI Metrics

| Metric | Formula | Target Benchmark |
| :--- | :--- | :--- |
| **Token Amplification Factor (TAF)** | $\frac{\text{Total Tokens Billed}}{\text{Tokens in Functional Agent Prompt + Answer}}$ | $< 2.5\times$ (Optimized)<br>$> 8.0\times$ (Unoptimized) |
| **Non-Functional Token Ratio (NFTR)** | $\frac{\text{Tokens}_{\text{Non-Functional}}}{\text{Total Tokens Billed}} \times 100\%$ | $< 35\%$ (Optimized)<br>$> 75\%$ (Unoptimized) |
| **Cost Per Task Completion (CPTC)** | $\frac{\sum_{\text{session}} C_{\text{all\_calls}}}{\text{Successful Goal Status}}$ | Stable predictable unit cost |
| **Evaluation Tax Ratio (ETR)** | $\frac{C_{\text{evals}}}{C_{\text{functional}}}$ | $5\% - 10\%$ (Sampled)<br>$> 150\%$ (100% Inline) |

---

### 2.3 Concrete Financial Scenario: 1,000,000 Monthly Active Sessions

Consider an enterprise customer support agent processing **1,000,000 user sessions per month**, averaging 4 turns per session (4,000,000 turns total).

#### Scenario A: Un-optimized Naive Harness
- **Model:** Frontier Model (e.g., GPT-4o / Claude 3.5 Sonnet: \$2.50/M in, \$10.00/M out) used for **all** tasks (Functional, Guardrails, Memory, Evals).
- **Guardrails:** 100% inline LLM prompt injection + 100% post-generation groundedness check with full context.
- **Memory:** LLM summarization pass every 3 turns.
- **Evals:** 100% inline LLM-as-a-judge scoring.
- **Average Tokens per Turn:**
  - Functional Agent: 2,500 in, 300 out.
  - Non-Functional (Guardrails, Memory, Evals): 12,000 in, 800 out.
  - Total per turn: 14,500 in, 1,100 out.

$$\text{Monthly Input Cost} = 4\text{M turns} \times 14,500 \text{ tokens} \times \frac{\$2.50}{10^6} = \$145,000$$
$$\text{Monthly Output Cost} = 4\text{M turns} \times 1,100 \text{ tokens} \times \frac{\$10.00}{10^6} = \$44,000$$
$$\mathbf{\text{Total Un-optimized Monthly Spend}} = \mathbf{\$189,000/\text{month}}$$
*(Of which \$148,000 or 78.3% is non-functional overhead!)*

---

#### Scenario B: FinOps-Optimized Harness
- **Frontier Model:** Reserved exclusively for complex agent reasoning & final answer synthesis.
- **Tiered SLMs:** Guardrails offloaded to fine-tuned Small Language Models (e.g., Llama-Guard 3 8B or Gemini 1.5 Flash / Claude 3.5 Haiku: \$0.075/M in, \$0.30/M out).
- **Deterministic Heuristic Filters:** Regex + Aho-Corasick for fast PII detection; vector similarity distance thresholding before LLM safety calls.
- **Prompt Caching:** Harness system prompts and tool schemas cached at 50%–80% discount.
- **Stratified Eval Sampling:** LLM-as-a-judge executed on a 5% statistical sample of sessions asynchronously via batch APIs (50% batch discount).
- **Semantic Caching:** Vector cache absorbs 25% of repetitive safety and retrieval validations.

$$\mathbf{\text{Total Optimized Monthly Spend}} = \mathbf{\$38,400/\text{month}}$$
$$\mathbf{\text{Monthly Savings: }} \mathbf{\$150,600 \text{ (79.7\% Reduction)}}$$

---

## 3. The FinOps Framework for Agentic AI

FinOps Foundation defines three phases: **Inform**, **Optimize**, and **Operate**. Here is how they map directly to Agentic AI Harness engineering:

```
                      FINOPS FOR AGENTIC HARNESS CYCLE
                      
       ┌─────────────────────────────────────────────────────────┐
       │                         INFORM                          │
       │  • Tag every LLM call with CallType & TenantID          │
       │  • Compute Real-time Token Amplification Factor (TAF)   │
       │  • Telemetry: OpenInference / OpenTelemetry Spans       │
       │  • Unit Economics: Cost per Task Completion (CPTC)      │
       └────────────────────────────┬────────────────────────────┘
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │                        OPTIMIZE                         │
       │  • Model Cascading: SLMs for Guardrails & Summaries     │
       │  • Prompt Prefix Caching (Anthropic/OpenAI/Gemini)      │
       │  • Deterministic Pre-Filtering (Regex, Embeddings)      │
       │  • Sampled / Asynchronous Batch Evaluations             │
       │  • Semantic Caching on Intermediate State Nodes         │
       └────────────────────────────┬────────────────────────────┘
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │                         OPERATE                         │
       │  • Real-time Leaky Bucket Token Circuit Breakers        │
       │  • Hard Loop Cap & Recursion Depth Limiter              │
       │  • Anomaly Detection on Runaway Agent Trajectories      │
       │  • Departmental Chargeback / Showback Invoicing         │
       └─────────────────────────────────────────────────────────┘
```

---

### Phase 1: Inform (Attribution & Visibility)

You cannot optimize what you cannot measure. Every HTTP call to an LLM provider must carry structured metadata headers and distributed tracing spans:

#### Metadata Schema for Agent Spans
```json
{
  "trace_id": "tr-8942b-99f1",
  "span_id": "sp-guardrail-pre-01",
  "tenant_id": "dept-fin-wealth-management",
  "session_id": "sess-user-99120",
  "turn_index": 3,
  "harness_component": "GUARDRAIL_PRE_FLIGHT",
  "call_classification": "NON_FUNCTIONAL",
  "model_family": "meta-llama/Llama-Guard-3-8B",
  "tokens_prompt": 450,
  "tokens_completion": 12,
  "cached_prompt_tokens": 300,
  "cost_usd": 0.000042,
  "latency_ms": 110
}
```

#### The 5 Call Classifications:
1. `FUNCTIONAL_REASONING`: The primary agent planning and ReAct loop.
2. `FUNCTIONAL_SYNTHESIS`: The final user-facing response generator.
3. `GUARDRAIL_INSPECTION`: Safety, prompt injection, PII, hallucination checks.
4. `MEMORY_MANAGEMENT`: Working memory compaction, episodic extraction, reranking.
5. `QUALITY_EVALUATION`: LLM-as-a-judge scoring, benchmark metrics.

---

### Phase 2: Optimize (Architectural Patterns)

#### Strategy 1: The Model Tiering Cascade (SLM Offloading)
Never use a \$3.00/M token model for tasks that can be accomplished with a \$0.10/M token model or fine-tuned SLM:

```
  [Ingress User Query]
          │
          ├──> Regex / Pattern Check (Cost: $0.00) ──[Match: SQLi/Regex PII]──> Block/Redact
          │
          ├──> Small SLM / DeBERTa / Llama-Guard 8B (Cost: $0.05/M)
          │    └── Safety & Jailbreak Check Passed?
          │           │
          │           ▼
          └──> Frontier LLM (GPT-4o / Claude 3.5 / Gemini 1.5 Pro) (Cost: $2.50/M)
               └── High-Level Planning & Tool Trajectory
```

#### Strategy 2: Prompt Prefix Caching
Harnesses routinely send identical static prefixes:
- System Persona & Guardrail Rules (~1,500 tokens)
- OpenAPI Tool Specifications (~2,500 tokens)
- Enterprise Knowledge Base Schema (~1,000 tokens)

By structuring prompt templates so **static content remains at the exact beginning** of the prompt, modern providers (Anthropic, Gemini, OpenAI) offer automatic prompt caching discounts:
- **Anthropic Claude:** 90% discount on cached input tokens.
- **OpenAI:** 50% discount on cached input tokens.
- **Google Gemini:** Up to 75% discount on cached context.

#### Strategy 3: Sampled & Asynchronous Evaluations
Evaluating 100% of live turns with an inline frontier LLM judge is a major financial drain.
- **Production Sampling:** Run LLM-as-a-judge on a **5% or 10% stratified random sample** of production turns.
- **Batch Evaluation Offloading:** Rather than running judges synchronously during user wait time, write inputs and outputs to a queue (Kafka / Cloud PubSub) and process them in off-peak batch jobs via OpenAI/Anthropic **Batch APIs (50% price reduction)**.
- **Event-Driven Triggers:** Only invoke heavy hallucination judges when specific trigger conditions occur (e.g., user thumb-down, high perplexity, or tool execution errors).

#### Strategy 4: Semantic Caching
Use high-speed vector embeddings (e.g., Qdrant, Redis, Cloud Vector Search) to cache non-functional calls:
- Safety checks for identical or semantically identical queries hit cache (0 tokens consumed).
- Retrieval queries hit semantic cache before triggering new vector reranking LLM passes.

---

### Phase 3: Operate (Governance & Circuit Breakers)

#### 1. Real-Time Token Leaky Bucket Circuit Breakers
Agents can get stuck in infinite reasoning loops when a tool returns unexpected output. The harness must enforce hard, non-bypassable constraints:
- `max_trajectory_hops`: Hard limit (e.g., maximum 6 tool iterations per turn).
- `max_turn_budget_tokens`: Terminate trajectory if cumulative tokens exceed threshold (e.g., 20,000 tokens).
- `max_turn_cost_dollars`: Abort task if single turn spend exceeds cap (e.g., \$0.15).

```python
class TokenCircuitBreaker:
    def __init__(self, max_cost_usd: float = 0.20, max_hops: int = 6):
        self.max_cost_usd = max_cost_usd
        self.max_hops = max_hops
        self.current_cost = 0.0
        self.current_hops = 0

    def record_call(self, cost: float):
        self.current_cost += cost
        self.current_hops += 1
        if self.current_cost > self.max_cost_usd:
            raise BudgetExceededException(f"Turn budget exceeded: ${self.current_cost:.4f} > ${self.max_cost_usd:.4f}")
        if self.current_hops > self.max_hops:
            raise MaxHopsExceededException(f"Agent loop detected: {self.current_hops} hops")
```

#### 2. Cost Showback & Chargeback Invoicing
Generate monthly showback reports grouped by:
- Tenant / Business Unit (`department_id`)
- Use Case / Agent ID (`agent_id`)
- Component Type (`Functional` vs `Non-Functional`)

---

## 4. Architectural Comparison: Naive vs FinOps Harness

```
   NAIVE HARNESS ARCHITECTURE                    FINOPS-GOVERNED HARNESS ARCHITECTURE
   
   [User Request]                                [User Request]
         │                                             │
         ▼                                             ▼
   [Frontier LLM]                                [Fast Deterministic Filter]
   (Pre-Guardrail: $2.50/M)                      (Regex / Aho-Corasick: $0.00)
         │                                             │
         ▼                                             ▼
   [Frontier LLM]                                [SLM Guardrail / Llama-Guard]
   (Context Reranker: $2.50/M)                   (Small Model: $0.08/M)
         │                                             │
         ▼                                             ▼
   [Frontier LLM]                                [Frontier LLM + Prompt Caching]
   (Agent ReAct: 8 hops unconstrained)           (Max 5 Hops + Cached Tools Prefix -80%)
         │                                             │
         ▼                                             ▼
   [Frontier LLM]                                [Adaptive Post-Guardrail]
   (Post-Guardrail 100% full context: $2.50/M)   (Lightweight SLM / Skip if Conf > 0.95)
         │                                             │
         ▼                                             ▼
   [Frontier LLM]                                [Async Sampled Eval Queue]
   (100% Inline Evals: $2.50/M)                  (5% Sampled, Batch API -50% Off-Peak)
         │                                             │
         ▼                                             ▼
   [User Answer]                                 [User Answer]
   
   Cost per 1k turns: $47.25                     Cost per 1k turns: $9.60  (-79.7%)
   TAF: 11.3x                                    TAF: 2.1x
```

---

## 5. Summary Checklist for Harness Engineers

- [ ] **Instrument every call:** Tag every LLM invocation with `call_type` (Functional, Guardrail, Memory, Eval) and tenant ID.
- [ ] **Track your TAF:** Calculate your Token Amplification Factor weekly. If TAF > 3.0, conduct a non-functional audit.
- [ ] **Demote Guardrails to SLMs:** Migrate prompt injection, toxicity, and PII checks away from frontier models to specialized SLMs (Llama-Guard, Mistral NeMo, or fine-tuned BERT/DeBERTa).
- [ ] **Enable Prompt Caching:** Order system prompts and OpenAPI tool definitions to guarantee static prefix reuse across turns.
- [ ] **Decouple and Sample Evals:** Remove synchronous 100% inline LLM-as-a-judge calls from the user request path; sample at 5%–10% into an asynchronous batch queue.
- [ ] **Enforce Token Circuit Breakers:** Implement hard ceilings on max hops, tokens per turn, and dollar budget per session to eliminate runaway recursion bills.
