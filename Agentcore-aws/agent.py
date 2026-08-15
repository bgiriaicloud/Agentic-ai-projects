"""
Amazon AgentCore - Cloud FinOps & Infrastructure Agent
-------------------------------------------------------
Demonstrates building an autonomous AI Agent using Amazon AgentCore SDK primitives:
- Runtime session execution
- Memory context & long-term fact storage
- Tool Gateway dispatch with Model Context Protocol (MCP)
- Code Sandbox execution
- Observability tracing
"""

import time
import math
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from agentcore_sdk import (
    AgentCoreRuntime,
    CodeInterpreterSandbox,
    TraceStep,
    Message
)


# ==========================================
# Tool Handlers for AgentCore Gateway
# ==========================================

def aws_cloud_cost_calculator(service: str, instance_type: str, count: int, hours_per_month: int = 730) -> Dict[str, Any]:
    """
    Calculates estimated AWS monthly cost for compute and database resources.
    """
    rates = {
        "ec2": {"t3.micro": 0.0104, "t3.medium": 0.0416, "t3.large": 0.0832, "m5.large": 0.096, "c5.xlarge": 0.17},
        "rds": {"db.t3.medium": 0.068, "db.r5.large": 0.24, "db.m5.xlarge": 0.38},
        "s3": {"standard_per_gb": 0.023, "glacier_per_gb": 0.004}
    }
    
    svc_lower = service.lower()
    inst_lower = instance_type.lower()

    if svc_lower in rates and inst_lower in rates[svc_lower]:
        hourly_rate = rates[svc_lower][inst_lower]
        monthly_cost = round(hourly_rate * count * hours_per_month, 2)
        yearly_cost = round(monthly_cost * 12, 2)
        
        # Savings plan / Reserved Instance estimates
        ri_1yr_savings = round(monthly_cost * 0.35, 2)
        
        return {
            "service": service,
            "instance_type": instance_type,
            "count": count,
            "hourly_rate_usd": hourly_rate,
            "monthly_cost_usd": monthly_cost,
            "yearly_cost_usd": yearly_cost,
            "reserved_instance_1yr_savings_usd": ri_1yr_savings,
            "recommendation": f"Enrolling in a 1-year Savings Plan for {count} x {instance_type} will save ~${ri_1yr_savings}/month."
        }
    
    # Default fallback calculation
    default_monthly = round(0.10 * count * hours_per_month, 2)
    return {
        "service": service,
        "instance_type": instance_type,
        "count": count,
        "monthly_cost_usd": default_monthly,
        "recommendation": "Estimated using standard cloud pricing benchmarks."
    }


def s3_log_analyzer(bucket_name: str, scan_depth: str = "deep") -> Dict[str, Any]:
    """
    Analyzes S3 bucket storage lifecycle and identifies cost savings opportunities.
    """
    return {
        "bucket_name": bucket_name,
        "scan_depth": scan_depth,
        "total_objects": 1_450_000,
        "total_size_gb": 850.5,
        "unaccessed_objects_over_90days_gb": 520.0,
        "estimated_monthly_savings_usd": round(520.0 * (0.023 - 0.004), 2),
        "suggested_action": "Transition 520 GB of unaccessed logs to S3 Glacier Flexible Retrieval to save $9.88/month."
    }


def execute_python_sandbox(code: str) -> Dict[str, Any]:
    """
    Executes code in the AgentCore Code Interpreter sandbox.
    """
    return CodeInterpreterSandbox.execute_python_code(code)


# ==========================================
# AgentCore Agent Class
# ==========================================

class FinOpsAgentCoreAgent:
    def __init__(self, runtime: AgentCoreRuntime):
        self.runtime = runtime
        self._register_gateway_tools()

    def _register_gateway_tools(self):
        """Register tools on the AgentCore Gateway using MCP definitions."""
        self.runtime.gateway.register_tool(
            name="aws_cloud_cost_calculator",
            description="Calculates estimated AWS monthly cost and Savings Plan recommendations for EC2, RDS, and S3.",
            parameters_schema={
                "service": {"type": "string", "enum": ["ec2", "rds", "s3"]},
                "instance_type": {"type": "string"},
                "count": {"type": "integer"},
                "hours_per_month": {"type": "integer", "default": 730}
            },
            handler=aws_cloud_cost_calculator
        )

        self.runtime.gateway.register_tool(
            name="s3_log_analyzer",
            description="Scans S3 storage buckets for unaccessed data and suggests Glacier lifecycle policies.",
            parameters_schema={
                "bucket_name": {"type": "string"},
                "scan_depth": {"type": "string", "default": "deep"}
            },
            handler=s3_log_analyzer
        )

        self.runtime.gateway.register_tool(
            name="code_interpreter_sandbox",
            description="Executes Python code in the AgentCore Code Interpreter sandbox.",
            parameters_schema={
                "code": {"type": "string"}
            },
            handler=execute_python_sandbox
        )

    def run(self, session_id: str, prompt: str) -> Dict[str, Any]:
        """
        Executes a turn of the AgentCore agent reasoning loop:
        1. Context & Long-Term Memory Retrieval
        2. Thought Planning & Tool Selection
        3. AgentCore Gateway Tool Dispatch
        4. Response Synthesis & Memory Persistence
        5. Observability Telemetry Recording
        """
        t0 = time.time()
        
        # Ensure session exists
        session = self.runtime.get_session(session_id)
        if not session:
            session = self.runtime.create_session()
            session_id = session.session_id

        # Step 1: Record User Message & Memory Context
        self.runtime.memory.add_message(session_id=session_id, role="user", content=prompt)
        history = self.runtime.memory.get_history(session_id)
        facts = self.runtime.memory.get_long_term_facts(session_id)

        self.runtime.observability.record_step(
            session_id=session_id,
            component="Memory",
            action="Load Context",
            details={"history_turns": len(history), "persistent_facts": list(facts.keys())},
            duration_ms=(time.time() - t0) * 1000
        )

        # Step 2: Reasoning & Tool Selection
        t1 = time.time()
        tool_calls = []
        lower_p = prompt.lower()

        if "cost" in lower_p or "ec2" in lower_p or "instance" in lower_p or "monthly" in lower_p:
            # Extract count if present
            count = 4 if "4" in lower_p else (2 if "2" in lower_p else 1)
            inst = "t3.large" if "t3.large" in lower_p else ("m5.large" if "m5.large" in lower_p else "t3.medium")
            tool_calls.append({
                "name": "aws_cloud_cost_calculator",
                "args": {"service": "ec2", "instance_type": inst, "count": count}
            })

        if "s3" in lower_p or "bucket" in lower_p or "log" in lower_p or "storage" in lower_p:
            tool_calls.append({
                "name": "s3_log_analyzer",
                "args": {"bucket_name": "production-app-logs-prod", "scan_depth": "deep"}
            })

        if "code" in lower_p or "calculate" in lower_p or "python" in lower_p:
            tool_calls.append({
                "name": "code_interpreter_sandbox",
                "args": {"code": "def calc_roi(cost, savings): return round((savings / cost) * 100, 2)\nprint('ROI:', calc_roi(240, 84))"}
            })

        self.runtime.observability.record_step(
            session_id=session_id,
            component="Planner",
            action="Generate Thought Plan",
            details={"selected_tools": [tc["name"] for tc in tool_calls]},
            duration_ms=(time.time() - t1) * 1000
        )

        # Step 3: Gateway Tool Execution
        tool_results = []
        for tc in tool_calls:
            t_start = time.time()
            try:
                result = self.runtime.gateway.invoke_tool(tc["name"], tc["args"])
                dur = (time.time() - t_start) * 1000
                tool_results.append({"tool": tc["name"], "status": "success", "output": result})
                
                self.runtime.observability.record_step(
                    session_id=session_id,
                    component="Gateway",
                    action=f"Execute Tool '{tc['name']}'",
                    details={"args": tc["args"], "result": result},
                    duration_ms=dur
                )
            except Exception as e:
                dur = (time.time() - t_start) * 1000
                tool_results.append({"tool": tc["name"], "status": "error", "error": str(e)})
                
                self.runtime.observability.record_step(
                    session_id=session_id,
                    component="Gateway",
                    action=f"Execute Tool Error '{tc['name']}'",
                    details={"error": str(e)},
                    duration_ms=dur
                )

        # Step 4: Answer Synthesis
        t2 = time.time()
        synthesis_parts = [f"### Amazon AgentCore Response for Session `{session_id}`\n"]

        if tool_results:
            synthesis_parts.append("Here is the analysis and tool execution report generated by Amazon AgentCore:\n")
            for tr in tool_results:
                if tr["status"] == "success":
                    out = tr["output"]
                    if tr["tool"] == "aws_cloud_cost_calculator":
                        synthesis_parts.append(
                            f"- **Cloud Cost Analysis**: {out['count']} x `{out['instance_type']}` EC2 instances cost **${out['monthly_cost_usd']}/month** (${out['yearly_cost_usd']}/year)."
                            f"\n  * {out['recommendation']}"
                        )
                        # Save long-term memory fact
                        self.runtime.memory.set_long_term_fact(session_id, "monthly_ec2_budget", out["monthly_cost_usd"])
                    elif tr["tool"] == "s3_log_analyzer":
                        synthesis_parts.append(
                            f"- **S3 Bucket Optimization** (`{out['bucket_name']}`): Identified **{out['unaccessed_objects_over_90days_gb']} GB** of stale logs."
                            f"\n  * {out['suggested_action']}"
                        )
                        self.runtime.memory.set_long_term_fact(session_id, "s3_potential_savings", out["estimated_monthly_savings_usd"])
                    elif tr["tool"] == "code_interpreter_sandbox":
                        synthesis_parts.append(
                            f"- **Code Interpreter Execution**: Output -> `{out['stdout']}` (Ran in {out['execution_time_ms']}ms)."
                        )
        else:
            synthesis_parts.append(f"I've processed your request regarding **'{prompt}'**. How can I assist with your AWS cloud operations or architecture today?")

        final_response = "\n\n".join(synthesis_parts)

        # Store Assistant Response in Memory
        self.runtime.memory.add_message(session_id=session_id, role="assistant", content=final_response)

        self.runtime.observability.record_step(
            session_id=session_id,
            component="Runtime",
            action="Synthesize & Save Response",
            details={"output_tokens_est": len(final_response.split()) * 1.3},
            duration_ms=(time.time() - t2) * 1000
        )

        total_latency_ms = round((time.time() - t0) * 1000, 2)

        return {
            "session_id": session_id,
            "prompt": prompt,
            "response": final_response,
            "tool_results": tool_results,
            "long_term_memory": self.runtime.memory.get_long_term_facts(session_id),
            "traces": [t.model_dump() for t in self.runtime.observability.get_traces(session_id)],
            "metrics": {
                "total_latency_ms": total_latency_ms,
                "tool_calls_count": len(tool_calls),
                "execution_mode": self.runtime.execution_mode
            }
        }
