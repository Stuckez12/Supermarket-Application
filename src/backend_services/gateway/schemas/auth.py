from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, field_validator
from uuid import UUID

from utils.constants import (
    EMAIL_CONFIG,
    FIRST_NAME_CONFIG,
    LAST_NAME_CONFIG,
    PASSWORD_CONFIG,
)
from utils.data_verification import DataVerification
from utils.enums.enums import AccountStatusEnum, GenderEnum


class MinimumAccountData(BaseModel):
    id: UUID
    role_id: UUID
    first_name: str
    last_name: str
    verified: bool
    master_user: bool = False
    user_status: AccountStatusEnum


class AccountLogin(BaseModel):
    email: str
    password: str

    @field_validator("email")
    def validate_email(param: str):  # type: ignore[misc]
        DataVerification().verify_string(param, param_name="Email", config=EMAIL_CONFIG)

        return param

    @field_validator("password")
    def validate_password(param: str):  # type: ignore[misc]
        DataVerification().verify_string(
            param, param_name="Password", config=PASSWORD_CONFIG
        )

        return param


class AccountRegistration(AccountLogin):
    first_name: str
    last_name: str
    date_of_birth: datetime
    gender: GenderEnum

    @field_validator("first_name")
    def validate_first_name(param: str):  # type: ignore[misc]
        DataVerification().verify_string(
            param, param_name="First name", config=FIRST_NAME_CONFIG
        )

        return param

    @field_validator("last_name")
    def validate_last_name(param: str):  # type: ignore[misc]
        DataVerification().verify_string(
            param, param_name="Last name", config=LAST_NAME_CONFIG
        )

        return param

    @field_validator("date_of_birth")
    def validate_date_of_birth(param: datetime):  # type: ignore[misc]
        minimum = datetime.now(timezone.utc) - relativedelta(years=13)
        maximum = datetime.now(timezone.utc) - relativedelta(years=120)

        if minimum < param:
            raise ValueError("You must be 13 years or older to register")

        if maximum > param:
            raise ValueError("Invalid age set")

        return param
