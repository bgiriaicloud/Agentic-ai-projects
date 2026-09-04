"""
FinOps for Agentic Harness - Pricing Configuration Catalog
Defines standard pricing per 1,000,000 tokens for Frontier Models, Lightweight Models,
and self-hosted Small Language Models (SLMs), including prompt caching discounts.
"""

from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class ModelPricing:
    name: str
    input_cost_per_m: float       # Cost per 1M input tokens ($)
    output_cost_per_m: float      # Cost per 1M output tokens ($)
    cached_input_cost_per_m: float # Cost per 1M cached input tokens ($)
    batch_discount_ratio: float   # Cost multiplier for async batch API (e.g. 0.5 for 50% discount)

# Standard industry pricing models (as of 2024-2025 enterprise tiers)
PRICING_CATALOG: Dict[str, ModelPricing] = {
    # Frontier Models (Used for complex planning, reasoning, code synthesis)
    "gpt-4o": ModelPricing(
        name="GPT-4o (Frontier)",
        input_cost_per_m=2.50,
        output_cost_per_m=10.00,
        cached_input_cost_per_m=1.25,  # 50% prompt caching discount
        batch_discount_ratio=0.50
    ),
    "claude-3-5-sonnet": ModelPricing(
        name="Claude 3.5 Sonnet (Frontier)",
        input_cost_per_m=3.00,
        output_cost_per_m=15.00,
        cached_input_cost_per_m=0.30,  # 90% prompt caching discount
        batch_discount_ratio=0.50
    ),
    "gemini-1-5-pro": ModelPricing(
        name="Gemini 1.5 Pro (Frontier)",
        input_cost_per_m=1.25,
        output_cost_per_m=5.00,
        cached_input_cost_per_m=0.3125, # 75% prompt caching discount
        batch_discount_ratio=0.50
    ),

    # Lightweight / Tier-2 Models (Used for summaries, intent routing)
    "gpt-4o-mini": ModelPricing(
        name="GPT-4o-mini (Lightweight)",
        input_cost_per_m=0.15,
        output_cost_per_m=0.60,
        cached_input_cost_per_m=0.075,
        batch_discount_ratio=0.50
    ),
    "claude-3-5-haiku": ModelPricing(
        name="Claude 3.5 Haiku (Lightweight)",
        input_cost_per_m=0.80,
        output_cost_per_m=4.00,
        cached_input_cost_per_m=0.08,
        batch_discount_ratio=0.50
    ),
    "gemini-1-5-flash": ModelPricing(
        name="Gemini 1.5 Flash (Lightweight)",
        input_cost_per_m=0.075,
        output_cost_per_m=0.30,
        cached_input_cost_per_m=0.01875,
        batch_discount_ratio=0.50
    ),

    # Dedicated SLM / Edge Guardrails (e.g., Llama-Guard 3 8B, DeBERTa, or fine-tuned BERT)
    "llama-guard-3-8b": ModelPricing(
        name="Llama-Guard 3 8B (Dedicated SLM)",
        input_cost_per_m=0.05,
        output_cost_per_m=0.05,
        cached_input_cost_per_m=0.05,
        batch_discount_ratio=1.00
    ),
    "deterministic-filter": ModelPricing(
        name="Deterministic Regex / Heuristic (Local CPU)",
        input_cost_per_m=0.00,
        output_cost_per_m=0.00,
        cached_input_cost_per_m=0.00,
        batch_discount_ratio=1.00
    )
}
