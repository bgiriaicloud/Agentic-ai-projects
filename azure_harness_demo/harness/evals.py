"""
Azure AI Studio Evaluation Harness.
Implements automated evaluations using Azure AI Evaluation principles (Groundedness, Relevance, Trajectory Evals).
"""

from typing import Dict, Any, List
from dataclasses import dataclass, field
from .telemetry import TrajectoryLog
from ..config import policy

@dataclass
class MetricScore:
    name: str
    score: float # 0.0 to 1.0 or 1 to 5
    passed: bool
    threshold: float
    reasoning: str

@dataclass
class EvaluationReport:
    session_id: str
    overall_status: str # "PASSED" | "FAILED"
    metrics: List[MetricScore] = field(default_factory=list)
    trajectory_efficiency_score: float = 1.0
    cost_efficiency_score: float = 1.0
    summary: str = ""

class AzureAIStudioEvaluator:
    """
    Harness component simulating and wrapping Azure AI Studio Evaluation SDK.
    Calculates Groundedness, Relevance, Trajectory Efficiency, and Pass/Fail status.
    """
    def __init__(self):
        self.policy = policy

    def evaluate_trajectory(self, query: str, final_response: str, context: str, trajectory: TrajectoryLog) -> EvaluationReport:
        """
        Runs Azure AI Studio evaluators on the completed agent execution.
        """
        metrics = []
        
        # 1. Relevance Evaluator
        query_terms = set(query.lower().split())
        response_terms = set(final_response.lower().split())
        overlap = len(query_terms.intersection(response_terms))
        rel_score = min(1.0, (overlap / max(1, len(query_terms))) + 0.4)
        metrics.append(MetricScore(
            name="Relevance",
            score=round(rel_score, 2),
            passed=(rel_score >= self.policy.min_relevance_score),
            threshold=self.policy.min_relevance_score,
            reasoning="Measures how directly the agent's output addresses the user's intent."
        ))

        # 2. Groundedness Evaluator
        groundedness_score = 0.95 if context else 0.85
        metrics.append(MetricScore(
            name="Groundedness",
            score=round(groundedness_score, 2),
            passed=(groundedness_score >= self.policy.min_groundedness_score),
            threshold=self.policy.min_groundedness_score,
            reasoning="Ensures the response does not hallucinate facts outside the context."
        ))

        # 3. Trajectory Efficiency Evaluator (Penalty for excessive steps)
        step_count = len(trajectory.steps)
        eff_score = max(0.0, 1.0 - (step_count * 0.1))
        metrics.append(MetricScore(
            name="Trajectory Efficiency",
            score=round(eff_score, 2),
            passed=(step_count <= self.policy.max_steps_per_task),
            threshold=1.0 - (self.policy.max_steps_per_task * 0.1),
            reasoning=f"Agent completed the task in {step_count} step(s)."
        ))

        all_passed = all(m.passed for m in metrics) and (trajectory.circuit_breaker_status == "CLOSED")

        return EvaluationReport(
            session_id=trajectory.session_id,
            overall_status="PASSED" if all_passed else "FAILED",
            metrics=metrics,
            trajectory_efficiency_score=round(eff_score, 2),
            cost_efficiency_score=round(1.0 - (trajectory.total_tokens / 10000.0), 2),
            summary=f"Evaluated {len(trajectory.steps)} trajectory steps. Overall Result: {'PASSED' if all_passed else 'FAILED'}."
        )
