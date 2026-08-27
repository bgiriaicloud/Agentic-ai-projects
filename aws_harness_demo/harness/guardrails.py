"""
Amazon Bedrock Guardrails Harness.
Provides real-time pre-execution Prompt Attack defense, Content Filters, Sensitive Information (PII) masking, and Contextual Grounding checks.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import re
from ..config import settings, policy

@dataclass
class AWSGuardrailResult:
    is_safe: bool
    blocked_reason: Optional[str] = None
    action: str = "NONE" # "NONE", "BLOCKED", "ANONYMIZED"
    categories_detected: List[str] = field(default_factory=list)
    prompt_attack_detected: bool = False
    grounding_score: float = 1.0
    anonymized_output: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)

class AWSBedrockGuardrailHarness:
    """
    Harness component simulating and wrapping Amazon Bedrock ApplyGuardrail API:
    POST /guardrail/{guardrailIdentifier}/version/{guardrailVersion}/apply
    """
    def __init__(self):
        self.settings = settings
        self.policy = policy

    def validate_input(self, user_prompt: str) -> AWSGuardrailResult:
        """
        Input Guardrail: Amazon Bedrock Prompt Attack & Content Filters.
        """
        # 1. Amazon Bedrock Prompt Attack Filter (Direct Prompt Injection & Jailbreaks)
        prompt_attacks = [
            r"ignore (all )?previous instructions",
            r"system prompt override",
            r"jailbreak",
            r"unrestricted developer mode",
            r"bypass (guardrails|safety)",
            r"dump aws_secret_access_key",
            r"drop table",
        ]
        for pattern in prompt_attacks:
            if re.search(pattern, user_prompt, re.IGNORECASE):
                return AWSGuardrailResult(
                    is_safe=False,
                    action="BLOCKED",
                    blocked_reason="Amazon Bedrock Guardrails: Prompt Attack / Direct Injection detected and blocked.",
                    prompt_attack_detected=True,
                    categories_detected=["PROMPT_ATTACK"]
                )

        # 2. Content Filters (Hate, Insults, Sexual, Violence)
        restricted_phrases = ["destructive cyberattack", "deploy ransomware", "illegal weapon"]
        for phrase in restricted_phrases:
            if phrase in user_prompt.lower():
                return AWSGuardrailResult(
                    is_safe=False,
                    action="BLOCKED",
                    blocked_reason=f"Amazon Bedrock Content Filter: Blocked for policy violation ('{phrase}').",
                    categories_detected=["VIOLENCE_MISCONDUCT"]
                )

        return AWSGuardrailResult(is_safe=True, action="NONE")

    def validate_output(self, output_text: str, grounding_context: Optional[str] = None) -> AWSGuardrailResult:
        """
        Output Guardrail: Bedrock Sensitive Information Filters (PII/Secrets) and Contextual Grounding.
        """
        sanitized_text = output_text

        # 1. Sensitive Information Filters (PII & AWS Credentials Masking)
        pii_rules = [
            (r"\b\d{3}-\d{2}-\d{4}\b", "[BEDROCK_MASKED_SSN]"),
            (r"\b4[0-9]{12}(?:[0-9]{3})?\b", "[BEDROCK_MASKED_CARD]"),
            (r"AKIA[0-9A-Z]{16}", "[BEDROCK_MASKED_AWS_KEY]"),
        ]
        anonymized = False
        for regex_pattern, mask in pii_rules:
            if re.search(regex_pattern, sanitized_text):
                sanitized_text = re.sub(regex_pattern, mask, sanitized_text)
                anonymized = True

        # 2. Bedrock Contextual Grounding Check
        grounding = 1.0
        if grounding_context:
            context_words = set(re.findall(r"\w+", grounding_context.lower()))
            output_tokens = re.findall(r"\w+", output_text.lower())
            
            grounded_terms = sum(1 for w in output_tokens if w in context_words)
            grounding = min(1.0, 0.78 + (0.22 * min(1.0, grounded_terms / max(1, len(context_words)))))

            if grounding < self.policy.min_grounding_score:
                return AWSGuardrailResult(
                    is_safe=False,
                    action="BLOCKED",
                    blocked_reason=f"Amazon Bedrock Contextual Grounding: Score ({grounding:.2f}) below threshold ({self.policy.min_grounding_score}).",
                    grounding_score=grounding,
                    categories_detected=["UNGROUNDED_HALLUCINATION"]
                )

        return AWSGuardrailResult(
            is_safe=True,
            action="ANONYMIZED" if anonymized else "NONE",
            grounding_score=grounding,
            anonymized_output=sanitized_text if anonymized else None
        )
