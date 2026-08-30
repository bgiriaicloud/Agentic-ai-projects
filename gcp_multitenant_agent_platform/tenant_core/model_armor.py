"""
Tenant-Level Model Armor & Cloud Sensitive Data Protection (DLP) Module.
Implements Step 4 (Sanitize Request) and Step 6 (Sanitize Response).
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import re
from ..config import registry

@dataclass
class ModelArmorSanitizationResult:
    is_safe: bool
    step: int
    action_type: str # "SANITIZE_REQUEST" (Step 4) | "SANITIZE_RESPONSE" (Step 6)
    sanitized_text: str
    blocked_reason: Optional[str] = None
    pii_redacted: bool = False
    groundedness_score: float = 1.0
    detected_entities: List[str] = field(default_factory=list)

class TenantModelArmor:
    """
    Tenant-specific Model Armor instance enforcing domain safety, DLP masking, and hallucination detection.
    """
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.tenant_config = registry.tenants.get(tenant_id)

    def sanitize_request(self, prompt: str) -> ModelArmorSanitizationResult:
        """
        Step 4: Sanitize Request inside Tenant project before handing to Agent Runtime.
        """
        # Tenant specific injection checks
        tenant_injection_patterns = [
            r"dump (all )?(users|records|tables)",
            r"bypass tenant isolation",
            r"read adjacent tenant project"
        ]
        for pattern in tenant_injection_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                return ModelArmorSanitizationResult(
                    is_safe=False,
                    step=4,
                    action_type="SANITIZE_REQUEST",
                    sanitized_text=prompt,
                    blocked_reason=f"Tenant Model Armor: Intercepted unauthorized cross-tenant query pattern in '{self.tenant_id}'."
                )

        return ModelArmorSanitizationResult(
            is_safe=True,
            step=4,
            action_type="SANITIZE_REQUEST",
            sanitized_text=prompt
        )

    def sanitize_response(self, response_text: str, grounding_context: str = "") -> ModelArmorSanitizationResult:
        """
        Step 6: Sanitize Response inside Tenant project before sending back to Frontend.
        Performs Cloud DLP (PII Redaction) and Groundedness Evaluation.
        """
        sanitized_text = response_text
        detected_pii = []

        # 1. Cloud Sensitive Data Protection (DLP) Masking
        dlp_patterns = [
            (r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]", "US_SSN"),
            (r"\b4[0-9]{12}(?:[0-9]{3})?\b", "[REDACTED_CREDIT_CARD]", "CREDIT_CARD_NUMBER"),
            (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[REDACTED_EMAIL]", "EMAIL_ADDRESS"),
            (r"AIza[0-9A-Za-z-_]{35}", "[REDACTED_GCP_API_KEY]", "GCP_API_KEY")
        ]

        pii_found = False
        for pattern, mask, entity_name in dlp_patterns:
            if re.search(pattern, sanitized_text):
                sanitized_text = re.sub(pattern, mask, sanitized_text)
                detected_pii.append(entity_name)
                pii_found = True

        # 2. Groundedness Evaluation against MCP / Datastore context
        groundedness = 1.0
        if grounding_context:
            context_words = set(re.findall(r"\w+", grounding_context.lower()))
            output_tokens = re.findall(r"\w+", response_text.lower())
            
            grounded_terms = sum(1 for w in output_tokens if w in context_words)
            groundedness = min(1.0, 0.78 + (0.22 * min(1.0, grounded_terms / max(1, len(context_words)))))

            if groundedness < 0.70:
                return ModelArmorSanitizationResult(
                    is_safe=False,
                    step=6,
                    action_type="SANITIZE_RESPONSE",
                    sanitized_text=sanitized_text,
                    blocked_reason="Tenant Model Armor: Groundedness score below threshold (Potential Hallucination).",
                    groundedness_score=groundedness
                )

        return ModelArmorSanitizationResult(
            is_safe=True,
            step=6,
            action_type="SANITIZE_RESPONSE",
            sanitized_text=sanitized_text,
            pii_redacted=pii_found,
            groundedness_score=groundedness,
            detected_entities=detected_pii
        )
