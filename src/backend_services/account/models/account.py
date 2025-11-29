import uuid

from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, Date, DateTime, Enum, Integer, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self, cast, TYPE_CHECKING

from account.models.association import account_removed_permissions
from account.models.model_base import BaseModel

from utils.enums import AccountStatusEnum, GenderEnum
from utils.database.column_types import EmailType, GenderType, PasswordType
from utils.utils import get_current_time

if TYPE_CHECKING:
    from account.models import PermissionModel, RoleModel


class AccountModel(BaseModel):
    __tablename__ = "accounts"

    email: Mapped[str] = mapped_column(EmailType, nullable=False, unique=True)

    password: Mapped[str] = mapped_column(PasswordType, nullable=False, unique=True)
    password_last_changed_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc), nullable=False
    )
    failed_login_attempts: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )
    account_locked_until: Mapped[datetime] = mapped_column(
        Integer, default=0, nullable=True
    )
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    master_user: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    date_of_birth: Mapped[datetime] = mapped_column(Date, nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(GenderType, nullable=False)

    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    user_status: Mapped[AccountStatusEnum] = mapped_column(
        Enum(AccountStatusEnum), default=AccountStatusEnum.UNVERIFIED, nullable=False
    )

    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, unique=True
    )

    roles: Mapped[list["RoleModel"]] = relationship(back_populates="accounts")
    removed_permissions: Mapped[list["PermissionModel"]] = relationship(
        secondary=account_removed_permissions, back_populates="accounts"
    )

    def __init__(
        self: Self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        date_of_birth: datetime,
        gender: str,
        email_verified: bool,
        user_status: AccountStatusEnum,
        role_id: uuid.UUID,
        password_last_changed_at: datetime | None = None,
        failed_login_attempts: int = 0,
        account_locked_until: datetime | None = None,
        last_login: datetime | None = None,
        master_user: bool = False,
    ):
        now = get_current_time()

        self.email = cast(Column[str], email)
        self.password = cast(Column[str], password)
        self.password_last_changed_at = cast(
            Column[datetime], password_last_changed_at or now
        )
        self.failed_login_attempts = cast(Column[int], failed_login_attempts)
        self.account_locked_until = cast(Column[datetime], account_locked_until or now)
        self.last_login = cast(Column[datetime], last_login or now)
        self.master_user = cast(Column[bool], master_user)
        self.first_name = cast(Column[str], first_name)
        self.last_name = cast(Column[str], last_name)
        self.date_of_birth = cast(Column[datetime], date_of_birth)
        self.gender = cast(Column[GenderEnum], gender)
        self.email_verified = cast(Column[bool], email_verified)
        self.user_status = cast(Column[AccountStatusEnum], user_status)
        self.role_id = cast(Column[uuid.UUID], role_id)
