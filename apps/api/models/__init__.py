"""ORM models and status enums.

Importing this package registers every table on ``Base.metadata`` so foreign
keys (for example ``TenantOwned.organization_id``) always resolve.
"""

from .phase1 import (
    INTERNAL_ORGANIZATION_ID,
    INTERNAL_ORGANIZATION_NAME,
    AuditLog,
    ConsentRecord,
    Lead,
    Organization,
    Project,
    ProjectInquiry,
)

__all__ = [
    "INTERNAL_ORGANIZATION_ID",
    "INTERNAL_ORGANIZATION_NAME",
    "AuditLog",
    "ConsentRecord",
    "Lead",
    "Organization",
    "Project",
    "ProjectInquiry",
]
