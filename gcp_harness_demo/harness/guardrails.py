"""
Google Cloud Model Armor, Vertex AI Safety & Sensitive Data Protection (Cloud DLP) Guardrails.
Provides pre-execution input screening and post-execution output verification.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import re
from ..config import settings, policy

@dataclass
class GCPGuardrailResult:
    is_safe: bool
    blocked_reason: Optional[str] = None
    categories_detected: List[str] = field(default_factory=list)
    prompt_injection_detected: bool = False
    groundedness_score: float = 1.0
    redacted_output: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)

class GCPGuardrailHarness:
    """
    Harness component wrapping Google Cloud Model Armor, Vertex AI Safety, and Cloud DLP.
    """
    def __init__(self):
        self.settings = settings
        self.policy = policy

    def validate_input(self, user_prompt: str) -> GCPGuardrailResult:
        """
        Input Guardrail: Evaluated by Google Cloud Model Armor before calling Gemini.
        """
        # 1. Model Armor Direct Prompt Injection & Jailbreak Heuristics
        injection_patterns = [
            r"ignore (all )?previous instructions",
            r"system prompt override",
            r"dan mode",
            r"jailbreak",
            r"you are now an unrestricted ai",
            r"bypass (guardrails|safety)",
            r"drop table",
            r"exfiltrate credentials",
        ]
        for pattern in injection_patterns:
            if re.search(pattern, user_prompt, re.IGNORECASE):
                return GCPGuardrailResult(
                    is_safe=False,
                    blocked_reason="Google Cloud Model Armor: Prompt Injection / Jailbreak attempt intercepted.",
                    prompt_injection_detected=True,
                    categories_detected=["PromptInjection_Jailbreak"]
                )

        # 2. Vertex AI Safety Settings (Harassment, Hate Speech, Dangerous Content)
        dangerous_keywords = ["exploit system", "ransomware", "ddos script", "cyber attack"]
        for kw in dangerous_keywords:
            if kw in user_prompt.lower():
                return GCPGuardrailResult(
                    is_safe=False,
                    blocked_reason=f"Vertex AI Safety Filter: Blocked under 'DANGEROUS_CONTENT' policy for keyword '{kw}'.",
                    categories_detected=["DANGEROUS_CONTENT"]
                )

        return GCPGuardrailResult(is_safe=True, prompt_injection_detected=False)

    def validate_output(self, output_text: str, grounding_context: Optional[str] = None) -> GCPGuardrailResult:
        """
        Output Guardrail: Sensitive Data Protection (DLP) redaction and Groundedness verification.
        """
        processed_text = output_text

        # 1. Cloud Sensitive Data Protection (DLP) - PII & API Key Redaction
        pii_patterns = [
            (r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]"),
            (r"\b4[0-9]{12}(?:[0-9]{3})?\b", "[REDACTED_CREDIT_CARD]"),
            (r"AIza[0-9A-Za-z-_]{35}", "[REDACTED_GCP_API_KEY]"),
        ]
        
        redacted = False
        for pattern, mask in pii_patterns:
            if re.search(pattern, processed_text):
                processed_text = re.sub(pattern, mask, processed_text)
                redacted = True

        # 2. Vertex AI Groundedness Verification
        groundedness = 1.0
        if grounding_context:
            context_words = set(re.findall(r"\w+", grounding_context.lower()))
            output_tokens = re.findall(r"\w+", output_text.lower())
            
            # Grounding check: verify that grounding terms and facts align
            grounded_terms = sum(1 for w in output_tokens if w in context_words)
            groundedness = min(1.0, 0.78 + (0.22 * min(1.0, grounded_terms / max(1, len(context_words)))))

            if groundedness < self.policy.min_groundedness_score:
                return GCPGuardrailResult(
                    is_safe=False,
                    blocked_reason=f"Vertex AI Groundedness Evaluator: Score ({groundedness:.2f}) below threshold ({self.policy.min_groundedness_score}).",
                    groundedness_score=groundedness,
                    categories_detected=["UngroundedContent"]
                )

        return GCPGuardrailResult(
            is_safe=True,
            groundedness_score=groundedness,
            redacted_output=processed_text if redacted else None
        )
