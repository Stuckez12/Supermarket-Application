import logging
import re

from argon2 import PasswordHasher
from email_validator import EmailNotValidError, validate_email
from sqlalchemy.types import Enum, String, TypeDecorator
from typing import Self

from utils.constants import EMAIL_CONFIG, PASSWORD_CONFIG
from utils.data_verification import DataVerification
from utils.database import GenderEnum
from utils.exceptions import UnableToFetchDataDBException


class EmailType(TypeDecorator):
    impl = String(96)

    def process_bind_param(self: Self, email: str, _):
        v = DataVerification(config={"string": EMAIL_CONFIG})

        v.verify_string(email)

        pattern = r"^(?!\.)(?!.*\.\.)[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$"

        if re.fullmatch(pattern, email) is None:
            logging.error("Attempted to insert malformed email into database")

            raise ValueError("Invalid email address")

        try:
            email_data = validate_email(email)

            validated_email = email_data.normalized

        except EmailNotValidError:
            logging.error("Attempted to insert invalid email into database")

            raise ValueError("Invalid email address")

        return validated_email

    def process_result_value(self: Self, email: str, _):
        return email


class PasswordType(TypeDecorator):
    impl = String(64)

    def process_bind_param(self: Self, password: str, _):
        v = DataVerification(config={"string": PASSWORD_CONFIG})

        v.verify_string(password)

        return PasswordHasher().hash(password)

    def process_result_value(self: Self, password: str, _):
        return password


class GenderType(TypeDecorator):
    impl = Enum(GenderEnum)

    def process_bind_param(self: Self, gender: GenderEnum, _):
        if type(gender) != GenderEnum:
            logging.error(
                "Gender value must be of type GenderEnum when passing to database"
            )

            raise ValueError("Invalid gender provided")

        return gender

    def process_result_value(self: Self, gender: str, _):
        try:
            return GenderEnum(gender)

        except:
            critical_messages = [
                "Invalid string format for gender enum is currently stored in the database",
                f"Acceptable enum strings: {[e.value for e in GenderEnum]}",
                f"String currently stored: {gender}",
            ]

            raise UnableToFetchDataDBException(critical_messages)
