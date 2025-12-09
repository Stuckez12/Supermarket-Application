import string

from datetime import datetime
from grpc import ServicerContext, StatusCode
from typing import Any, Self, cast

from utils.schemas import DateTimeConfig, NumberConfig, StringConfig, DataTypeConfig


class DataVerification:
    def __init__(
        self: Self,
        grpc_context: ServicerContext | None = None,
        config: dict[str, DataTypeConfig] | None = None,
    ):
        if config is None:
            config = {}

        self.grpc_context = grpc_context
        self.string = cast(StringConfig, config.get("string", StringConfig()))
        self.number = cast(NumberConfig, config.get("number", NumberConfig()))
        self.datetime = cast(DateTimeConfig, config.get("datetime", DateTimeConfig()))

    def _raise_error(
        self: Self, error: str, error_type: StatusCode = StatusCode.INTERNAL
    ):
        if self.grpc_context is not None:
            self.grpc_context.abort(error_type, error)

            return None

        raise ValueError(error)

    def verify_string(
        self: Self, param: Any, param_name: str, config: StringConfig | None = None
    ):
        string_conf = config or self.string

        if not isinstance(string_conf, StringConfig):
            err = "Invalid config provided. Expected StringConfig"

            self._raise_error(err, error_type=StatusCode.INVALID_ARGUMENT)

        if not isinstance(param, str):
            err = f"{param_name} is not of type string"

            self._raise_error(err, error_type=StatusCode.INVALID_ARGUMENT)

        if not len(param) >= string_conf.min_len:
            err = f"{param_name} must include a minimum of {string_conf.min_len} characters"

            self._raise_error(err, error_type=StatusCode.INVALID_ARGUMENT)

        if not len(param) <= string_conf.max_len:
            err = f"{param_name} must include a maximum of {string_conf.max_len} characters"

            self._raise_error(err, error_type=StatusCode.INVALID_ARGUMENT)

        lowercase = False
        uppercase = False
        numbers = False
        specials = False

        for char in param:
            lowercase = char.islower() if char.islower() else lowercase
            uppercase = char.isupper() if char.isupper() else uppercase
            numbers = char.isdigit() if char.isdigit() else numbers
            specials = True if char in string.punctuation else specials

        character_checks = [
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
                err = f"{param_name} must include {name}"

                self._raise_error(err, error_type=StatusCode.INVALID_ARGUMENT)

            if required is False and present:
                err = f"{param_name} must not include {name}"

                self._raise_error(err, error_type=StatusCode.INVALID_ARGUMENT)

    def verify_number(
        self: Self, param: Any, param_name: str, config: NumberConfig | None = None
    ):
        number_conf = config or self.number

        if not isinstance(number_conf, NumberConfig):
            err = f"Invalid config provided. Expected NumberConfig"

            self._raise_error(err, error_type=StatusCode.INVALID_ARGUMENT)

        if not isinstance(param, number_conf.number_type):
            err = f"{param_name} is not of type {number_conf.number_type.__name__}"

            self._raise_error(err, error_type=StatusCode.INVALID_ARGUMENT)

        if param < number_conf.min_val:
            err = f"{param_name} must be equal or larger than {number_conf.min_val}"

            self._raise_error(err, error_type=StatusCode.INVALID_ARGUMENT)

        if param > number_conf.max_val:
            err = f"{param_name} must be equal or smaller than {number_conf.max_val}"

            self._raise_error(err, error_type=StatusCode.INVALID_ARGUMENT)

    def verify_datetime(
        self: Self,
        param: Any,
        param_name: str,
        config: DateTimeConfig | None = None,
    ):
        datetime_conf = config or self.datetime

        if not isinstance(datetime_conf, DateTimeConfig):
            err = f"Invalid config provided. Expected DateTimeConfig"

            self._raise_error(err, error_type=StatusCode.INVALID_ARGUMENT)

        if not isinstance(param, datetime):
            err = f"{param_name} is not of type datetime"

            self._raise_error(err, error_type=StatusCode.INVALID_ARGUMENT)

        if param < datetime_conf.min_datetime:
            err = f"{param_name} must be larger than {datetime_conf.min_datetime}: {param}"

            self._raise_error(err, error_type=StatusCode.INVALID_ARGUMENT)

        if param > datetime_conf.max_datetime:
            err = f"{param_name} must be smaller than {datetime_conf.max_datetime}"

            self._raise_error(err, error_type=StatusCode.INVALID_ARGUMENT)
