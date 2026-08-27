"""
Azure Agent Harness Controller.
Wraps the agent execution loop with full safety guardrails, sandboxing, circuit breakers, and telemetry.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import uuid
import time
from .guardrails import AzureGuardrailHarness, GuardrailResult
from .sandbox import AzureDynamicSessionSandbox, SandboxExecutionResult
from .telemetry import AzureTelemetryHarness, CircuitBreakerTrippedException, TrajectoryLog
from .evals import AzureAIStudioEvaluator, EvaluationReport

@dataclass
class HarnessExecutionOutput:
    session_id: str
    success: bool
    output_text: str
    error_message: Optional[str] = None
    trajectory: Optional[TrajectoryLog] = None
    evaluation_report: Optional[EvaluationReport] = None
    execution_time_seconds: float = 0.0

class AzureAgentHarness:
    """
    The Master Production Harness.
    Guarantees that an Agent cannot run without safety checks, isolated runtime, and observability.
    """
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or f"az-harness-{uuid.uuid4().hex[:8]}"
        self.guardrails = AzureGuardrailHarness()
        self.sandbox = AzureDynamicSessionSandbox()
        self.telemetry = AzureTelemetryHarness(session_id=self.session_id)
        self.evaluator = AzureAIStudioEvaluator()

    def run_safe_session(self, user_goal: str, agent_fn, grounding_context: str = "") -> HarnessExecutionOutput:
        """
        Executes a complete agent task inside the protected Azure Harness.
        
        Lifecycle:
        1. [Input Guardrail] Check Prompt Shield & Content Safety
        2. [Telemetry Start] Initialize trace context and budget limits
        3. [Execution Loop] Run Agent with Sandboxed Tool access & Circuit Breakers
        4. [Output Guardrail] Verify PII, toxicity, and groundedness
        5. [Evaluation Harness] Run Azure AI Studio benchmarks and generate report
        """
        start_time = time.time()
        self.telemetry.start_session(user_goal)

        # -------------------------------------------------------------
        # STEP 1: Input Guardrail (Prompt Shield & Azure Content Safety)
        # -------------------------------------------------------------
        input_guard_res = self.guardrails.validate_input(user_goal)
        if not input_guard_res.is_safe:
            self.telemetry.log_guardrail_event("INPUT_BLOCKED", {
                "reason": input_guard_res.blocked_reason,
                "categories": input_guard_res.categories_detected
            })
            return HarnessExecutionOutput(
                session_id=self.session_id,
                success=False,
                output_text="[BLOCKED BY AZURE HARNESS]",
                error_message=input_guard_res.blocked_reason,
                trajectory=self.telemetry.trajectory,
                evaluation_report=None,
                execution_time_seconds=time.time() - start_time
            )

        # -------------------------------------------------------------
        # STEP 2 & 3: Run Agent within Circuit Breakers & Sandbox Access
        # -------------------------------------------------------------
        try:
            raw_response = agent_fn(
                goal=user_goal,
                sandbox=self.sandbox,
                telemetry=self.telemetry
            )
        except CircuitBreakerTrippedException as cb_err:
            return HarnessExecutionOutput(
                session_id=self.session_id,
                success=False,
                output_text="[CIRCUIT BREAKER TERMINATION]",
                error_message=str(cb_err),
                trajectory=self.telemetry.trajectory,
                evaluation_report=None,
                execution_time_seconds=time.time() - start_time
            )
        except Exception as e:
            return HarnessExecutionOutput(
                session_id=self.session_id,
                success=False,
                output_text="[EXECUTION ERROR]",
                error_message=f"Agent runtime error: {str(e)}",
                trajectory=self.telemetry.trajectory,
                evaluation_report=None,
                execution_time_seconds=time.time() - start_time
            )

        # -------------------------------------------------------------
        # STEP 4: Output Guardrail (Content Safety & Groundedness)
        # -------------------------------------------------------------
        output_guard_res = self.guardrails.validate_output(raw_response, grounding_context=grounding_context)
        if not output_guard_res.is_safe:
            self.telemetry.log_guardrail_event("OUTPUT_BLOCKED", {
                "reason": output_guard_res.blocked_reason,
                "categories": output_guard_res.categories_detected
            })
            return HarnessExecutionOutput(
                session_id=self.session_id,
                success=False,
                output_text="[OUTPUT BLOCKED BY AZURE HARNESS]",
                error_message=output_guard_res.blocked_reason,
                trajectory=self.telemetry.trajectory,
                evaluation_report=None,
                execution_time_seconds=time.time() - start_time
            )

        # -------------------------------------------------------------
        # STEP 5: Continuous Evaluation (Azure AI Studio Evaluation SDK)
        # -------------------------------------------------------------
        eval_report = self.evaluator.evaluate_trajectory(
            query=user_goal,
            final_response=raw_response,
            context=grounding_context,
            trajectory=self.telemetry.trajectory
        )

        return HarnessExecutionOutput(
            session_id=self.session_id,
            success=True,
            output_text=raw_response,
            error_message=None,
            trajectory=self.telemetry.trajectory,
            evaluation_report=eval_report,
            execution_time_seconds=round(time.time() - start_time, 2)
        )
