"""
Configuration and Tenant Registry for Google Cloud Multi-Tenant Agent Platform.
Includes Shared VPC Hub settings, PAB boundaries, Model Armor policies, and MCP configs.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any
import os

@dataclass
class TenantConfig:
    tenant_id: str
    project_id: str
    display_name: str
    pab_boundary_id: str
    datastore_type: str # "BigQuery" or "AlloyDB"
    allowed_roles: List[str] = field(default_factory=list)
    model_armor_policy: str = "STRICT_ENTERPRISE"
    gemini_model: str = "gemini-1.5-pro"

@dataclass
class SharedHubConfig:
    organization_id: str = "org-enterprise-gcp-9901"
    routing_hub_project: str = "gcp-shared-routing-hub"
    governance_hub_project: str = "gcp-central-governance-hub"
    region: str = "us-central1"
    
    # Cloud Armor & Model Armor Edge Policies
    cloud_armor_waf_enabled: bool = True
    central_model_armor_enabled: bool = True
    iap_enforced: bool = True

@dataclass
class PlatformRegistry:
    shared_hub: SharedHubConfig = field(default_factory=SharedHubConfig)
    tenants: Dict[str, TenantConfig] = field(default_factory=lambda: {
        "tenant-finance-a": TenantConfig(
            tenant_id="tenant-finance-a",
            project_id="gcp-tenant-finance-a-prod",
            display_name="Tenant A (Global Finance & Treasury)",
            pab_boundary_id="pab-boundary-finance-001",
            datastore_type="BigQuery",
            allowed_roles=["roles/finance.analyst", "roles/finance.admin"]
        ),
        "tenant-healthcare-b": TenantConfig(
            tenant_id="tenant-healthcare-b",
            project_id="gcp-tenant-healthcare-b-prod",
            display_name="Tenant B (Clinical Health Informatics)",
            pab_boundary_id="pab-boundary-healthcare-002",
            datastore_type="AlloyDB",
            allowed_roles=["roles/healthcare.doctor", "roles/healthcare.clinical_researcher"]
        )
    })

registry = PlatformRegistry()
