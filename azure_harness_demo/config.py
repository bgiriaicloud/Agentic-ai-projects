"""
Configuration and thresholds for Azure Harness Engineering Demo.
Includes safety thresholds, circuit breaker budgets, and Azure service settings.
"""

from dataclasses import dataclass, field
import os

@dataclass
class AzureSettings:
    # Azure OpenAI
    azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "https://demo-ai.openai.azure.com/")
    azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "mock-azure-key")
    azure_openai_deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    
    # Azure AI Content Safety & Prompt Shield
    content_safety_endpoint: str = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "https://demo-safety.cognitiveservices.azure.com/")
    content_safety_key: str = os.getenv("AZURE_CONTENT_SAFETY_KEY", "mock-safety-key")
    
    # Azure Container Apps Dynamic Sessions (Code Interpreter Sandbox)
    aca_session_pool_endpoint: str = os.getenv("ACA_SESSION_POOL_ENDPOINT", "https://eastus.dynamicsessions.io/subscriptions/demo/pool/code-sandbox")
    
    # Azure Application Insights / Monitor Connection String
    app_insights_connection_string: str = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING", "InstrumentationKey=mock-key;IngestionEndpoint=https://dc.services.visualstudio.com/")

@dataclass
class HarnessPolicy:
    # Circuit Breaker Limits
    max_steps_per_task: int = 6                 # Maximum reasoning/action iterations before trip
    max_tokens_budget: int = 8000               # Hard ceiling on tokens per session
    max_execution_timeout_seconds: float = 30.0 # Session timeout in seconds
    max_consecutive_tool_failures: int = 2      # Trip if tool fails repeatedly
    
    # Safety Thresholds (Azure AI Content Safety Severity Scale 0-7)
    max_hate_severity: int = 2
    max_self_harm_severity: int = 0
    max_sexual_severity: int = 2
    max_violence_severity: int = 2
    
    # Groundedness & Eval Thresholds (0.0 to 1.0)
    min_groundedness_score: float = 0.70
    min_relevance_score: float = 0.75
    block_on_prompt_injection: bool = True

settings = AzureSettings()
policy = HarnessPolicy()
