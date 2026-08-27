"""
GCP FastMCP Server - Enterprise Agentic AI Platform
----------------------------------------------------
Exposes GCP infrastructure, GKE cluster, and BigQuery billing tools via Model Context Protocol (MCP).
"""

from typing import Dict, Any, List

class FastMCPServer:
    def __init__(self, name: str = "GCP-MCP-Server"):
        self.name = name
        self._tools = {}
        self._register_default_tools()

    def _register_default_tools(self):
        self._tools["list_gcp_resources"] = {
            "description": "Lists mock GCP Compute Engine, GKE clusters, and Cloud Run services.",
            "handler": self.list_gcp_resources
        }
        self._tools["query_bigquery_billing"] = {
            "description": "Queries BigQuery billing export dataset for monthly GCP spend breakdown.",
            "handler": self.query_bigquery_billing
        }

    def list_gcp_resources(self, region: str = "us-central1") -> Dict[str, Any]:
        return {
            "region": region,
            "gke_clusters": [
                {"name": "production-autopilot-cluster", "status": "RUNNING", "nodes": 12, "location": region}
            ],
            "compute_vms": [
                {"name": "api-gateway-vm-1", "type": "n2-standard-4", "status": "RUNNING"},
                {"name": "worker-node-vm-2", "type": "e2-medium", "status": "RUNNING"}
            ],
            "cloud_run_services": [
                {"name": "mcp-server-sse", "url": "https://mcp-server-sse-uc.a.run.app", "instances": 3}
            ]
        }

    def query_bigquery_billing(self, dataset_id: str = "billing_export_v1") -> Dict[str, Any]:
        return {
            "dataset_id": dataset_id,
            "monthly_gcp_spend_usd": 2581.30,
            "breakdown": {
                "compute_engine": 1450.80,
                "gke_autopilot": 820.00,
                "bigquery": 310.50
            },
            "potential_cud_savings_usd": 435.00
        }

    def list_tools() -> List[Dict[str, str]]:
        return [
            {"name": k, "description": v["description"]}
            for k, v in self._tools.items()
        ]

    def call_tool(self, tool_name: str, **kwargs) -> Any:
        if tool_name not in self._tools:
            raise ValueError(f"MCP Tool '{tool_name}' not found on {self.name}.")
        return self._tools[tool_name]["handler"](**kwargs)


mcp_server = FastMCPServer()
