"""
Master Multi-Tenant Platform Orchestrator.
Executes the full 7-step lifecycle depicted in the Google Cloud Enterprise Multi-Tenant Architecture.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
import time
from .config import registry
from .shared_hub.routing_hub import RoutingHubIngress, IngressResult
from .shared_hub.governance_hub import GovernanceSecurityHub, AuditEvent
from .tenant_core.pab_boundary import PABBoundaryEnforcer, PABValidationResult
from .tenant_core.model_armor import TenantModelArmor, ModelArmorSanitizationResult
from .tenant_core.agent_runtime import TenantAgentRuntime, AgentExecutionResult

@dataclass
class PlatformExecutionReport:
    success: bool
    final_step_reached: int
    user_identity: str
    tenant_id: str
    final_response: str
    error_reason: Optional[str] = None
    step_trace: List[Dict[str, Any]] = field(default_factory=list)
    total_latency_ms: float = 0.0

class GCPMultiTenantPlatform:
    """
    Simulates the complete Google Cloud Multi-Tenant Agent Platform.
    """
    def __init__(self):
        self.governance_hub = GovernanceSecurityHub()
        self.routing_hub = RoutingHubIngress(self.governance_hub)

    def handle_user_request(
        self,
        user_identity: str,
        user_role: str,
        target_tenant_id: str,
        user_prompt: str
    ) -> PlatformExecutionReport:
        """
        Executes Steps 1 to 7.
        """
        start_time = time.time()
        trace = []

        # -------------------------------------------------------------
        # STEP 1 & 2: Routing Hub (ALB -> Cloud Armor -> Central Model Armor -> IAP -> Cloud Run)
        # -------------------------------------------------------------
        ingress_res = self.routing_hub.process_incoming_request(
            user_identity=user_identity,
            user_role=user_role,
            target_tenant_id=target_tenant_id,
            raw_prompt=user_prompt
        )

        trace.append({
            "step": 1,
            "name": "Central Ingress (Cloud Armor & Central Model Armor)",
            "status": "PASS" if ingress_res.waf_passed and ingress_res.model_armor_passed else "FAIL",
            "details": "WAF rules and edge prompt inspection verified."
        })

        if not ingress_res.allowed:
            return PlatformExecutionReport(
                success=False,
                final_step_reached=ingress_res.step,
                user_identity=user_identity,
                tenant_id=target_tenant_id,
                final_response="[BLOCKED AT ROUTING HUB]",
                error_reason=ingress_res.block_reason,
                step_trace=trace,
                total_latency_ms=(time.time() - start_time) * 1000
            )

        trace.append({
            "step": 2,
            "name": "Cloud Run Frontend Portal & IAP Authentication",
            "status": "PASS",
            "details": f"User authenticated via IAP with role '{user_role}'."
        })

        # -------------------------------------------------------------
        # STEP 3: Route Request to Tenant across PAB (Principal Access Boundary)
        # -------------------------------------------------------------
        pab_enforcer = PABBoundaryEnforcer(target_tenant_id)
        pab_res = pab_enforcer.validate_tenant_ingress(target_tenant_id)

        trace.append({
            "step": 3,
            "name": "PAB (Principal Access Boundary) Routing",
            "status": "PASS" if pab_res.allowed else "FAIL",
            "details": f"Routed to project '{pab_res.target_project_id}' within PAB boundary '{pab_res.pab_boundary_id}'."
        })

        if not pab_res.allowed:
            return PlatformExecutionReport(
                success=False,
                final_step_reached=3,
                user_identity=user_identity,
                tenant_id=target_tenant_id,
                final_response="[BLOCKED BY PAB BOUNDARY]",
                error_reason=pab_res.reason,
                step_trace=trace,
                total_latency_ms=(time.time() - start_time) * 1000
            )

        # -------------------------------------------------------------
        # STEP 4: Tenant Model Armor (Sanitize Request)
        # -------------------------------------------------------------
        tenant_armor = TenantModelArmor(target_tenant_id)
        req_san_res = tenant_armor.sanitize_request(ingress_res.sanitized_prompt)

        trace.append({
            "step": 4,
            "name": "Tenant Model Armor: Ingress Sanitization",
            "status": "PASS" if req_san_res.is_safe else "FAIL",
            "details": "Tenant-level prompt verification passed."
        })

        if not req_san_res.is_safe:
            return PlatformExecutionReport(
                success=False,
                final_step_reached=4,
                user_identity=user_identity,
                tenant_id=target_tenant_id,
                final_response="[BLOCKED BY TENANT MODEL ARMOR]",
                error_reason=req_san_res.blocked_reason,
                step_trace=trace,
                total_latency_ms=(time.time() - start_time) * 1000
            )

        # -------------------------------------------------------------
        # STEP 5: Agent Runtime + Gemini + MCP Servers (Secure RAG over BigQuery/AlloyDB)
        # -------------------------------------------------------------
        agent_runtime = TenantAgentRuntime(target_tenant_id)
        agent_res = agent_runtime.execute_agent_task(req_san_res.sanitized_text)

        trace.append({
            "step": 5,
            "name": f"Agent Runtime + Gemini 1.5 Pro + MCP Server ({agent_res.mcp_tool_result.datastore_target})",
            "status": "PASS",
            "details": f"Executed Secure RAG query over tenant {agent_res.mcp_tool_result.datastore_target} datastore."
        })

        # -------------------------------------------------------------
        # STEP 6: Tenant Model Armor (Sanitize Response & Cloud DLP Masking)
        # -------------------------------------------------------------
        resp_san_res = tenant_armor.sanitize_response(
            response_text=agent_res.raw_response,
            grounding_context=agent_res.grounding_corpus
        )

        trace.append({
            "step": 6,
            "name": "Tenant Model Armor: Egress Sanitization & Cloud DLP",
            "status": "PASS" if resp_san_res.is_safe else "FAIL",
            "details": f"Groundedness score: {resp_san_res.groundedness_score:.2f} | PII Redacted: {resp_san_res.pii_redacted}."
        })

        if not resp_san_res.is_safe:
            return PlatformExecutionReport(
                success=False,
                final_step_reached=6,
                user_identity=user_identity,
                tenant_id=target_tenant_id,
                final_response="[OUTPUT BLOCKED BY TENANT MODEL ARMOR]",
                error_reason=resp_san_res.blocked_reason,
                step_trace=trace,
                total_latency_ms=(time.time() - start_time) * 1000
            )

        # -------------------------------------------------------------
        # STEP 7: Route Sanitized Response from Tenant back to User
        # -------------------------------------------------------------
        trace.append({
            "step": 7,
            "name": "Return Sanitized Response to User via Cloud Run & ALB",
            "status": "PASS",
            "details": "Sanitized response delivered to caller."
        })

        self.governance_hub.record_audit(
            tenant_id=target_tenant_id,
            user_identity=user_identity,
            step=7,
            action="RESPONSE_DISPATCHED",
            status="SUCCESS",
            details={"tokens_consumed": agent_res.tokens_consumed}
        )

        return PlatformExecutionReport(
            success=True,
            final_step_reached=7,
            user_identity=user_identity,
            tenant_id=target_tenant_id,
            final_response=resp_san_res.sanitized_text,
            error_reason=None,
            step_trace=trace,
            total_latency_ms=round((time.time() - start_time) * 1000, 2)
        )
