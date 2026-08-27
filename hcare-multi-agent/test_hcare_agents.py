"""
===============================================================================
HEALTHCARE MULTI-AGENT UNIT TEST SUITE (ADK & GEMINI PLATFORM)
===============================================================================
Verifies:
1. HIPAA Compliance & PHI De-identification (SSN, Phone, Email)
2. ADK Framework Skills & Abstractions (Skills, Tools, Agents)
3. Gemini Agent Platform Grounding & Clinical Reasoning
4. A2A Communication Orchestration & Dynamic Domain Routing
5. Domain Agent Execution (Patient, Lab Test, Doctor, Insurance, Nursing, IT)
6. Latency & Execution Trace SLA
===============================================================================
"""

import unittest
from hcare_orchestrator import hospital_assistant, HealthcareQueryRequest, ADKHealthcareRegistry


class TestHealthcareMultiAgent(unittest.TestCase):
    def setUp(self):
        self.runtime = hospital_assistant

    def test_01_adk_skills_registry(self):
        """Verifies that ADK Skills are properly registered and configured."""
        self.assertIn("hipaa_compliance_skill", ADKHealthcareRegistry.SKILLS)
        self.assertIn("clinical_reasoning_skill", ADKHealthcareRegistry.SKILLS)
        self.assertIn("a2a_orchestration_skill", ADKHealthcareRegistry.SKILLS)

    def test_02_hipaa_phi_sanitization(self):
        """Verifies that HIPAA skill redacts SSNs, phone numbers, and emails."""
        raw_text = "Patient SSN is 123-45-6789 and contact is 555-892-1234 or patient@hospital.org."
        clean_text, redacted = self.runtime.execute_hipaa_deid(raw_text)
        
        self.assertNotIn("123-45-6789", clean_text)
        self.assertNotIn("555-892-1234", clean_text)
        self.assertNotIn("patient@hospital.org", clean_text)
        self.assertGreaterEqual(len(redacted), 3)

    def test_03_lab_test_agent_routing_and_fhir(self):
        """Verifies routing to Lab Test Agent and FHIR Observation retrieval."""
        req = HealthcareQueryRequest(
            patient_id="P-98421",
            user_role="Patient",
            query="What are my latest blood test and HbA1c glucose lab results?"
        )
        res = self.runtime.process_request(req)
        self.assertEqual(res.routed_agent, "Lab Test Agent")
        self.assertTrue(res.hipaa_compliant)
        self.assertIn("HbA1c", res.final_response)
        self.assertGreater(len(res.fhir_resources), 0)
        self.assertIn("hipaa_compliance_skill", res.active_skills)

    def test_04_insurance_agent_routing(self):
        """Verifies routing to Insurance Agent for claims & copay pre-auth."""
        req = HealthcareQueryRequest(
            patient_id="P-98421",
            user_role="Insurance",
            query="Verify insurance claim pre-authorization status and specialist copay."
        )
        res = self.runtime.process_request(req)
        self.assertEqual(res.routed_agent, "Insurance Agent")
        self.assertIn("BlueCross BlueShield", res.final_response)
        self.assertIn("$25.00", res.final_response)

    def test_05_doctor_agent_clinical_reasoning(self):
        """Verifies Doctor Agent clinical notes and Meta-Agent reasoning flags."""
        req = HealthcareQueryRequest(
            patient_id="P-98421",
            user_role="Doctor",
            query="Access doctor clinical notes and physician recommendation."
        )
        res = self.runtime.process_request(req)
        self.assertEqual(res.routed_agent, "Doctor Agent")
        self.assertIn("Clinical Assessment", res.clinical_reasoning)
        self.assertIn("Physician Portal", res.final_response)
        self.assertIn("Metformin", res.final_response)

    def test_06_execution_trace_and_platform_status(self):
        """Verifies ADK & Gemini Agent Platform metadata and execution SLA."""
        req = HealthcareQueryRequest(
            patient_id="P-98421",
            user_role="Admin",
            query="Check hospital ICU bed occupancy and staffing metrics."
        )
        res = self.runtime.process_request(req)
        self.assertEqual(res.routed_agent, "Hospital Admin Agent")
        self.assertIn("Google ADK", res.adk_framework_version)
        self.assertIn("ACTIVE", res.gemini_agent_platform_status)
        self.assertEqual(len(res.execution_trace), 4)
        self.assertLess(res.total_latency_seconds, 1.0)

    def test_07_gcp_secret_manager_retrieval(self):
        """Verifies that secrets are retrieved via GCPSecretManager."""
        from secret_manager import GCPSecretManager
        gemini_key = GCPSecretManager.get_gemini_api_key()
        payer_key = GCPSecretManager.get_payer_api_gateway_key()
        fhir_token = GCPSecretManager.get_fhir_auth_token()
        
        self.assertIsNotNone(gemini_key)
        self.assertIsNotNone(payer_key)
        self.assertIsNotNone(fhir_token)


if __name__ == "__main__":
    unittest.main()
