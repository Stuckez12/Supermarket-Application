import uuid

from sqlalchemy import Boolean, Column, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self, cast, TYPE_CHECKING

from account.models.association import (
    account_removed_permissions,
    permission_tags,
    role_permissions,
)
from account.models.model_base import BaseModel
from account.common.enums import InteractionType

if TYPE_CHECKING:
    from account.models import AccountModel, PermissionTagsModel, RoleModel


class PermissionModel(BaseModel):
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=False)
    type: Mapped[InteractionType] = mapped_column(Enum(InteractionType), nullable=False)
    category: Mapped[str] = mapped_column(String(32), nullable=False)
    removable: Mapped[bool] = mapped_column(Boolean, nullable=False)

    accounts: Mapped[list["AccountModel"]] = relationship(
        secondary=account_removed_permissions, back_populates="removed_permissions"
    )
    perm_tags: Mapped[list["PermissionTagsModel"]] = relationship(
        secondary=permission_tags, back_populates="permissions"
    )
    roles: Mapped[list["RoleModel"]] = relationship(
        secondary=role_permissions, back_populates="permissions"
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
