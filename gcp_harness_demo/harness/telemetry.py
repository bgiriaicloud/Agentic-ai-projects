"""
Google Cloud Trace & Cloud Logging OpenTelemetry Harness with Circuit Breakers.
Tracks agent trajectories, tool spans, token quotas, and enforces deterministic circuit breakers.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import time
from ..config import settings, policy

class GCPCircuitBreakerTrippedException(Exception):
    """Raised when safety, token quotas, or iteration limits are exceeded on GCP."""
    pass

@dataclass
class GCPStepSpan:
    step_number: int
    span_name: str
    input_data: str
    output_data: str
    tokens_used: int
    duration_ms: float
    status: str # "OK", "ERROR", "CIRCUIT_BREAKER_TRIPPED"

@dataclass
class GCPTrajectoryLog:
    session_id: str
    goal: str
    spans: List[GCPStepSpan] = field(default_factory=list)
    total_tokens: int = 0
    total_latency_ms: float = 0.0
    circuit_breaker_state: str = "CLOSED" # CLOSED (Healthy), OPEN (Tripped)
    guardrail_audit_log: List[Dict[str, Any]] = field(default_factory=list)

class GCPTelemetryHarness:
    """
    Harness component collecting distributed OpenTelemetry spans into Google Cloud Trace & Cloud Logging.
    """
    def __init__(self, session_id: str = "gcp-agent-session-001"):
        self.session_id = session_id
        self.policy = policy
        self.trajectory = GCPTrajectoryLog(session_id=session_id, goal="")
        self.start_time = time.time()
        self.consecutive_errors = 0

    def start_trace(self, goal: str):
        self.trajectory.goal = goal
        self.start_time = time.time()

    def record_span(self, span_name: str, input_data: str, output_data: str, tokens: int, duration_ms: float, success: bool = True):
        step_num = len(self.trajectory.spans) + 1
        
        self.trajectory.total_tokens += tokens
        self.trajectory.total_latency_ms += duration_ms
        
        if not success:
            self.consecutive_errors += 1
        else:
            self.consecutive_errors = 0

        span = GCPStepSpan(
            step_number=step_num,
            span_name=span_name,
            input_data=input_data,
            output_data=output_data,
            tokens_used=tokens,
            duration_ms=duration_ms,
            status="OK" if success else "ERROR"
        )
        self.trajectory.spans.append(span)

        # Enforce Cloud Circuit Breakers
        self._evaluate_circuit_breakers(step_num)

    def _evaluate_circuit_breakers(self, current_step: int):
        # 1. Step Quota Circuit Breaker
        if current_step > self.policy.max_steps_per_task:
            self.trajectory.circuit_breaker_state = "OPEN"
            raise GCPCircuitBreakerTrippedException(
                f"🚨 GCP Circuit Breaker Tripped: Exceeded maximum reasoning steps ({self.policy.max_steps_per_task}). Agent terminated."
            )

        # 2. Vertex AI Token Budget Circuit Breaker
        if self.trajectory.total_tokens > self.policy.max_tokens_budget:
            self.trajectory.circuit_breaker_state = "OPEN"
            raise GCPCircuitBreakerTrippedException(
                f"🚨 GCP Circuit Breaker Tripped: Vertex AI token budget ({self.policy.max_tokens_budget}) breached. Total: {self.trajectory.total_tokens}."
            )

        # 3. Consecutive Error Trip
        if self.consecutive_errors >= self.policy.max_consecutive_tool_failures:
            self.trajectory.circuit_breaker_state = "OPEN"
            raise GCPCircuitBreakerTrippedException(
                f"🚨 GCP Circuit Breaker Tripped: {self.consecutive_errors} consecutive tool failures intercepted. Aborting to avoid cascade."
            )

        # 4. Session Deadline Timeout
        elapsed = time.time() - self.start_time
        if elapsed > self.policy.max_execution_timeout_seconds:
            self.trajectory.circuit_breaker_state = "OPEN"
            raise GCPCircuitBreakerTrippedException(
                f"🚨 GCP Circuit Breaker Tripped: Session exceeded SLA deadline of {self.policy.max_execution_timeout_seconds}s."
            )

    def audit_guardrail_event(self, event_type: str, details: Dict[str, Any]):
        self.trajectory.guardrail_audit_log.append({
            "timestamp": time.time(),
            "event_type": event_type,
            "details": details
        })
