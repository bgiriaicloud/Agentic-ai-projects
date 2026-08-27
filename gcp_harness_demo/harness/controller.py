"""
Master GCP Agent Harness Controller.
Integrates Model Armor, gVisor Sandboxed Execution, Circuit Breakers, Cloud Trace, and Vertex AI Evaluation.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import uuid
import time
from .guardrails import GCPGuardrailHarness, GCPGuardrailResult
from .sandbox import GCPgVisorSandbox, GCPSandboxExecutionResult
from .telemetry import GCPTelemetryHarness, GCPCircuitBreakerTrippedException, GCPTrajectoryLog
from .evals import VertexAIEvaluator, GCPEvaluationReport

@dataclass
class GCPHarnessOutput:
    session_id: str
    success: bool
    output_text: str
    error_message: Optional[str] = None
    trajectory: Optional[GCPTrajectoryLog] = None
    evaluation_report: Optional[GCPEvaluationReport] = None
    latency_seconds: float = 0.0

class GCPAgentHarness:
    """
    Production-grade GCP Harness orchestrator for Vertex AI Agents.
    """
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or f"gcp-harness-{uuid.uuid4().hex[:8]}"
        self.guardrails = GCPGuardrailHarness()
        self.sandbox = GCPgVisorSandbox()
        self.telemetry = GCPTelemetryHarness(session_id=self.session_id)
        self.evaluator = VertexAIEvaluator()

    def run_safe_agent(self, user_goal: str, agent_fn, grounding_context: str = "") -> GCPHarnessOutput:
        """
        Executes a Gemini Agent task within the GCP Harness boundary.
        
        Lifecycle:
        1. [Model Armor Input Filter] Intercepts direct prompt injections & toxic input
        2. [Cloud Trace Start] Initializes OpenTelemetry distributed spans & budget limits
        3. [Execution Loop] Runs Agent with gVisor sandbox tool invocation & Circuit Breakers
        4. [Output Guardrail] Checks Groundedness & Cloud DLP sensitive data redaction
        5. [Vertex AI Evaluation] Grades trajectory using GenAI Evaluation Service
        """
        start_time = time.time()
        self.telemetry.start_trace(user_goal)

        # -------------------------------------------------------------
        # STEP 1: Google Cloud Model Armor Input Screen
        # -------------------------------------------------------------
        input_guard = self.guardrails.validate_input(user_goal)
        if not input_guard.is_safe:
            self.telemetry.audit_guardrail_event("MODEL_ARMOR_BLOCKED", {
                "reason": input_guard.blocked_reason,
                "categories": input_guard.categories_detected
            })
            return GCPHarnessOutput(
                session_id=self.session_id,
                success=False,
                output_text="[INTERCEPTED BY GOOGLE CLOUD MODEL ARMOR]",
                error_message=input_guard.blocked_reason,
                trajectory=self.telemetry.trajectory,
                evaluation_report=None,
                latency_seconds=time.time() - start_time
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
        except GCPCircuitBreakerTrippedException as cb_err:
            return GCPHarnessOutput(
                session_id=self.session_id,
                success=False,
                output_text="[GCP CIRCUIT BREAKER TERMINATION]",
                error_message=str(cb_err),
                trajectory=self.telemetry.trajectory,
                evaluation_report=None,
                latency_seconds=time.time() - start_time
            )
        except Exception as e:
            return GCPHarnessOutput(
                session_id=self.session_id,
                success=False,
                output_text="[AGENT RUNTIME ERROR]",
                error_message=str(e),
                trajectory=self.telemetry.trajectory,
                evaluation_report=None,
                latency_seconds=time.time() - start_time
            )

        # -------------------------------------------------------------
        # STEP 4: Output Guardrail (Vertex AI Groundedness & Cloud DLP)
        # -------------------------------------------------------------
        output_guard = self.guardrails.validate_output(raw_response, grounding_context=grounding_context)
        if not output_guard.is_safe:
            self.telemetry.audit_guardrail_event("OUTPUT_GUARD_BLOCKED", {
                "reason": output_guard.blocked_reason,
                "categories": output_guard.categories_detected
            })
            return GCPHarnessOutput(
                session_id=self.session_id,
                success=False,
                output_text="[OUTPUT BLOCKED BY VERTEX AI GUARDRAIL]",
                error_message=output_guard.blocked_reason,
                trajectory=self.telemetry.trajectory,
                evaluation_report=None,
                latency_seconds=time.time() - start_time
            )

        final_text = output_guard.redacted_output if output_guard.redacted_output else raw_response

        # -------------------------------------------------------------
        # STEP 5: Vertex AI GenAI Evaluation Service
        # -------------------------------------------------------------
        eval_report = self.evaluator.evaluate(
            prompt=user_goal,
            response=final_text,
            context=grounding_context,
            trajectory=self.telemetry.trajectory
        )

        return GCPHarnessOutput(
            session_id=self.session_id,
            success=True,
            output_text=final_text,
            error_message=None,
            trajectory=self.telemetry.trajectory,
            evaluation_report=eval_report,
            latency_seconds=round(time.time() - start_time, 2)
        )
