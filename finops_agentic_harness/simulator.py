"""
FinOps for Agentic Harness - Simulation Engine
Compares Naive / Unmanaged Harness vs. FinOps-Governed Harness architecture.
"""

from typing import List
from .config import PRICING_CATALOG, ModelPricing
from .models import CallClassification, LLMCallSpan, TurnSimulationResult

def calculate_span_cost(
    model_key: str,
    input_tokens: int,
    output_tokens: int,
    cached_input_tokens: int = 0,
    is_async_batch: bool = False
) -> float:
    """Computes exact USD cost for an LLM call factoring in caching and batch discounts."""
    pricing: ModelPricing = PRICING_CATALOG.get(model_key, PRICING_CATALOG["gpt-4o"])
    
    uncached_inputs = max(0, input_tokens - cached_input_tokens)
    
    # Base input cost
    input_cost = (uncached_inputs / 1_000_000.0) * pricing.input_cost_per_m
    # Cached input cost
    cached_cost = (cached_input_tokens / 1_000_000.0) * pricing.cached_input_cost_per_m
    # Output cost
    output_cost = (output_tokens / 1_000_000.0) * pricing.output_cost_per_m
    
    total_cost = input_cost + cached_cost + output_cost
    
    # Apply batch discount if executed via asynchronous batch queue
    if is_async_batch:
        total_cost *= pricing.batch_discount_ratio
        
    return total_cost

def simulate_naive_harness(frontier_model: str = "gpt-4o") -> TurnSimulationResult:
    """
    Simulates a standard unmanaged enterprise harness where:
    - 100% of auxiliary tasks use the expensive Frontier Model.
    - No prompt caching is applied.
    - 100% inline evaluations are executed synchronously on every user turn.
    - Post-guardrails re-verify entire context.
    """
    result = TurnSimulationResult(scenario_name="Unmanaged / Naive Harness")
    
    def add_span(name: str, cls: CallClassification, inp: int, out: int, lat: float):
        cost = calculate_span_cost(frontier_model, inp, out)
        result.spans.append(LLMCallSpan(
            name=name,
            classification=cls,
            model_key=frontier_model,
            input_tokens=inp,
            output_tokens=out,
            cached_input_tokens=0,
            is_async_batch=False,
            cost_usd=cost,
            latency_ms=lat
        ))

    # 1. Pre-Guardrails (Inline Frontier Model)
    add_span("Prompt Injection & Jailbreak Scanner", CallClassification.GUARDRAIL_PRE, 450, 15, 240.0)
    add_span("PII & Content Safety Classifier", CallClassification.GUARDRAIL_PRE, 600, 20, 260.0)
    
    # 2. State & Memory Management (Inline Frontier Model)
    add_span("Working Memory Rolling Summarizer", CallClassification.MEMORY_MANAGEMENT, 1800, 150, 480.0)
    add_span("Episodic Memory Fact Extractor", CallClassification.MEMORY_MANAGEMENT, 1200, 80, 390.0)
    add_span("Context Candidate Listwise Reranker", CallClassification.MEMORY_MANAGEMENT, 2500, 100, 620.0)

    # 3. Core Functional Agent (Business Logic)
    add_span("Agent Trajectory (3 Tool Hops + Reasoning)", CallClassification.FUNCTIONAL_CORE, 4700, 400, 1450.0)
    add_span("Final Answer Synthesis", CallClassification.FUNCTIONAL_SYNTHESIS, 1200, 350, 650.0)

    # 4. Post-Guardrails (Inline Frontier Model with Full Context Repass)
    add_span("Groundedness & Hallucination Auditor", CallClassification.GUARDRAIL_POST, 4500, 120, 950.0)
    add_span("PII Egress & Brand Tone Checker", CallClassification.GUARDRAIL_POST, 800, 30, 310.0)

    # 5. Evals (100% Inline LLM-as-a-Judge)
    add_span("LLM-as-a-Judge: Context Relevance", CallClassification.QUALITY_EVALUATION, 3800, 80, 820.0)
    add_span("LLM-as-a-Judge: Trajectory Fidelity", CallClassification.QUALITY_EVALUATION, 5200, 150, 1100.0)

    return result

def simulate_finops_harness(
    frontier_model: str = "gpt-4o",
    eval_sampling_rate: float = 0.05
) -> TurnSimulationResult:
    """
    Simulates a FinOps-Governed Harness where:
    - Pre-Guardrails use Deterministic Heuristic + Dedicated SLM (Llama-Guard 3 8B).
    - Memory uses lightweight models & deterministic bi-encoders; episodic extraction is deferred.
    - Prompt Caching is enabled on static tool schemas and system instructions (80% cached).
    - Post-Guardrails are confidence-gated (SLM fallback).
    - Evals are sampled at 5% and executed asynchronously via Batch API (50% discount).
    """
    result = TurnSimulationResult(scenario_name="FinOps-Governed Harness")
    
    # 1. Pre-Guardrails: Deterministic First + SLM Offloading
    # Regex & Aho-Corasick absorbs PII and simple attacks at 0 tokens
    result.spans.append(LLMCallSpan(
        name="Deterministic PII & Injection Filter",
        classification=CallClassification.GUARDRAIL_PRE,
        model_key="deterministic-filter",
        input_tokens=0,
        output_tokens=0,
        cost_usd=0.0,
        latency_ms=2.0
    ))
    # SLM Guardrail (Llama-Guard 3 8B)
    slm_cost = calculate_span_cost("llama-guard-3-8b", 450, 10)
    result.spans.append(LLMCallSpan(
        name="SLM Guardrail (Llama-Guard 3 8B)",
        classification=CallClassification.GUARDRAIL_PRE,
        model_key="llama-guard-3-8b",
        input_tokens=450,
        output_tokens=10,
        cost_usd=slm_cost,
        latency_ms=85.0
    ))

    # 2. State & Memory: Bi-Encoder Reranker (0 LLM Tokens) + Lightweight Summarizer (Gemini Flash / 4o-mini)
    summary_cost = calculate_span_cost("gpt-4o-mini", 1200, 80)
    result.spans.append(LLMCallSpan(
        name="SLM Rolling Summarizer (Tier-2)",
        classification=CallClassification.MEMORY_MANAGEMENT,
        model_key="gpt-4o-mini",
        input_tokens=1200,
        output_tokens=80,
        cost_usd=summary_cost,
        latency_ms=180.0
    ))
    # Candidate reranking performed locally via fast cross-encoder embedding (0 LLM tokens)
    result.spans.append(LLMCallSpan(
        name="Bi-Encoder Embedding Reranker",
        classification=CallClassification.MEMORY_MANAGEMENT,
        model_key="deterministic-filter",
        input_tokens=0,
        output_tokens=0,
        cost_usd=0.0,
        latency_ms=15.0
    ))

    # 3. Core Functional Agent (Frontier Model + Prompt Prefix Caching)
    # 3,500 of the 4,700 tokens are cached tool schemas and system instructions
    cached_in = 3500
    uncached_in = 1200
    reasoning_cost = calculate_span_cost(
        frontier_model,
        input_tokens=4700,
        output_tokens=400,
        cached_input_tokens=cached_in
    )
    result.spans.append(LLMCallSpan(
        name="Agent Trajectory (Cached Prefix + Circuit Breaker)",
        classification=CallClassification.FUNCTIONAL_CORE,
        model_key=frontier_model,
        input_tokens=4700,
        output_tokens=400,
        cached_input_tokens=cached_in,
        cost_usd=reasoning_cost,
        latency_ms=920.0
    ))

    synth_cost = calculate_span_cost(
        frontier_model,
        input_tokens=1200,
        output_tokens=350,
        cached_input_tokens=800
    )
    result.spans.append(LLMCallSpan(
        name="Final Answer Synthesis (Cached Prefix)",
        classification=CallClassification.FUNCTIONAL_SYNTHESIS,
        model_key=frontier_model,
        input_tokens=1200,
        output_tokens=350,
        cached_input_tokens=800,
        cost_usd=synth_cost,
        latency_ms=450.0
    ))

    # 4. Post-Guardrails: Confidence-Gated Adaptive Check via SLM
    # Structured outputs with deterministic tool proofs skip full hallucination check
    post_guard_cost = calculate_span_cost("llama-guard-3-8b", 800, 20)
    result.spans.append(LLMCallSpan(
        name="Adaptive Groundedness & Egress SLM",
        classification=CallClassification.GUARDRAIL_POST,
        model_key="llama-guard-3-8b",
        input_tokens=800,
        output_tokens=20,
        cost_usd=post_guard_cost,
        latency_ms=90.0
    ))

    # 5. Evals: 5% Stratified Random Sample via Asynchronous Batch API (50% discount)
    # Effective cost per turn = 5% * Batch-discounted Eval Cost
    batch_eval_tokens_in = int((3800 + 5200) * eval_sampling_rate) # 450 tokens avg
    batch_eval_tokens_out = int((80 + 150) * eval_sampling_rate)   # 11 tokens avg
    eval_cost = calculate_span_cost(
        "gpt-4o-mini", # Use cost-efficient evaluator model
        input_tokens=batch_eval_tokens_in,
        output_tokens=batch_eval_tokens_out,
        is_async_batch=True
    )
    result.spans.append(LLMCallSpan(
        name="Sampled Async Batch Evals (5% Sample)",
        classification=CallClassification.QUALITY_EVALUATION,
        model_key="gpt-4o-mini",
        input_tokens=batch_eval_tokens_in,
        output_tokens=batch_eval_tokens_out,
        is_async_batch=True,
        cost_usd=eval_cost,
        latency_ms=0.0 # Zero user-facing latency impact
    ))

    return result
