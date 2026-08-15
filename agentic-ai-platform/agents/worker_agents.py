"""
Worker Agents Module - Enterprise Agentic AI Platform
------------------------------------------------------
Implements specialized child subagents for Agent-to-Agent (A2A) task execution:
1. CloudOpsWorkerAgent - Manages GCP/Multi-cloud infrastructure & IAM security.
2. FinOpsWorkerAgent   - Analyzes cloud billing exports & code interpreter calculations.
"""

import time
from typing import Dict, Any, List
from tools.custom_tools import calculate_cloud_cost, check_iam_security_policy, run_code_interpreter
from mcp_servers.mcp_gcp_server import mcp_server


class CloudOpsWorkerAgent:
    def __init__(self, name: str = "CloudOps-Subagent"):
        self.name = name

    def execute_subtask(self, task_description: str) -> Dict[str, Any]:
        t0 = time.time()
        mcp_res = mcp_server.call_tool("list_gcp_resources", region="us-central1")
        iam_res = check_iam_security_policy("gcp-10-project")
        
        latency = round((time.time() - t0) * 1000, 2)
        return {
            "subagent": self.name,
            "role": "Cloud Infrastructure & IAM Security",
            "task": task_description,
            "mcp_gcp_resources": mcp_res,
            "iam_security_audit": iam_res,
            "summary": f"Scanned {len(mcp_res['compute_vms'])} VMs & {len(mcp_res['gke_clusters'])} GKE clusters. IAM Security Score: {iam_res['security_score']}/100.",
            "latency_ms": latency
        }


class FinOpsWorkerAgent:
    def __init__(self, name: str = "FinOps-Subagent"):
        self.name = name

    def execute_subtask(self, task_description: str) -> Dict[str, Any]:
        t0 = time.time()
        bq_res = mcp_server.call_tool("query_bigquery_billing", dataset_id="billing_export_v1")
        cost_calc = calculate_cloud_cost("gcp", "n2-standard-4", 4)
        code_res = run_code_interpreter("spend = 2581.30\nsavings = 435.00\nprint('Net Monthly Spend:', spend - savings)")

        latency = round((time.time() - t0) * 1000, 2)
        return {
            "subagent": self.name,
            "role": "Cloud Billing & BigQuery Analytics",
            "task": task_description,
            "bigquery_billing": bq_res,
            "cost_calculation": cost_calc,
            "code_interpreter": code_res,
            "summary": f"Total GCP Monthly Spend: ${bq_res['monthly_gcp_spend_usd']}. Identified CUD savings: ${bq_res['potential_cud_savings_usd']}/month.",
            "latency_ms": latency
        }
