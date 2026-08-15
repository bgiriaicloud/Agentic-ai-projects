"""
Unit Test Suite for Google Cloud Enterprise Agent Platform
"""

import unittest
from gcp_agent_platform_sdk import AgentPlatformRuntime, GovernanceGuardrails
from agent import GCPEnterpriseAgent


class TestGCPAgentPlatform(unittest.TestCase):
    def setUp(self):
        self.runtime = AgentPlatformRuntime(execution_mode="mock", project_id="gcp-10-project")
        self.agent = GCPEnterpriseAgent(self.runtime)

    def test_pillar_scale_session_runtime(self):
        """Test SCALE Pillar: Isolated session creation and state persistence."""
        session = self.runtime.create_session(metadata={"env": "production"})
        self.assertTrue(session.session_id.startswith("gcp-agent-"))
        self.assertEqual(session.project_id, "gcp-10-project")

    def test_pillar_build_vertex_extensions(self):
        """Test BUILD Pillar: Vertex Extension registration and invocation."""
        exts = self.runtime.extensions.list_extensions()
        ext_names = [e["name"] for e in exts]
        self.assertIn("vertex_ai_search", ext_names)
        self.assertIn("bigquery_finops_tool", ext_names)
        self.assertIn("vertex_code_interpreter", ext_names)

        # Invoke BigQuery FinOps tool
        res = self.runtime.extensions.invoke_extension("bigquery_finops_tool", {"dataset": "billing_export"})
        self.assertEqual(res["total_gcp_spend_usd"], 2581.30)

    def test_pillar_govern_responsible_ai_eval(self):
        """Test GOVERN Pillar: Grounding verification and Responsible AI checks."""
        gov_eval = self.runtime.governance.evaluate(
            user_prompt="Check GKE clusters",
            generated_text="GKE Autopilot manages cluster infrastructure.",
            tool_outputs=[{"snippet": "GKE Autopilot managed"}]
        )
        self.assertTrue(gov_eval.safety_passed)
        self.assertEqual(gov_eval.grounding_status, "VERIFIED")
        self.assertGreaterEqual(gov_eval.grounding_score, 0.70)

    def test_full_enterprise_agent_cycle(self):
        """Test complete turn across all 4 Pillars (Build, Scale, Govern, Optimize)."""
        session = self.runtime.create_session()
        prompt = "Run Vertex AI search for GKE and query BigQuery costs"

        result = self.agent.run(session.session_id, prompt)

        self.assertEqual(result["session_id"], session.session_id)
        self.assertIn("Vertex AI Search Grounding", result["response"])
        self.assertIn("BigQuery Billing Analysis", result["response"])

        # Check GOVERN Governance Audit
        self.assertTrue(result["governance"]["safety_passed"])

        # Check OPTIMIZE Telemetry Traces
        self.assertTrue(len(result["traces"]) >= 5)


if __name__ == "__main__":
    unittest.main()
