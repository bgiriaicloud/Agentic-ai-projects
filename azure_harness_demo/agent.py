"""
Agent Execution Layer.
Simulates a multi-step reasoning & tool-calling Agent (e.g. built with Semantic Kernel or LangGraph).
It receives the sandboxed execution environment and telemetry recorder from the Azure Harness.
"""

import time
from .harness.sandbox import AzureDynamicSessionSandbox
from .harness.telemetry import AzureTelemetryHarness

class DataAnalysisAgent:
    """
    Agent capable of planning, generating Python code, and running it in the ACA Dynamic Sessions Sandbox.
    """
    def __init__(self, name: str = "AzureDataAnalystAgent"):
        self.name = name

    def execute(self, goal: str, sandbox: AzureDynamicSessionSandbox, telemetry: AzureTelemetryHarness) -> str:
        """
        Executes a goal by running multi-step reasoning, invoking tools via the harness sandbox,
        and logging every step to telemetry.
        """
        # STEP 1: Planning / Intent Understanding
        start_t = time.time()
        plan = f"Plan for '{goal}': 1. Generate analysis script 2. Execute in ACA sandbox 3. Synthesize insights."
        telemetry.record_step(
            action_type="AGENT_PLANNING",
            input_payload=goal,
            output_payload=plan,
            tokens=350,
            duration_ms=(time.time() - start_t) * 1000,
            success=True
        )

        # STEP 2: Code Generation & Sandboxed Tool Execution
        code_start_t = time.time()
        
        # Example Python code to be run in Azure Container Apps Dynamic Sessions
        python_code = """
revenue = [120000, 145000, 160000, 195000]
growth = [(revenue[i] - revenue[i-1])/revenue[i-1] * 100 for i in range(1, len(revenue))]
avg_growth = sum(growth) / len(growth)
print(f"Average QoQ Growth: {avg_growth:.2f}% | Final Quarter Revenue: ${revenue[-1]:,}")
"""
        # Execute inside the isolated sandbox harness
        sandbox_res = sandbox.execute_python_code(python_code)
        
        telemetry.record_step(
            action_type="SANDBOX_TOOL_EXECUTION",
            input_payload=python_code.strip(),
            output_payload=sandbox_res.stdout if sandbox_res.success else sandbox_res.stderr,
            tokens=620,
            duration_ms=(time.time() - code_start_t) * 1000,
            success=sandbox_res.success
        )

        if not sandbox_res.success:
            return f"Agent failed to execute computation: {sandbox_res.stderr}"

        # STEP 3: Final Synthesis & Output Generation
        synth_start_t = time.time()
        final_answer = (
            f"Based on the sandboxed computational analysis: {sandbox_res.stdout}. "
            f"The business demonstrates robust quarterly revenue growth across all recorded periods."
        )
        telemetry.record_step(
            action_type="FINAL_SYNTHESIS",
            input_payload=sandbox_res.stdout,
            output_payload=final_answer,
            tokens=410,
            duration_ms=(time.time() - synth_start_t) * 1000,
            success=True
        )

        return final_answer
