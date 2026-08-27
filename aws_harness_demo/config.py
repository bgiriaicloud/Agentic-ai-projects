"""
Configuration and policies for AWS Harness Engineering Demo.
Includes Amazon Bedrock settings, Bedrock Guardrails thresholds, and CloudWatch circuit breakers.
"""

from dataclasses import dataclass, field
import os

@dataclass
class AWSSettings:
    # AWS Region & Identity
    aws_region: str = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    aws_account_id: str = os.getenv("AWS_ACCOUNT_ID", "123456789012")
    
    # Amazon Bedrock Agent Core Config
    bedrock_model_id: str = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")
    agent_id: str = os.getenv("BEDROCK_AGENT_ID", "agent-core-prod-001")
    agent_alias_id: str = os.getenv("BEDROCK_AGENT_ALIAS_ID", "LIVE")
    
    # Amazon Bedrock Guardrails Identifier
    guardrail_id: str = os.getenv("BEDROCK_GUARDRAIL_ID", "gr-enterprise-safety-001")
    guardrail_version: str = os.getenv("BEDROCK_GUARDRAIL_VERSION", "1")
    
    # AWS Lambda / Firecracker MicroVM Action Group Endpoint
    lambda_action_group_arn: str = os.getenv(
        "LAMBDA_ACTION_GROUP_ARN", 
        "arn:aws:lambda:us-east-1:123456789012:function:BedrockAgentActionGroupSandbox"
    )

@dataclass
class AWSHarnessPolicy:
    # Circuit Breakers & Resource Limits
    max_steps_per_task: int = 6                  # Max reasoning/action iterations before trip
    max_tokens_budget: int = 8000                # Hard ceiling on tokens per session
    max_execution_timeout_seconds: float = 30.0  # Session SLA deadline
    max_consecutive_action_failures: int = 2     # Halt cascading action group errors
    
    # Bedrock Guardrail Thresholds (BLOCK_HIGH, BLOCK_MEDIUM, BLOCK_LOW)
    content_filter_strength: str = "HIGH"
    
    # Contextual Grounding Thresholds (0.0 to 1.0)
    min_grounding_score: float = 0.70
    min_relevance_score: float = 0.75
    block_on_prompt_attack: bool = True

settings = AWSSettings()
policy = AWSHarnessPolicy()
