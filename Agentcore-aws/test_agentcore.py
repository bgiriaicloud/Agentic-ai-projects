"""
Unit Test Suite for Amazon AgentCore SDK & Agent
"""

import unittest
from agentcore_sdk import AgentCoreRuntime, CodeInterpreterSandbox
from agent import FinOpsAgentCoreAgent


class TestAgentCoreFramework(unittest.TestCase):
    def setUp(self):
        self.runtime = AgentCoreRuntime(execution_mode="mock")
        self.agent = FinOpsAgentCoreAgent(self.runtime)

    def test_session_creation(self):
        """Test session container creation and runtime isolation."""
        session = self.runtime.create_session(metadata={"env": "testing"})
        self.assertTrue(session.session_id.startswith("agentcore-session-"))
        self.assertIsNotNone(self.runtime.get_session(session.session_id))

    def test_gateway_tool_registration_and_invocation(self):
        """Test gateway MCP tool registration and handler execution."""
        tools = self.runtime.gateway.list_tools()
        tool_names = [t["name"] for t in tools]
        self.assertIn("aws_cloud_cost_calculator", tool_names)
        self.assertIn("s3_log_analyzer", tool_names)
        self.assertIn("code_interpreter_sandbox", tool_names)

        # Invoke cost calculator tool
        res = self.runtime.gateway.invoke_tool("aws_cloud_cost_calculator", {"service": "ec2", "instance_type": "t3.large", "count": 4})
        self.assertEqual(res["monthly_cost_usd"], 242.94)

    def test_code_interpreter_sandbox(self):
        """Test code interpreter sandbox Python execution."""
        code = "a = 20\nb = 30\nprint(f'Sum: {a + b}')"
        res = CodeInterpreterSandbox.execute_python_code(code)
        self.assertTrue(res["success"])
        self.assertEqual(res["stdout"], "Sum: 50")

    def test_full_agent_turn_execution(self):
        """Test complete AgentCore agent turn execution with memory and tracing."""
        session = self.runtime.create_session()
        prompt = "Calculate monthly cost for 4 EC2 t3.large instances and scan S3 log bucket"
        
        result = self.agent.run(session.session_id, prompt)
        
        self.assertEqual(result["session_id"], session.session_id)
        self.assertIn("Cloud Cost Analysis", result["response"])
        self.assertIn("S3 Bucket Optimization", result["response"])
        
        # Verify Memory Fact Retention
        self.assertIn("monthly_ec2_budget", result["long_term_memory"])
        self.assertEqual(result["long_term_memory"]["monthly_ec2_budget"]["value"], 242.94)
        
        # Verify Observability Traces
        self.assertTrue(len(result["traces"]) >= 4)


if __name__ == "__main__":
    unittest.main()
