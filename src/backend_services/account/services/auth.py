from sqlalchemy.orm import Session
from typing import Self

from account.models import AccountModel
from account.services.base import BaseDBService


class AuthService(BaseDBService):
    def __init__(self, db: Session):
        super().__init__(db)

    @property
    def table(self):
        return AccountModel

    def is_email_used(self: Self, email: str):
        return (
            self.db.query(AccountModel)
            .filter(AccountModel.email == email)
            .one_or_none()
        )

    # TODO: Move registration code in here when more complex code is required
    def register(self: Self):
        pass

    # TODO: Move login code in here when more complex code and checks are required
    def login(self: Self):
        pass
