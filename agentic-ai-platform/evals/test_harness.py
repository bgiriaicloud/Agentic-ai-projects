"""
Evaluation Test Harness - Enterprise Agentic AI Platform
---------------------------------------------------------
Automated test suite verifying A2A orchestration, tool execution, grounding scores, and latency targets.
"""

import unittest
from agents.supervisor_agent import SupervisorAgent
from mcp_servers.mcp_gcp_server import mcp_server
from tools.custom_tools import calculate_cloud_cost


class TestAgenticPlatformHarness(unittest.TestCase):
    def setUp(self):
        self.supervisor = SupervisorAgent(name="Supervisor-Architect")

    def test_mcp_server_tools(self):
        """Test FastMCP server resource listing and billing queries."""
        resources = mcp_server.call_tool("list_gcp_resources", region="us-central1")
        self.assertEqual(len(resources["gke_clusters"]), 1)
        self.assertEqual(len(resources["compute_vms"]), 2)

        billing = mcp_server.call_tool("query_bigquery_billing", dataset_id="billing_export_v1")
        self.assertEqual(billing["monthly_gcp_spend_usd"], 2581.30)

    def test_custom_tools_calculation(self):
        """Test custom cloud cost calculation tool."""
        res = calculate_cloud_cost("gcp", "n2-standard-4", 4)
        self.assertEqual(res["monthly_cost_usd"], 554.80)

    def test_supervisor_a2a_orchestration(self):
        """Test Supervisor Master Agent delegating to CloudOps & FinOps worker agents."""
        prompt = "Perform full infrastructure audit and calculate BigQuery billing costs"
        result = self.supervisor.orchestrate(prompt)

        self.assertIn("session_id", result)
        self.assertEqual(len(result["subagent_outputs"]), 2)
        self.assertIn("CloudOps-Subagent", [o["subagent"] for o in result["subagent_outputs"]])
        self.assertIn("FinOps-Subagent", [o["subagent"] for o in result["subagent_outputs"]])

    def test_latency_performance_target(self):
        """Test that execution meets sub-1500ms latency targets."""
        result = self.supervisor.orchestrate("Quick check FinOps costs")
        self.assertLess(result["metrics"]["total_latency_ms"], 1500)


if __name__ == "__main__":
    unittest.main()
