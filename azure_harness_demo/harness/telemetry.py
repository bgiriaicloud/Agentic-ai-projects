"""
Azure Application Insights & OpenTelemetry Telemetry Harness with Circuit Breakers.
Tracks agent trajectories, tool invocations, token spend, and trips circuit breakers on budget/loop anomalies.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import time
from ..config import settings, policy

class CircuitBreakerTrippedException(Exception):
    """Raised when safety, cost, or loop limits are breached."""
    pass

@dataclass
class StepRecord:
    step_number: int
    action_type: str
    input_payload: str
    output_payload: str
    tokens_consumed: int
    duration_ms: float
    status: str # "SUCCESS", "FAILED", "TRIPPED"

@dataclass
class TrajectoryLog:
    session_id: str
    task_goal: str
    steps: List[StepRecord] = field(default_factory=list)
    total_tokens: int = 0
    total_duration_ms: float = 0.0
    circuit_breaker_status: str = "CLOSED" # CLOSED (Normal), OPEN (Tripped)
    guardrail_events: List[Dict[str, Any]] = field(default_factory=list)

class AzureTelemetryHarness:
    """
    Harness component providing full trajectory observability and circuit breaker enforcement.
    Connects to Azure Monitor / Application Insights via OpenTelemetry.
    """
    def __init__(self, session_id: str = "azure-agent-session-001"):
        self.session_id = session_id
        self.policy = policy
        self.trajectory = TrajectoryLog(session_id=session_id, task_goal="")
        self.start_time = time.time()
        self.consecutive_failures = 0

    def start_session(self, task_goal: str):
        self.trajectory.task_goal = task_goal
        self.start_time = time.time()

    def record_step(self, action_type: str, input_payload: str, output_payload: str, tokens: int, duration_ms: float, success: bool = True):
        step_num = len(self.trajectory.steps) + 1
        
        # 1. Update Metrics
        self.trajectory.total_tokens += tokens
        self.trajectory.total_duration_ms += duration_ms
        
        if not success:
            self.consecutive_failures += 1
        else:
            self.consecutive_failures = 0

        record = StepRecord(
            step_number=step_num,
            action_type=action_type,
            input_payload=input_payload,
            output_payload=output_payload,
            tokens_consumed=tokens,
            duration_ms=duration_ms,
            status="SUCCESS" if success else "FAILED"
        )
        self.trajectory.steps.append(record)

        # 2. Evaluate Circuit Breakers
        self._check_circuit_breakers(step_num)

    def _check_circuit_breakers(self, current_step: int):
        # A. Max Steps Circuit Breaker
        if current_step > self.policy.max_steps_per_task:
            self.trajectory.circuit_breaker_status = "OPEN"
            raise CircuitBreakerTrippedException(
                f"🚨 Circuit Breaker Tripped: Maximum reasoning steps ({self.policy.max_steps_per_task}) exceeded. Agent loop terminated."
            )

        # B. Token Budget Circuit Breaker
        if self.trajectory.total_tokens > self.policy.max_tokens_budget:
            self.trajectory.circuit_breaker_status = "OPEN"
            raise CircuitBreakerTrippedException(
                f"🚨 Circuit Breaker Tripped: Token ceiling ({self.policy.max_tokens_budget}) exceeded. Total spent: {self.trajectory.total_tokens}."
            )

        # C. Consecutive Failure Circuit Breaker
        if self.consecutive_failures >= self.policy.max_consecutive_tool_failures:
            self.trajectory.circuit_breaker_status = "OPEN"
            raise CircuitBreakerTrippedException(
                f"🚨 Circuit Breaker Tripped: {self.consecutive_failures} consecutive tool failures detected. Halting execution to prevent cascade."
            )

        # D. Session Timeout Check
        elapsed = time.time() - self.start_time
        if elapsed > self.policy.max_execution_timeout_seconds:
            self.trajectory.circuit_breaker_status = "OPEN"
            raise CircuitBreakerTrippedException(
                f"🚨 Circuit Breaker Tripped: Session execution time ({elapsed:.1f}s) exceeded timeout limit ({self.policy.max_execution_timeout_seconds}s)."
            )

    def log_guardrail_event(self, event_type: str, details: Dict[str, Any]):
        self.trajectory.guardrail_events.append({
            "timestamp": time.time(),
            "event_type": event_type,
            "details": details
        })
