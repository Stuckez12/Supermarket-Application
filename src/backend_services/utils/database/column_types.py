import logging
import re

from email_validator import EmailNotValidError, validate_email
from sqlalchemy.types import String, TypeDecorator


class EmailType(TypeDecorator):
    impl = String(96)

    def process_bind_param(self, email, _):
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

    def process_result_value(self, email, _):
        return email


class PasswordType(TypeDecorator):
    impl = String(64)

    def process_bind_param(self, password, _):
        return password

    def process_result_value(self, password, _):
        return password
