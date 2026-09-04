"""
FinOps Data Models for Agentic Harness Telemetry & Analytics
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict

class CallClassification(str, Enum):
    FUNCTIONAL_CORE = "FUNCTIONAL_CORE"          # Core agent reasoning, ReAct loop, tool orchestration
    FUNCTIONAL_SYNTHESIS = "FUNCTIONAL_SYNTHESIS" # Final user-facing answer generation
    GUARDRAIL_PRE = "GUARDRAIL_PRE"              # Prompt injection, jailbreak, PII ingress scanner
    GUARDRAIL_POST = "GUARDRAIL_POST"            # Groundedness/hallucination, PII egress audit
    MEMORY_MANAGEMENT = "MEMORY_MANAGEMENT"      # Rolling summary, episodic extraction, candidate reranking
    QUALITY_EVALUATION = "QUALITY_EVALUATION"    # LLM-as-a-judge (relevance, fidelity, safety scoring)

@dataclass
class LLMCallSpan:
    name: str
    classification: CallClassification
    model_key: str
    input_tokens: int
    output_tokens: int
    cached_input_tokens: int = 0
    is_async_batch: bool = False
    cost_usd: float = 0.0
    latency_ms: float = 0.0

@dataclass
class TurnSimulationResult:
    scenario_name: str
    spans: List[LLMCallSpan] = field(default_factory=list)
    
    @property
    def total_tokens(self) -> int:
        return sum(s.input_tokens + s.output_tokens for s in self.spans)
        
    @property
    def functional_tokens(self) -> int:
        return sum(s.input_tokens + s.output_tokens for s in self.spans 
                   if s.classification in (CallClassification.FUNCTIONAL_CORE, CallClassification.FUNCTIONAL_SYNTHESIS))
                   
    @property
    def non_functional_tokens(self) -> int:
        return self.total_tokens - self.functional_tokens

    @property
    def total_cost_usd(self) -> float:
        return sum(s.cost_usd for s in self.spans)

    @property
    def functional_cost_usd(self) -> float:
        return sum(s.cost_usd for s in self.spans 
                   if s.classification in (CallClassification.FUNCTIONAL_CORE, CallClassification.FUNCTIONAL_SYNTHESIS))

    @property
    def non_functional_cost_usd(self) -> float:
        return self.total_cost_usd - self.functional_cost_usd

    @property
    def token_amplification_factor(self) -> float:
        """TAF: Total Tokens / Functional Tokens"""
        return (self.total_tokens / self.functional_tokens) if self.functional_tokens > 0 else 1.0

    @property
    def non_functional_token_ratio(self) -> float:
        """NFTR: Non-Functional Tokens / Total Tokens (%)"""
        return (self.non_functional_tokens / self.total_tokens * 100.0) if self.total_tokens > 0 else 0.0

    @property
    def non_functional_cost_ratio(self) -> float:
        """NFCR: Non-Functional Spend / Total Spend (%)"""
        return (self.non_functional_cost_usd / self.total_cost_usd * 100.0) if self.total_cost_usd > 0 else 0.0

    def get_category_breakdown(self) -> Dict[str, Dict[str, float]]:
        """Returns tokens and cost aggregated by category."""
        breakdown = {}
        for c in CallClassification:
            cat_spans = [s for s in self.spans if s.classification == c]
            tokens = sum(s.input_tokens + s.output_tokens for s in cat_spans)
            cost = sum(s.cost_usd for s in cat_spans)
            breakdown[c.value] = {
                "tokens": tokens,
                "cost_usd": cost,
                "token_share_pct": (tokens / self.total_tokens * 100.0) if self.total_tokens > 0 else 0.0,
                "cost_share_pct": (cost / self.total_cost_usd * 100.0) if self.total_cost_usd > 0 else 0.0
            }
        return breakdown
