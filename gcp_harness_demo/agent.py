"""
Vertex AI Gemini Agent Execution Layer.
Simulates a multi-step reasoning agent using Vertex AI Reasoning Engine / Gemini 1.5 Pro.
Executes code and BigQuery queries safely via the GCP gVisor Sandbox Harness.
"""

import time
from .harness.sandbox import GCPgVisorSandbox
from .harness.telemetry import GCPTelemetryHarness

class VertexBigQueryDataAgent:
    """
    Agent performing multi-step reasoning, SQL generation, and gVisor sandboxed data computation.
    """
    def __init__(self, name: str = "VertexGeminiAnalystAgent"):
        self.name = name

    def execute(self, goal: str, sandbox: GCPgVisorSandbox, telemetry: GCPTelemetryHarness) -> str:
        """
        Executes goal by generating a query, executing within gVisor sandbox, and synthesizing results.
        """
        # SPAN 1: Vertex AI Gemini Intent Planning
        t0 = time.time()
        reasoning_plan = f"Vertex AI Reasoning: Goal '{goal}' parsed. 1. Generate BigQuery aggregate 2. Execute in gVisor sandbox 3. Synthesize summary."
        telemetry.record_span(
            span_name="VERTEX_AI_GEMINI_PLANNING",
            input_data=goal,
            output_data=reasoning_plan,
            tokens=380,
            duration_ms=(time.time() - t0) * 1000,
            success=True
        )

        # SPAN 2: Cloud Run / gVisor Sandboxed BigQuery & Python Calculation
        t1 = time.time()
        python_snippet = """
# Simulated BigQuery client aggregation inside gVisor sandbox
cloud_storage_tb = [450, 520, 610, 780]
compute_cores = [128, 256, 256, 512]
avg_storage = sum(cloud_storage_tb) / len(cloud_storage_tb)
max_cores = max(compute_cores)
print(f"Average Storage Usage: {avg_storage:.1f} TB | Peak Compute Cores: {max_cores}")
"""
        exec_res = sandbox.execute_python_code(python_snippet)
        telemetry.record_span(
            span_name="GVISOR_SANDBOX_BIGQUERY_TOOL",
            input_data=python_snippet.strip(),
            output_data=exec_res.stdout if exec_res.success else exec_res.stderr,
            tokens=590,
            duration_ms=(time.time() - t1) * 1000,
            success=exec_res.success
        )

        if not exec_res.success:
            return f"Agent failed to execute BigQuery tool: {exec_res.stderr}"

        # SPAN 3: Vertex AI Gemini Final Response Synthesis
        t2 = time.time()
        final_answer = (
            f"Based on GCP BigQuery data processed in gVisor sandbox: {exec_res.stdout}. "
            f"Workload resource utilization is scaling smoothly within expected GCP cloud quotas."
        )
        telemetry.record_span(
            span_name="GEMINI_FINAL_SYNTHESIS",
            input_data=exec_res.stdout,
            output_data=final_answer,
            tokens=420,
            duration_ms=(time.time() - t2) * 1000,
            success=True
        )

        return final_answer
