"""
Google Cloud Enterprise Agent - Cloud Ops & FinOps Assistant
------------------------------------------------------------
Implements an Enterprise AI Agent leveraging GCP Agent Platform primitives:
- BUILD: Vertex AI Extensions (Vertex Search, BigQuery SQL, Code Sandbox)
- SCALE: Serverless session runtime
- GOVERN: Grounding & Responsible AI Safety checks
- OPTIMIZE: Chain-of-Thought Telemetry & Cost Optimization
"""

import time
import math
import sys
import io
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from gcp_agent_platform_sdk import (
    AgentPlatformRuntime,
    GovernanceAssessment,
    TelemetryTrace
)


# ==========================================
# Extension Handlers for Vertex Gateway
# ==========================================

def vertex_ai_search(query: str, datastore_id: str = "ds-gcp-architecture") -> Dict[str, Any]:
    """
    Performs grounded semantic search over GCP Enterprise Datastores.
    """
    datastore_docs = [
        {
            "id": "doc-gcp-101",
            "title": "GKE Enterprise Cluster Autopilot Best Practices",
            "snippet": "GKE Autopilot manages cluster infrastructure, node provisioning, and auto-scaling. Enabling Spot Pods can reduce compute costs by up to 60-80% for fault-tolerant workloads.",
            "confidence": 0.94
        },
        {
            "id": "doc-gcp-102",
            "title": "GCP Cloud IAM Permission Governance & Least Privilege",
            "snippet": "Enforce Service Account Key rotation every 90 days. Avoid primitive roles (Owner, Editor) and use predefined or custom IAM roles with conditional bindings.",
            "confidence": 0.91
        }
    ]
    return {
        "query": query,
        "datastore_id": datastore_id,
        "results": datastore_docs,
        "total_results": len(datastore_docs)
    }


def bigquery_finops_tool(dataset: str, query_type: str = "cost_breakdown") -> Dict[str, Any]:
    """
    Executes automated SQL analytical queries on GCP BigQuery billing exports.
    """
    return {
        "dataset": dataset,
        "query_type": query_type,
        "monthly_compute_engine_usd": 1450.80,
        "monthly_gke_cluster_usd": 820.00,
        "monthly_bigquery_slot_usd": 310.50,
        "total_gcp_spend_usd": 2581.30,
        "savings_opportunity": "Migrate 4 Compute Engine VMs to Committed Use Discounts (CUD) to save ~$435.00/month."
    }


def vertex_code_interpreter(code: str) -> Dict[str, Any]:
    """
    Executes Python code in the Vertex AI Code Interpreter sandbox.
    """
    old_stdout = sys.stdout
    redirected_output = io.StringIO()
    sys.stdout = redirected_output
    start_time = time.time()
    success = True
    error_msg = None

    try:
        exec_scope = {"math": __import__("math")}
        exec(code, exec_scope)
        output = redirected_output.getvalue()
    except Exception as e:
        success = False
        error_msg = str(e)
        output = redirected_output.getvalue()
    finally:
        sys.stdout = old_stdout

    return {
        "success": success,
        "stdout": output.strip(),
        "error": error_msg,
        "execution_time_ms": round((time.time() - start_time) * 1000, 2)
    }


# ==========================================
# GCP Enterprise Agent Implementation
# ==========================================

class GCPEnterpriseAgent:
    def __init__(self, runtime: AgentPlatformRuntime):
        self.runtime = runtime
        self._register_vertex_extensions()

    def _register_vertex_extensions(self):
        """Register extensions on the Vertex Extension Gateway."""
        self.runtime.extensions.register_extension(
            name="vertex_ai_search",
            description="Searches GCP Enterprise Datastores for architecture guides, IAM policies, and GKE documentation.",
            extension_type="vertex_search",
            parameters_schema={"query": {"type": "string"}},
            handler=vertex_ai_search
        )

        self.runtime.extensions.register_extension(
            name="bigquery_finops_tool",
            description="Queries GCP BigQuery billing export logs for resource spend and Committed Use Discounts (CUD).",
            extension_type="bigquery_sql",
            parameters_schema={"dataset": {"type": "string"}},
            handler=bigquery_finops_tool
        )

        self.runtime.extensions.register_extension(
            name="vertex_code_interpreter",
            description="Executes Python code in the Vertex AI Code Interpreter sandbox.",
            extension_type="code_sandbox",
            parameters_schema={"code": {"type": "string"}},
            handler=vertex_code_interpreter
        )

    def run(self, session_id: str, prompt: str) -> Dict[str, Any]:
        """
        Executes an enterprise agent turn across the 4 Pillars:
        1. BUILD: Reason & dispatch Vertex extensions
        2. SCALE: Isolated session runtime & memory state persistence
        3. GOVERN: Grounding verification & Responsible AI safety filters
        4. OPTIMIZE: Chain-of-Thought Telemetry & Cost optimization metrics
        """
        t0 = time.time()

        # Step 1: SCALE - Session Container Management
        session = self.runtime.get_session(session_id)
        if not session:
            session = self.runtime.create_session()
            session_id = session.session_id

        self.runtime.add_memory_message(session_id, role="user", content=prompt)

        self.runtime.optimizer.record_trace(
            session_id=session_id,
            pillar="SCALE",
            action="Load Context & State",
            details={"session_id": session_id, "project_id": self.runtime.project_id},
            latency_ms=(time.time() - t0) * 1000
        )

        # Step 2: BUILD - Extension Dispatch Selection
        t1 = time.time()
        extension_calls = []
        lower_p = prompt.lower()

        if "search" in lower_p or "gke" in lower_p or "architecture" in lower_p or "iam" in lower_p:
            extension_calls.append({"name": "vertex_ai_search", "args": {"query": prompt}})

        if "bigquery" in lower_p or "cost" in lower_p or "billing" in lower_p or "spend" in lower_p:
            extension_calls.append({"name": "bigquery_finops_tool", "args": {"dataset": "billing_export_v1"}})

        if "code" in lower_p or "python" in lower_p or "calculate" in lower_p:
            extension_calls.append({
                "name": "vertex_code_interpreter",
                "args": {"code": "cud_savings = 2581.30 * 0.17\nprint('Projected CUD Annual Savings:', round(cud_savings * 12, 2))"}
            })

        self.runtime.optimizer.record_trace(
            session_id=session_id,
            pillar="BUILD",
            action="Select Extensions & Generate Thought Plan",
            details={"extensions": [e["name"] for e in extension_calls]},
            latency_ms=(time.time() - t1) * 1000
        )

        # Execute Extensions
        extension_results = []
        for ext in extension_calls:
            ext_t0 = time.time()
            try:
                res = self.runtime.extensions.invoke_extension(ext["name"], ext["args"])
                dur = (time.time() - ext_t0) * 1000
                extension_results.append({"extension": ext["name"], "status": "success", "output": res})

                self.runtime.optimizer.record_trace(
                    session_id=session_id,
                    pillar="BUILD",
                    action=f"Execute Extension '{ext['name']}'",
                    details={"args": ext["args"], "result": res},
                    latency_ms=dur
                )
            except Exception as e:
                dur = (time.time() - ext_t0) * 1000
                extension_results.append({"extension": ext["name"], "status": "error", "error": str(e)})

        # Synthesize Answer Response
        response_parts = [f"### GCP Agent Platform Response (Project: `{self.runtime.project_id}`)\n"]

        if extension_results:
            response_parts.append("Below is the grounded enterprise intelligence generated via Vertex AI Extensions:\n")
            for er in extension_results:
                if er["status"] == "success":
                    out = er["output"]
                    if er["extension"] == "vertex_ai_search":
                        top_doc = out["results"][0]
                        response_parts.append(f"- **Vertex AI Search Grounding**: Document `{top_doc['title']}`\n  * {top_doc['snippet']}")
                    elif er["extension"] == "bigquery_finops_tool":
                        response_parts.append(
                            f"- **BigQuery Billing Analysis**: Total monthly spend **${out['total_gcp_spend_usd']} USD** (Compute: ${out['monthly_compute_engine_usd']}, GKE: ${out['monthly_gke_cluster_usd']})."
                            f"\n  * {out['savings_opportunity']}"
                        )
                        self.runtime.set_long_term_fact(session_id, "monthly_gcp_spend", out["total_gcp_spend_usd"])
                    elif er["extension"] == "vertex_code_interpreter":
                        response_parts.append(f"- **Vertex Code Interpreter**: Output -> `{out['stdout']}` (Ran in {out['execution_time_ms']}ms).")
        else:
            response_parts.append(f"I am your enterprise GCP Cloud Operations agent. I can perform Vertex AI Grounded Search, BigQuery Billing analysis, and Code Interpreter tasks.")

        grounded_response = "\n\n".join(response_parts)

        # Step 3: GOVERN - Safety & Grounding Verification
        t_gov = time.time()
        governance = self.runtime.governance.evaluate(
            user_prompt=prompt,
            generated_text=grounded_response,
            tool_outputs=[er["output"] for er in extension_results if er["status"] == "success"]
        )

        self.runtime.optimizer.record_trace(
            session_id=session_id,
            pillar="GOVERN",
            action="Perform Responsible AI & Grounding Audit",
            details=governance.model_dump(),
            latency_ms=(time.time() - t_gov) * 1000
        )

        self.runtime.add_memory_message(session_id, role="assistant", content=grounded_response)

        # Step 4: OPTIMIZE - Latency & Cost Metrics
        total_latency_ms = round((time.time() - t0) * 1000, 2)
        cost_opt = self.runtime.optimizer.calculate_cost_optimization(prompt, grounded_response, total_latency_ms)

        self.runtime.optimizer.record_trace(
            session_id=session_id,
            pillar="OPTIMIZE",
            action="Calculate Telemetry & Cost Optimization",
            details=cost_opt,
            latency_ms=total_latency_ms
        )

        return {
            "session_id": session_id,
            "project_id": self.runtime.project_id,
            "prompt": prompt,
            "response": grounded_response,
            "governance": governance.model_dump(),
            "extension_results": extension_results,
            "long_term_memory": self.runtime.get_long_term_facts(session_id),
            "traces": [t.model_dump() for t in self.runtime.optimizer.get_traces(session_id)],
            "metrics": {
                "total_latency_ms": total_latency_ms,
                "cost_optimization": cost_opt,
                "execution_mode": self.runtime.execution_mode
            }
        }
