from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self, cast, TYPE_CHECKING

from account.models.association import permission_tags
from account.models.model_base import BaseModel

if TYPE_CHECKING:
    from account.models import PermissionModel


class PermissionTagsModel(BaseModel):
    __tablename__ = "perm_tags"

    name: Mapped[str] = mapped_column(String(64), nullable=False)

    tags: Mapped[list["PermissionModel"]] = relationship(
        secondary=permission_tags, back_populates="perm_tags"
    )

    def __init__(
        self: Self,
        name: str,
    ):
        self.name = cast(Column[str], name)
