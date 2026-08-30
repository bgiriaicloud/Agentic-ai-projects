"""
Principal Access Boundary (PAB) Enforcement Module.
Ensures strict tenant project boundary isolation and blocks cross-tenant data leakage.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from ..config import registry

@dataclass
class PABValidationResult:
    allowed: bool
    step: int
    source_origin: str
    target_project_id: str
    pab_boundary_id: str
    reason: Optional[str] = None

class PABBoundaryEnforcer:
    """
    Validates that incoming tenant requests and outgoing tool invocations adhere to
    the project's Principal Access Boundary (PAB).
    """
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.tenant_config = registry.tenants.get(tenant_id)

    def validate_tenant_ingress(self, caller_tenant_id: str) -> PABValidationResult:
        """
        Step 3: Route request to tenant across PAB.
        Blocks cross-tenant requests if caller tenant does not match destination project.
        """
        if not self.tenant_config:
            return PABValidationResult(
                allowed=False,
                step=3,
                source_origin=caller_tenant_id,
                target_project_id="UNKNOWN",
                pab_boundary_id="UNKNOWN",
                reason=f"Unknown tenant identifier '{self.tenant_id}'."
            )

        if caller_tenant_id != self.tenant_id:
            return PABValidationResult(
                allowed=False,
                step=3,
                source_origin=caller_tenant_id,
                target_project_id=self.tenant_config.project_id,
                pab_boundary_id=self.tenant_config.pab_boundary_id,
                reason=f"PAB Violation: Request from '{caller_tenant_id}' rejected by '{self.tenant_config.display_name}' PAB boundary."
            )

        return PABValidationResult(
            allowed=True,
            step=3,
            source_origin=caller_tenant_id,
            target_project_id=self.tenant_config.project_id,
            pab_boundary_id=self.tenant_config.pab_boundary_id
        )
