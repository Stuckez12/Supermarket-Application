from sqlalchemy import Column, ForeignKey, Table, UUID

from account.models.model_base import Base


role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("permission_id", UUID, ForeignKey("permissions.id"), primary_key=True),
    Column("role_id", UUID, ForeignKey("roles.id"), primary_key=True),
)
