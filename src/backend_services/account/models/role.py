from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self, cast, TYPE_CHECKING

from account.models.association import role_permissions
from account.models.model_base import BaseModel

if TYPE_CHECKING:
    from account.models import AccountModel, PermissionModel


class RoleModel(BaseModel):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=False)

    accounts: Mapped[list["AccountModel"]] = relationship(back_populates="roles")
    permissions: Mapped[list["PermissionModel"]] = relationship(
        secondary=role_permissions, back_populates="roles"
    )

    def __init__(
        self: Self,
        name: str,
        description: str,
    ):
        self.name = cast(Column[str], name)
        self.description = cast(Column[str], description)
