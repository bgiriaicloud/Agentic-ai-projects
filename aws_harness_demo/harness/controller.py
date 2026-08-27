"""
Master AWS AgentCore Harness Controller.
Integrates Amazon Bedrock Guardrails, Lambda Firecracker MicroVM Sandboxing, CloudWatch Circuit Breakers, and Bedrock Automated Evaluations.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import uuid
import time
from .guardrails import AWSBedrockGuardrailHarness, AWSGuardrailResult
from .sandbox import AWSFirecrackerSandbox, AWSSandboxExecutionResult
from .telemetry import AWSTelemetryHarness, AWSCircuitBreakerTrippedException, AWSTrajectoryLog
from .evals import AWSBedrockEvaluator, AWSEvaluationReport

@dataclass
class AWSHarnessOutput:
    session_id: str
    success: bool
    output_text: str
    error_message: Optional[str] = None
    trajectory: Optional[AWSTrajectoryLog] = None
    evaluation_report: Optional[AWSEvaluationReport] = None
    execution_time_seconds: float = 0.0

class AWSAgentHarness:
    """
    Production-grade AWS AgentCore Harness orchestrator.
    Guarantees that Amazon Bedrock Agents execute exclusively inside safe, measured, and sandboxed boundaries.
    """
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or f"aws-harness-{uuid.uuid4().hex[:8]}"
        self.guardrails = AWSBedrockGuardrailHarness()
        self.sandbox = AWSFirecrackerSandbox()
        self.telemetry = AWSTelemetryHarness(session_id=self.session_id)
        self.evaluator = AWSBedrockEvaluator()

    def run_safe_agent(self, user_goal: str, agent_fn, grounding_context: str = "") -> AWSHarnessOutput:
        """
        Executes an Amazon Bedrock Agent task within the protected AWS Harness.
        
        Lifecycle:
        1. [Bedrock Guardrails Input Filter] Intercepts prompt attacks & content violations
        2. [CloudWatch & X-Ray Start] Initializes trace segment and budget ledger
        3. [Execution Loop] Runs Agent with Firecracker MicroVM Action Group execution & Circuit Breakers
        4. [Output Guardrail] Checks Contextual Grounding & Masks PII / AWS Keys
        5. [Amazon Bedrock Evaluation] Grades trajectory using automated evaluation benchmarks
        """
        start_time = time.time()
        self.telemetry.start_trace(user_goal)

        # -------------------------------------------------------------
        # STEP 1: Amazon Bedrock Guardrails Input Filter
        # -------------------------------------------------------------
        input_guard = self.guardrails.validate_input(user_goal)
        if not input_guard.is_safe:
            self.telemetry.log_guardrail_verdict("INPUT_GUARDRAIL_BLOCKED", {
                "reason": input_guard.blocked_reason,
                "categories": input_guard.categories_detected
            })
            return AWSHarnessOutput(
                session_id=self.session_id,
                success=False,
                output_text="[INTERCEPTED BY AMAZON BEDROCK GUARDRAILS]",
                error_message=input_guard.blocked_reason,
                trajectory=self.telemetry.trajectory,
                evaluation_report=None,
                execution_time_seconds=time.time() - start_time
            )

        # -------------------------------------------------------------
        # STEP 2 & 3: Run Agent in Sandbox with Circuit Breakers
        # -------------------------------------------------------------
        try:
            raw_response = agent_fn(
                goal=user_goal,
                sandbox=self.sandbox,
                telemetry=self.telemetry
            )
        except AWSCircuitBreakerTrippedException as cb_err:
            return AWSHarnessOutput(
                session_id=self.session_id,
                success=False,
                output_text="[AWS CIRCUIT BREAKER TERMINATION]",
                error_message=str(cb_err),
                trajectory=self.telemetry.trajectory,
                evaluation_report=None,
                execution_time_seconds=time.time() - start_time
            )
        except Exception as e:
            return AWSHarnessOutput(
                session_id=self.session_id,
                success=False,
                output_text="[AGENT RUNTIME ERROR]",
                error_message=str(e),
                trajectory=self.telemetry.trajectory,
                evaluation_report=None,
                execution_time_seconds=time.time() - start_time
            )

        # -------------------------------------------------------------
        # STEP 4: Output Guardrail (Bedrock Contextual Grounding & PII)
        # -------------------------------------------------------------
        output_guard = self.guardrails.validate_output(raw_response, grounding_context=grounding_context)
        if not output_guard.is_safe:
            self.telemetry.log_guardrail_verdict("OUTPUT_GUARDRAIL_BLOCKED", {
                "reason": output_guard.blocked_reason,
                "categories": output_guard.categories_detected
            })
            return AWSHarnessOutput(
                session_id=self.session_id,
                success=False,
                output_text="[OUTPUT BLOCKED BY BEDROCK GUARDRAILS]",
                error_message=output_guard.blocked_reason,
                trajectory=self.telemetry.trajectory,
                evaluation_report=None,
                execution_time_seconds=time.time() - start_time
            )

        final_response_text = output_guard.anonymized_output if output_guard.anonymized_output else raw_response

        # -------------------------------------------------------------
        # STEP 5: Amazon Bedrock Automated Model Evaluation
        # -------------------------------------------------------------
        eval_report = self.evaluator.evaluate_session(
            user_intent=user_goal,
            agent_response=final_response_text,
            context=grounding_context,
            trajectory=self.telemetry.trajectory
        )

        return AWSHarnessOutput(
            session_id=self.session_id,
            success=True,
            output_text=final_response_text,
            error_message=None,
            trajectory=self.telemetry.trajectory,
            evaluation_report=eval_report,
            execution_time_seconds=round(time.time() - start_time, 2)
        )
