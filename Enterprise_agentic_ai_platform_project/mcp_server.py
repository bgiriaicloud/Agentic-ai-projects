import os
import json
from fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("GCP Knowledge Base Server")

# Mock External Knowledge Base (Company Cloud Infrastructure Documentation)
MOCK_KNOWLEDGE_BASE = {
    "gcp_networking": {
        "title": "GCP Networking Standard Architecture",
        "description": "Standard configurations for Google Cloud VPC networks.",
        "content": (
            "All production systems must leverage a Shared VPC topology. Host projects "
            "manage subnets, firewalls, and HA VPN gateways. Service projects attach compute instances "
            "directly to subnets using Workload Identity. Public IPs are strictly forbidden for production "
            "VM instances; all egress internet traffic must route through Cloud NAT gateways."
        )
    },
    "cloud_run_rules": {
        "title": "Google Cloud Run Deployment Guardrails",
        "description": "Compliance guidelines for container deployment on Cloud Run.",
        "content": (
            "Cloud Run service deployments must enforce ingress restrictions: only internal "
            "and load balancer traffic is allowed for backend services. Always set maximum scale limits "
            "to prevent run-away autoscaling token billing. Environment secrets must be loaded dynamically "
            "from GCP Secret Manager; never hardcode credentials inside the Dockerfile."
        )
    },
    "security_standard": {
        "title": "Enterprise Zero-Trust IAM Policy",
        "description": "Identity & Access Management baseline rules.",
        "content": (
            "Workload Identity must be used for GKE and VM connections. Access is restricted using "
            "VPC Service Controls (VPC-SC) perimeters. Customer-Managed Encryption Keys (CMEK) managed "
            "via Cloud KMS are mandatory for encrypting Cloud Storage buckets and BigQuery datasets containing PII."
        )
    }
}

@mcp.tool()
def query_knowledge_base(topic_id: str) -> str:
    """Queries the external knowledge base for GCP architecture guidelines.

    Args:
        topic_id: The identifier of the topic. Allowed values: 'gcp_networking', 'cloud_run_rules', 'security_standard'.
    """
    topic = MOCK_KNOWLEDGE_BASE.get(topic_id.lower().strip())
    if not topic:
        allowed = ", ".join(MOCK_KNOWLEDGE_BASE.keys())
        return f"Error: Topic '{topic_id}' not found. Available topics: {allowed}"
    
    return json.dumps({
        "status": "success",
        "title": topic["title"],
        "description": topic["description"],
        "content": topic["content"]
    }, indent=2)

@mcp.tool()
def list_knowledge_topics() -> str:
    """Lists all available documentation topics in the external knowledge base."""
    topics = []
    for key, value in MOCK_KNOWLEDGE_BASE.items():
        topics.append({
            "topic_id": key,
            "title": value["title"],
            "description": value["description"]
        })
    return json.dumps(topics, indent=2)

if __name__ == "__main__":
    mcp.run()
