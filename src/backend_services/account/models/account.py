from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, Date, DateTime, Enum, Integer, String

from account.models.model_base import BaseModel

from utils.database.column_enums import AccountRoleEnum, AccountStatusEnum
from utils.database.column_types import EmailType, GenderType, PasswordType


class AccountModel(BaseModel):
    __tablename__ = "accounts"

    email = Column(EmailType, nullable=False, unique=True)

    password = Column(PasswordType, nullable=False, unique=True)
    password_last_changed_at = Column(
        DateTime, default=datetime.now(timezone.utc), nullable=False
    )
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    account_locked_until = Column(Integer, default=0, nullable=True)
    last_login = Column(DateTime, nullable=True)

    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(GenderType, nullable=False)

    email_verified = Column(Boolean, default=False, nullable=False)
    user_status = Column(
        Enum(AccountStatusEnum), default=AccountStatusEnum.UNVERIFIED, nullable=False
    )
    user_role = Column(
        Enum(AccountRoleEnum), default=AccountRoleEnum.CUSTOMER, nullable=False
    )
