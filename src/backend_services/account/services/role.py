from sqlalchemy.orm import Session
from typing import Self

from account.models import RoleModel
from account.services.base import BaseDBService


class RoleService(BaseDBService):
    def __init__(self, db: Session):
        super().__init__(db)

    @property
    def table(self):
        return RoleModel

    def get_by_name(self: Self, name: str):
        return self.db.query(self.table).filter(self.table.name == name).first()
