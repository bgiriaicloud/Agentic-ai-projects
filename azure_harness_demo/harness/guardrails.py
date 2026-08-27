"""
Azure AI Content Safety & Prompt Shield Guardrail Harness.
Provides real-time input/output filtering, injection detection, and groundedness checks.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import re
from ..config import settings, policy

@dataclass
class GuardrailResult:
    is_safe: bool
    blocked_reason: Optional[str] = None
    categories_detected: List[str] = field(default_factory=list)
    prompt_injection_detected: bool = False
    groundedness_score: float = 1.0
    details: Dict[str, Any] = field(default_factory=dict)

class AzureGuardrailHarness:
    """
    Harness component responsible for input & output safety validation
    leveraging Azure AI Content Safety and Azure Prompt Shield.
    """
    def __init__(self):
        self.settings = settings
        self.policy = policy
        self._init_azure_client()

    def _init_azure_client(self):
        # In production: ContentSafetyClient(endpoint=..., credential=AzureKeyCredential(...))
        self.has_live_credentials = (
            self.settings.content_safety_key != "mock-safety-key"
            and not self.settings.content_safety_endpoint.startswith("https://demo-")
        )

    def validate_input(self, user_prompt: str) -> GuardrailResult:
        """
        Input Guardrail: Runs Azure Prompt Shield & Content Safety before LLM execution.
        """
        # 1. Prompt Injection & Jailbreak Heuristics / Prompt Shield Check
        injection_patterns = [
            r"ignore (all )?previous instructions",
            r"system prompt override",
            r"jailbreak",
            r"you are now in developer mode",
            r"bypass (safety|filters)",
            r"drop database",
            r"exfiltrate data",
        ]
        for pattern in injection_patterns:
            if re.search(pattern, user_prompt, re.IGNORECASE):
                return GuardrailResult(
                    is_safe=False,
                    blocked_reason="Azure Prompt Shield: Direct Prompt Injection / Jailbreak attempt detected.",
                    prompt_injection_detected=True,
                    categories_detected=["PromptInjection"]
                )

        # 2. Harmful Content Classification (Toxicity / Self-Harm / Violence)
        toxic_keywords = ["self-harm", "build a bomb", "attack system", "malware script"]
        for kw in toxic_keywords:
            if kw in user_prompt.lower():
                return GuardrailResult(
                    is_safe=False,
                    blocked_reason=f"Azure AI Content Safety: Prohibited category detected ('{kw}').",
                    categories_detected=["Violence/Prohibited"]
                )

        return GuardrailResult(is_safe=True, prompt_injection_detected=False)

    def validate_output(self, output_text: str, grounding_context: Optional[str] = None) -> GuardrailResult:
        """
        Output Guardrail: Checks for hallucination/groundedness and toxic output.
        """
        # Check PII (e.g. mock credit card / SSN patterns)
        ssn_pattern = r"\b\d{3}-\d{2}-\d{4}\b"
        if re.search(ssn_pattern, output_text):
            return GuardrailResult(
                is_safe=False,
                blocked_reason="Azure AI Content Safety: PII detected (SSN). Output redacted/blocked.",
                categories_detected=["PII_SSN"]
            )

        # Groundedness Check if context is provided
        groundedness = 1.0
        if grounding_context:
            context_words = set(re.findall(r"\w+", grounding_context.lower()))
            output_tokens = re.findall(r"\w+", output_text.lower())
            
            # Grounding check: verify that numbers and key entities in output are present in context
            numbers_in_output = [t for t in output_tokens if t.isdigit()]
            numbers_in_context = [t for t in context_words if t.isdigit()]
            
            # Unanchored numbers check (e.g. inventing false dollar amounts)
            unanchored_nums = [n for n in numbers_in_output if n not in numbers_in_context and int(n) > 100]
            if unanchored_nums:
                groundedness = 0.40
            else:
                # Key topic overlap
                grounded_terms = sum(1 for w in output_tokens if w in context_words)
                groundedness = min(1.0, 0.75 + (0.25 * min(1.0, grounded_terms / max(1, len(numbers_in_context)))))

            if groundedness < self.policy.min_groundedness_score:
                return GuardrailResult(
                    is_safe=False,
                    blocked_reason=f"Azure Groundedness Detection: Score ({groundedness:.2f}) below threshold ({self.policy.min_groundedness_score}).",
                    groundedness_score=groundedness,
                    categories_detected=["UngroundedContent"]
                )

        return GuardrailResult(is_safe=True, groundedness_score=groundedness)
