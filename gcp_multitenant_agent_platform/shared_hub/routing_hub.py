"""
Routing Hub (Central Ingress) in Shared VPC.
Implements External Application Load Balancer, Cloud Armor, Central Model Armor, IAP, and Cloud Run Frontend Portal.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import re
import time
from ..config import registry
from .governance_hub import GovernanceSecurityHub

@dataclass
class IngressResult:
    allowed: bool
    status_code: int
    step: int
    user_identity: str
    target_tenant_id: str
    sanitized_prompt: str
    block_reason: Optional[str] = None
    waf_passed: bool = True
    model_armor_passed: bool = True
    iap_authenticated: bool = True

class RoutingHubIngress:
    """
    Central Routing Hub enforcing perimeter security and tenancy routing.
    """
    def __init__(self, governance_hub: GovernanceSecurityHub):
        self.config = registry.shared_hub
        self.governance = governance_hub

    def process_incoming_request(
        self,
        user_identity: str,
        user_role: str,
        target_tenant_id: str,
        raw_prompt: str
    ) -> IngressResult:
        """
        Step 1 & 2: External ALB -> Cloud Armor -> Central Model Armor -> IAP -> Cloud Run Frontend
        """
        # 1. Cloud Armor WAF & Security Policy Check
        sql_injection_pattern = r"(union\s+select|;\s*drop\s+table|--\s*$)"
        if re.search(sql_injection_pattern, raw_prompt, re.IGNORECASE):
            self.governance.record_audit(
                tenant_id=target_tenant_id,
                user_identity=user_identity,
                step=1,
                action="CLOUD_ARMOR_WAF_EVALUATION",
                status="BLOCKED",
                details={"reason": "Cloud Armor: OWASP SQLi / SQL injection payload detected."}
            )
            return IngressResult(
                allowed=False,
                status_code=403,
                step=1,
                user_identity=user_identity,
                target_tenant_id=target_tenant_id,
                sanitized_prompt=raw_prompt,
                block_reason="Cloud Armor: Blocked by WAF security policy (SQLi pattern detected).",
                waf_passed=False
            )

        # 2. Central Model Armor (Edge Prompt Sanitization)
        jailbreak_patterns = [
            r"ignore (all )?previous instructions",
            r"dan mode",
            r"system prompt override",
            r"exfiltrate all tenant data"
        ]
        for pattern in jailbreak_patterns:
            if re.search(pattern, raw_prompt, re.IGNORECASE):
                self.governance.record_audit(
                    tenant_id=target_tenant_id,
                    user_identity=user_identity,
                    step=1,
                    action="CENTRAL_MODEL_ARMOR_INSPECTION",
                    status="BLOCKED",
                    details={"reason": "Central Model Armor: Edge Prompt Injection / Jailbreak blocked."}
                )
                return IngressResult(
                    allowed=False,
                    status_code=400,
                    step=1,
                    user_identity=user_identity,
                    target_tenant_id=target_tenant_id,
                    sanitized_prompt=raw_prompt,
                    block_reason="Central Model Armor: Direct Prompt Injection attack intercepted at edge ingress.",
                    model_armor_passed=False
                )

        # 3. Identity-Aware Proxy (IAP) & Central IAM Authentication
        is_authorized = self.governance.check_iam_authorization(user_identity, user_role, target_tenant_id)
        if not is_authorized:
            self.governance.record_audit(
                tenant_id=target_tenant_id,
                user_identity=user_identity,
                step=2,
                action="IAP_IAM_AUTHENTICATION",
                status="BLOCKED",
                details={"reason": f"IAM Authorization failure: User '{user_identity}' lacks required role for {target_tenant_id}."}
            )
            return IngressResult(
                allowed=False,
                status_code=401,
                step=2,
                user_identity=user_identity,
                target_tenant_id=target_tenant_id,
                sanitized_prompt=raw_prompt,
                block_reason=f"Identity-Aware Proxy (IAP): User '{user_identity}' ({user_role}) is unauthorized for '{target_tenant_id}'.",
                iap_authenticated=False
            )

        # Step 2 Success: Cloud Run Frontend receives verified request
        self.governance.record_audit(
            tenant_id=target_tenant_id,
            user_identity=user_identity,
            step=2,
            action="CLOUD_RUN_FRONTEND_DISPATCH",
            status="ALLOWED",
            details={"message": "Request authenticated via IAP, validated by Cloud Armor and Central Model Armor."}
        )

        return IngressResult(
            allowed=True,
            status_code=200,
            step=2,
            user_identity=user_identity,
            target_tenant_id=target_tenant_id,
            sanitized_prompt=raw_prompt
        )
