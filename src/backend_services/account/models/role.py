import uuid

from sqlalchemy import Boolean, Column, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self, cast, TYPE_CHECKING

from account.models.association import role_permissions
from account.models.model_base import BaseModel
from account.common.enums import InteractionType

if TYPE_CHECKING:
    from account.models import PermissionModel


class RoleModel(BaseModel):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=False)

    permissions: Mapped[list["PermissionModel"]] = relationship(
        secondary=role_permissions, back_populates="roles"
    )

    def __init__(
        self: Self,
        id: uuid.UUID,
        name: str,
        description: str,
        type: InteractionType,
        category: str,
        removable: bool,
    ):
        self.id = cast(Column[uuid.UUID], id)
        self.name = cast(Column[str], name)
        self.description = cast(Column[str], description)
        self.type = cast(Column[InteractionType], type)
        self.category = cast(Column[str], category)
        self.removable = cast(Column[bool], removable)
