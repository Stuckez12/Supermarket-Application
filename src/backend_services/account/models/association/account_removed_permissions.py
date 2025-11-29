from sqlalchemy import Column, ForeignKey, Table, UUID

from account.models.model_base import Base


account_removed_permissions = Table(
    "account_removed_permissions",
    Base.metadata,
    Column("permission_id", UUID, ForeignKey("permissions.id"), primary_key=True),
    Column("account_id", UUID, ForeignKey("accounts.id"), primary_key=True),
)
