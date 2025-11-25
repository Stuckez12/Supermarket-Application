from sqlalchemy import Column

from utils.database import BaseModel
from utils.database.column_types import EmailType, PasswordType


class Account(BaseModel):
    __tablename__ = "accounts"

    email = Column(EmailType, nullable=False, unique=True)
    password = Column(PasswordType, nullable=False, unique=True)
