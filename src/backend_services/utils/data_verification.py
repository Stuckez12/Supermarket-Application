import string as string_lib

from datetime import datetime
from typing import Any, Self, Union

from utils.schemas import DateTimeConfig, NumberConfig, StringConfig, DataTypeConfig


class DataVerification:
    def __init__(self: Self, config: dict[str, DataTypeConfig]):
        self.string = config.get("string", StringConfig())
        self.number = config.get("number", NumberConfig())
        self.datetime = config.get("datetime", DateTimeConfig())

    def verify_string(
        self: Self, string: Any, param_name: str, config: StringConfig | None = None
    ):
        string_conf: StringConfig = config or self.string

        if not isinstance(string, str):
            raise ValueError(f"{param_name} is not of type string")

        if not len(string) >= string_conf.min_len:
            raise ValueError(
                f"{param_name} must include a minimum of {string_conf.min_len} characters"
            )

        if not len(string) <= string_conf.max_len:
            raise ValueError(
                f"{param_name} must include a maximum of {string_conf.max_len} characters"
            )

        lowercase, uppercase, numbers, specials = False

        for char in string:
            lowercase = char.islower() if char.islower() else lowercase
            uppercase = char.isupper() if char.isupper() else uppercase
            numbers = char.isdigit() if char.isdigit() else numbers
            specials = True if char in string_lib.punctuation else specials

        character_checks: tuple[bool, Union[bool, None], str] = [
            (
                lowercase,
                string_conf.include_lowercase.value,
                "lowercase characters",
            ),
            (
                uppercase,
                string_conf.include_uppercase.value,
                "uppercase characters",
            ),
            (numbers, string_conf.include_number.value, "numbers"),
            (specials, string_conf.include_specials.value, "special characters"),
        ]

        for present, required, name in character_checks:
            if required is True and not present:
                raise ValueError(f"{param_name} must include {name}")

            if required is False and present:
                raise ValueError(f"{param_name} must not include {name}")

    def verify_number(
        self: Self, number: Any, param_name: str, config: NumberConfig | None = None
    ):
        number_conf: NumberConfig = config or self.number

        if not isinstance(number, number_conf.number_type):
            raise ValueError(f"{param_name} is not of type {number_conf.number_type}")

        if not len(number) >= number_conf.min_len:
            raise ValueError(
                f"{param_name} must be larger than {number_conf.min_val - 1}"
            )

        if not len(number) <= number_conf.max_len:
            raise ValueError(
                f"{param_name} must be smaller than {number_conf.max_val + 1}"
            )

    def verify_datetime(
        self: Self,
        date_time: Any,
        param_name: str,
        config: DateTimeConfig | None = None,
    ):
        datetime_conf: DateTimeConfig = config or self.datetime

        if not isinstance(date_time, datetime):
            raise ValueError(f"{param_name} is not of type datetime")

        if date_time < datetime_conf.min_datetime:
            raise ValueError(
                f"{param_name} must be larger than {datetime_conf.min_datetime}"
            )

        if date_time > datetime_conf.max_datetime:
            raise ValueError(
                f"{param_name} must be smaller than {datetime_conf.max_datetime}"
            )
