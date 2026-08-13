from mcp.server.fastmcp import FastMCP
import os

# Create an MCP server named "GCPAssistantMCP"
mcp = FastMCP("GCPAssistantMCP")

@mcp.tool()
def list_gcp_resources(resource_type: str) -> str:
    """Lists mock active resources in a Google Cloud project by type.

    Args:
        resource_type: The type of GCP resource to list. Must be one of: 'gce_instance', 'cloud_run_service', 'gcs_bucket'.
    """
    resource_type = resource_type.strip().lower()
    if resource_type == "gce_instance":
        return (
            "Active GCE Instances in project 'enterprise-agentic-ai-prod':\n"
            "- name: supervisor-node-01, zone: us-central1-a, status: RUNNING, type: n2-standard-4\n"
            "- name: agent-worker-02, zone: us-central1-b, status: RUNNING, type: n2-standard-8\n"
            "- name: legacy-bastion, zone: us-central1-f, status: TERMINATED, type: e2-micro"
        )
    elif resource_type == "cloud_run_service":
        return (
            "Active Cloud Run Services in project 'enterprise-agentic-ai-prod':\n"
            "- service: mcp-jira-bridge, region: us-central1, status: READY, url: https://mcp-jira-bridge-x7uq.a.run.app\n"
            "- service: mcp-slack-bridge, region: us-central1, status: READY, url: https://mcp-slack-bridge-x7uq.a.run.app\n"
            "- service: agent-engine-core, region: us-east1, status: READY, url: https://agent-engine-core-x7uq.a.run.app"
        )
    elif resource_type == "gcs_bucket":
        return (
            "Active GCS Buckets in project 'enterprise-agentic-ai-prod':\n"
            "- bucket: enterprise-rag-knowledge-base, location: US-MULTI-REGIONAL, storage_class: STANDARD\n"
            "- bucket: agent-audit-logs-export, location: US-CENTRAL1, storage_class: NEARLINE\n"
            "- bucket: terraform-state-backend, location: US-CENTRAL1, storage_class: STANDARD"
        )
    else:
        return f"Unknown resource type: '{resource_type}'. Valid types are: 'gce_instance', 'cloud_run_service', 'gcs_bucket'."

if __name__ == "__main__":
    mcp.run()
