"""
Configuration and policies for GCP Harness Engineering Demo.
Includes Google Cloud Vertex AI settings, Model Armor thresholds, and circuit breaker policies.
"""

from dataclasses import dataclass, field
import os

@dataclass
class GCPSettings:
    # Google Cloud Project & Location
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", "demo-gcp-ai-project")
    location: str = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
    
    # Vertex AI Model Config
    gemini_model: str = os.getenv("VERTEX_AI_MODEL", "gemini-1.5-pro")
    
    # Vertex AI Model Armor / Sensitive Data Protection (DLP)
    model_armor_template_id: str = os.getenv("MODEL_ARMOR_TEMPLATE_ID", "default-enterprise-guardrail")
    dlp_inspect_template: str = os.getenv("DLP_INSPECT_TEMPLATE", "projects/demo/inspectTemplates/pii-guard")
    
    # Cloud Run / gVisor Sandbox Endpoint
    cloud_run_sandbox_url: str = os.getenv("CLOUD_RUN_SANDBOX_URL", "https://gvisor-sandbox-run.a.run.app")

@dataclass
class GCPHarnessPolicy:
    # Circuit Breakers & Resource Ceilings
    max_steps_per_task: int = 6                  # Max reasoning / tool loops before circuit breaker trip
    max_tokens_budget: int = 8000                # Hard ceiling on tokens per session
    max_execution_timeout_seconds: float = 30.0  # Session SLA deadline
    max_consecutive_tool_failures: int = 2       # Stop cascade on repeated tool exceptions
    
    # Vertex AI Safety Settings (BLOCK_NONE, BLOCK_ONLY_HIGH, BLOCK_MEDIUM_AND_ABOVE, BLOCK_LOW_AND_ABOVE)
    safety_threshold: str = "BLOCK_MEDIUM_AND_ABOVE"
    
    # Groundedness & Evaluation Thresholds (0.0 to 1.0)
    min_groundedness_score: float = 0.70
    min_instruction_following_score: float = 0.75
    block_on_model_armor_violation: bool = True

settings = GCPSettings()
policy = GCPHarnessPolicy()
