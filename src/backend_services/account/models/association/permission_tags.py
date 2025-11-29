from sqlalchemy import Column, ForeignKey, Table, UUID

from account.models.model_base import Base


permission_tags = Table(
    "permission_tags",
    Base.metadata,
    Column("permission_id", UUID, ForeignKey("permissions.id"), primary_key=True),
    Column("tag_id", UUID, ForeignKey("perm_tags.id"), primary_key=True),
)
