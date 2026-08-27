"""
AWS CloudWatch & AWS X-Ray OpenTelemetry Telemetry Harness with Circuit Breakers.
Collects distributed trace segments, tracks token consumption ledger, and enforces circuit breakers.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import time
from ..config import settings, policy

class AWSCircuitBreakerTrippedException(Exception):
    """Raised when safety, cost, or reasoning loop limits are exceeded on AWS."""
    pass

@dataclass
class AWSSegmentSpan:
    segment_number: int
    segment_name: str
    input_payload: str
    output_payload: str
    tokens_consumed: int
    duration_ms: float
    status: str # "SUCCESS", "ERROR", "TRIPPED"

@dataclass
class AWSTrajectoryLog:
    session_id: str
    task_goal: str
    segments: List[AWSSegmentSpan] = field(default_factory=list)
    total_tokens: int = 0
    total_latency_ms: float = 0.0
    circuit_breaker_status: str = "CLOSED" # CLOSED (Healthy), OPEN (Tripped)
    guardrail_audit_records: List[Dict[str, Any]] = field(default_factory=list)

class AWSTelemetryHarness:
    """
    Harness component collecting distributed OpenTelemetry traces into AWS CloudWatch & AWS X-Ray.
    """
    def __init__(self, session_id: str = "aws-agentcore-session-001"):
        self.session_id = session_id
        self.policy = policy
        self.trajectory = AWSTrajectoryLog(session_id=session_id, task_goal="")
        self.start_time = time.time()
        self.consecutive_errors = 0

    def start_trace(self, task_goal: str):
        self.trajectory.task_goal = task_goal
        self.start_time = time.time()

    def record_segment(self, segment_name: str, input_payload: str, output_payload: str, tokens: int, duration_ms: float, success: bool = True):
        segment_num = len(self.trajectory.segments) + 1
        
        self.trajectory.total_tokens += tokens
        self.trajectory.total_latency_ms += duration_ms
        
        if not success:
            self.consecutive_errors += 1
        else:
            self.consecutive_errors = 0

        segment = AWSSegmentSpan(
            segment_number=segment_num,
            segment_name=segment_name,
            input_payload=input_payload,
            output_payload=output_payload,
            tokens_consumed=tokens,
            duration_ms=duration_ms,
            status="SUCCESS" if success else "ERROR"
        )
        self.trajectory.segments.append(segment)

        # Evaluate AWS Circuit Breaker Thresholds
        self._evaluate_circuit_breakers(segment_num)

    def _evaluate_circuit_breakers(self, current_step: int):
        # 1. Step Quota Limit
        if current_step > self.policy.max_steps_per_task:
            self.trajectory.circuit_breaker_status = "OPEN"
            raise AWSCircuitBreakerTrippedException(
                f"🚨 AWS Circuit Breaker Tripped: Maximum reasoning iterations ({self.policy.max_steps_per_task}) exceeded. Agent halted."
            )

        # 2. Token Budget Ledger Ceilings
        if self.trajectory.total_tokens > self.policy.max_tokens_budget:
            self.trajectory.circuit_breaker_status = "OPEN"
            raise AWSCircuitBreakerTrippedException(
                f"🚨 AWS Circuit Breaker Tripped: Bedrock token ceiling ({self.policy.max_tokens_budget}) breached. Total: {self.trajectory.total_tokens}."
            )

        # 3. Consecutive Action Group Error Breaker
        if self.consecutive_errors >= self.policy.max_consecutive_action_failures:
            self.trajectory.circuit_breaker_status = "OPEN"
            raise AWSCircuitBreakerTrippedException(
                f"🚨 AWS Circuit Breaker Tripped: {self.consecutive_errors} consecutive Action Group errors intercepted. Halting agent to protect AWS resources."
            )

        # 4. SLA Execution Timeout
        elapsed = time.time() - self.start_time
        if elapsed > self.policy.max_execution_timeout_seconds:
            self.trajectory.circuit_breaker_status = "OPEN"
            raise AWSCircuitBreakerTrippedException(
                f"🚨 AWS Circuit Breaker Tripped: Session execution time ({elapsed:.1f}s) exceeded {self.policy.max_execution_timeout_seconds}s limit."
            )

    def log_guardrail_verdict(self, event_type: str, details: Dict[str, Any]):
        self.trajectory.guardrail_audit_records.append({
            "timestamp": time.time(),
            "event_type": event_type,
            "details": details
        })
