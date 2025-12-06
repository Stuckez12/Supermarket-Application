import pytest

from datetime import datetime, timedelta
from typing import Any

from utils.data_verification import DataVerification
from utils.enums import TriBool
from utils.schemas import DateTimeConfig, NumberConfig, StringConfig


STRING_CONF_MIN_LEN = StringConfig().min_len
STRING_CONF_MIN_LEN_ERROR = StringConfig().min_len - 1
STRING_CONF_MAX_LEN = StringConfig().max_len
STRING_CONF_MAX_LEN_ERROR = StringConfig().max_len + 1

NUMBER_CONF_MIN_VAL = NumberConfig().min_val
NUMBER_CONF_MIN_VAL_ERROR = NumberConfig().min_val - 1
NUMBER_CONF_MAX_VAL = NumberConfig().max_val
NUMBER_CONF_MAX_VAL_ERROR = NumberConfig().max_val + 1


class TestDataVerification:
    @pytest.mark.parametrize(
        ("param"),
        [
            ("string"),
            ("String"),
            ("string1"),
            ("String1"),
            ("a" * STRING_CONF_MIN_LEN),
            ("a" * STRING_CONF_MAX_LEN),
        ],
    )
    def test_verify_string_default_success(
        self, test_data_verify: DataVerification, param: Any
    ):
        assert (
            test_data_verify.verify_string(
                param=param, param_name="Test_Data", config=None
            )
            is None
        )

    @pytest.mark.parametrize(
        ("param", "exception", "error_message"),
        [
            (1, ValueError, "Test_Data is not of type string"),
            ("STRING", ValueError, "Test_Data must include lowercase characters"),
            ("111111", ValueError, "Test_Data must include lowercase characters"),
            ("STR111", ValueError, "Test_Data must include lowercase characters"),
            ("!!!!!!", ValueError, "Test_Data must include lowercase characters"),
            ("string!", ValueError, "Test_Data must not include special characters"),
            (
                "a" * STRING_CONF_MIN_LEN_ERROR,
                ValueError,
                f"Test_Data must include a minimum of {STRING_CONF_MIN_LEN} characters",
            ),
            (
                "a" * STRING_CONF_MAX_LEN_ERROR,
                ValueError,
                f"Test_Data must include a maximum of {STRING_CONF_MAX_LEN} characters",
            ),
        ],
    )
    def test_verify_string_default_error(
        self,
        test_data_verify: DataVerification,
        param: Any,
        exception: BaseException,
        error_message: str,
    ):
        with pytest.raises(exception, match=error_message):
            test_data_verify.verify_string(
                param=param, param_name="Test_Data", config=None
            )

    @pytest.mark.parametrize(
        ("param", "config"),
        [
            ("string", {"min_len": 6}),
            ("string", {"max_len": 6}),
            ("string", {"include_lowercase": TriBool.NONE}),
            ("s123NG", {"include_lowercase": TriBool.NONE}),
            ("STRING", {"include_lowercase": TriBool.FALSE}),
            (
                "string",
                {
                    "include_lowercase": TriBool.TRUE,
                    "include_uppercase": TriBool.FALSE,
                    "include_number": TriBool.FALSE,
                    "include_specials": TriBool.FALSE,
                },
            ),
        ],
    )
    def test_verify_string_custom_success(self, param: Any, config: dict):
        verify = DataVerification(config={"string": StringConfig(**config)})

        assert (
            verify.verify_string(param=param, param_name="Test_Data", config=None)
            is None
        )

    @pytest.mark.parametrize(
        ("param", "config", "exception", "error_message"),
        [
            (1, {}, ValueError, "Test_Data is not of type string"),
            (
                "string",
                {"min_len": 7},
                ValueError,
                "Test_Data must include a minimum of 7 characters",
            ),
            (
                "string",
                {"max_len": 5},
                ValueError,
                "Test_Data must include a maximum of 5 characters",
            ),
            (
                "string",
                {"include_lowercase": TriBool.FALSE},
                ValueError,
                "Test_Data must not include lowercase characters",
            ),
            (
                "s123NG",
                {"include_uppercase": TriBool.FALSE},
                ValueError,
                "Test_Data must not include uppercase characters",
            ),
            (
                "s123NG",
                {"include_number": TriBool.FALSE},
                ValueError,
                "Test_Data must not include numbers",
            ),
            (
                "!!!!!!",
                {"include_lowercase": TriBool.NONE, "include_specials": TriBool.FALSE},
                ValueError,
                "Test_Data must not include special characters",
            ),
        ],
    )
    def test_verify_string_custom_error(
        self,
        param: Any,
        config: dict,
        exception: BaseException,
        error_message: str,
    ):
        verify = DataVerification(config={"string": StringConfig(**config)})

        with pytest.raises(exception, match=error_message):
            verify.verify_string(param=param, param_name="Test_Data", config=None)

    @pytest.mark.parametrize(
        ("param", "config"),
        [
            ("string", {"min_len": 6}),
            ("string", {"max_len": 6}),
            ("string", {"include_lowercase": TriBool.NONE}),
            ("s123NG", {"include_lowercase": TriBool.NONE}),
            ("STRING", {"include_lowercase": TriBool.FALSE}),
            (
                "string",
                {
                    "include_lowercase": TriBool.TRUE,
                    "include_uppercase": TriBool.FALSE,
                    "include_number": TriBool.FALSE,
                    "include_specials": TriBool.FALSE,
                },
            ),
        ],
    )
    def test_verify_string_custom_insert_success(
        self, test_data_verify: DataVerification, param: Any, config: dict
    ):
        assert (
            test_data_verify.verify_string(
                param=param, param_name="Test_Data", config=StringConfig(**config)
            )
            is None
        )

    @pytest.mark.parametrize(
        ("param", "config", "exception", "error_message"),
        [
            (1, {}, ValueError, "Test_Data is not of type string"),
            (
                "string",
                {"min_len": 7},
                ValueError,
                "Test_Data must include a minimum of 7 characters",
            ),
            (
                "string",
                {"max_len": 5},
                ValueError,
                "Test_Data must include a maximum of 5 characters",
            ),
            (
                "string",
                {"include_lowercase": TriBool.FALSE},
                ValueError,
                "Test_Data must not include lowercase characters",
            ),
            (
                "s123NG",
                {"include_uppercase": TriBool.FALSE},
                ValueError,
                "Test_Data must not include uppercase characters",
            ),
            (
                "s123NG",
                {"include_number": TriBool.FALSE},
                ValueError,
                "Test_Data must not include numbers",
            ),
            (
                "!!!!!!",
                {"include_lowercase": TriBool.NONE, "include_specials": TriBool.FALSE},
                ValueError,
                "Test_Data must not include special characters",
            ),
        ],
    )
    def test_verify_string_custom_insert_error(
        self,
        test_data_verify: DataVerification,
        param: Any,
        config: dict,
        exception: BaseException,
        error_message: str,
    ):
        with pytest.raises(exception, match=error_message):
            test_data_verify.verify_string(
                param=param, param_name="Test_Data", config=StringConfig(**config)
            )

    @pytest.mark.parametrize(
        ("param"),
        [(NUMBER_CONF_MIN_VAL), (50), (NUMBER_CONF_MAX_VAL)],
    )
    def test_verify_number_default_success(
        self, test_data_verify: DataVerification, param: Any
    ):
        assert (
            test_data_verify.verify_number(
                param=param, param_name="Test_Data", config=None
            )
            is None
        )

    @pytest.mark.parametrize(
        ("param", "exception", "error_message"),
        [
            ("0", ValueError, "Test_Data is not of type int"),
            (
                NUMBER_CONF_MIN_VAL_ERROR,
                ValueError,
                f"Test_Data must be equal or larger than {NUMBER_CONF_MIN_VAL}",
            ),
            (
                NUMBER_CONF_MAX_VAL_ERROR,
                ValueError,
                f"Test_Data must be equal or smaller than {NUMBER_CONF_MAX_VAL}",
            ),
        ],
    )
    def test_verify_number_default_error(
        self,
        test_data_verify: DataVerification,
        param: Any,
        exception: BaseException,
        error_message: str,
    ):
        with pytest.raises(exception, match=error_message):
            test_data_verify.verify_number(
                param=param, param_name="Test_Data", config=None
            )

    @pytest.mark.parametrize(
        ("param", "config"),
        [
            (20, {"number_type": int}),
            (20.0, {"number_type": float}),
            (16.5, {"number_type": float}),
            (20, {"min_val": 20}),
            (20, {"max_val": 20}),
            (15.5, {"number_type": float, "min_val": 15.5}),
            (15.5, {"number_type": float, "max_val": 15.5}),
        ],
    )
    def test_verify_number_custom_success(self, param: Any, config: dict):
        verify = DataVerification(config={"number": NumberConfig(**config)})

        assert (
            verify.verify_number(param=param, param_name="Test_Data", config=None)
            is None
        )

    @pytest.mark.parametrize(
        ("param", "config", "exception", "error_message"),
        [
            (
                "1",
                {"number_type": int, "min_val": 20},
                ValueError,
                "Test_Data is not of type int",
            ),
            (
                "1",
                {"number_type": float, "min_val": 20},
                ValueError,
                "Test_Data is not of type float",
            ),
            (
                1,
                {"number_type": int, "min_val": 20},
                ValueError,
                "Test_Data must be equal or larger than 20",
            ),
            (
                1,
                {"number_type": int, "max_val": -20},
                ValueError,
                "Test_Data must be equal or smaller than -20",
            ),
            (
                1.0,
                {"number_type": float, "min_val": 20.5},
                ValueError,
                "Test_Data must be equal or larger than 20.5",
            ),
            (
                1.0,
                {"number_type": float, "max_val": -20.5},
                ValueError,
                "Test_Data must be equal or smaller than -20.5",
            ),
        ],
    )
    def test_verify_number_custom_error(
        self,
        param: Any,
        config: dict,
        exception: BaseException,
        error_message: str,
    ):
        verify = DataVerification(config={"number": NumberConfig(**config)})

        with pytest.raises(exception, match=error_message):
            verify.verify_number(param=param, param_name="Test_Data", config=None)

    @pytest.mark.parametrize(
        ("param", "config"),
        [
            (20, {"number_type": int}),
            (20.0, {"number_type": float}),
            (16.5, {"number_type": float}),
            (20, {"min_val": 20}),
            (20, {"max_val": 20}),
            (15.5, {"number_type": float, "min_val": 15.5}),
            (15.5, {"number_type": float, "max_val": 15.5}),
        ],
    )
    def test_verify_number_custom_insert_success(
        self, test_data_verify: DataVerification, param: Any, config: dict
    ):
        assert (
            test_data_verify.verify_number(
                param=param, param_name="Test_Data", config=NumberConfig(**config)
            )
            is None
        )

    @pytest.mark.parametrize(
        ("param", "config", "exception", "error_message"),
        [
            (
                "1",
                {"number_type": int, "min_val": 20},
                ValueError,
                "Test_Data is not of type int",
            ),
            (
                "1",
                {"number_type": float, "min_val": 20},
                ValueError,
                "Test_Data is not of type float",
            ),
            (
                1,
                {"number_type": int, "min_val": 20},
                ValueError,
                "Test_Data must be equal or larger than 20",
            ),
            (
                1,
                {"number_type": int, "max_val": -20},
                ValueError,
                "Test_Data must be equal or smaller than -20",
            ),
            (
                1.0,
                {"number_type": float, "min_val": 20.5},
                ValueError,
                "Test_Data must be equal or larger than 20.5",
            ),
            (
                1.0,
                {"number_type": float, "max_val": -20.5},
                ValueError,
                "Test_Data must be equal or smaller than -20.5",
            ),
        ],
    )
    def test_verify_number_custom_insert_error(
        self,
        test_data_verify: DataVerification,
        param: Any,
        config: dict,
        exception: BaseException,
        error_message: str,
    ):
        with pytest.raises(exception, match=error_message):
            test_data_verify.verify_number(
                param=param, param_name="Test_Data", config=NumberConfig(**config)
            )

    @pytest.mark.parametrize(
        ("param", "config"),
        [
            (
                datetime.now(),
                {"min_datetime": datetime.now() - timedelta(milliseconds=10)},
            ),
            (
                datetime.now() + timedelta(milliseconds=200),
                {
                    "min_datetime": datetime.now() - timedelta(milliseconds=10),
                    "max_datetime": datetime.now() + timedelta(milliseconds=400),
                },
            ),
            (
                datetime.now(),
                {
                    "min_datetime": datetime.now() - timedelta(milliseconds=10),
                    "max_datetime": datetime.now() + timedelta(milliseconds=10),
                },
            ),
        ],
    )
    def test_verify_datetime_custom_success(self, param: Any, config: dict):
        verify = DataVerification(config={"datetime": DateTimeConfig(**config)})

        assert (
            verify.verify_datetime(param=param, param_name="Test_Data", config=None)
            is None
        )

    @pytest.mark.parametrize(
        ("param", "config", "exception", "error_message"),
        [
            (1, {}, ValueError, "Test_Data is not of type datetime"),
            (
                datetime.now(),
                {"min_datetime": datetime.now() + timedelta(milliseconds=10)},
                ValueError,
                r"Test_Data must be larger than *",
            ),
            (
                datetime.now(),
                {
                    "min_datetime": datetime.now() - timedelta(weeks=1),
                    "max_datetime": datetime.now() - timedelta(milliseconds=10),
                },
                ValueError,
                r"Test_Data must be smaller than *",
            ),
        ],
    )
    def test_verify_datetime_custom_error(
        self,
        param: Any,
        config: dict,
        exception: BaseException,
        error_message: str,
    ):
        verify = DataVerification(config={"datetime": DateTimeConfig(**config)})

        with pytest.raises(exception, match=error_message):
            verify.verify_datetime(param=param, param_name="Test_Data", config=None)

    @pytest.mark.parametrize(
        ("param", "config"),
        [
            (
                datetime.now(),
                {"min_datetime": datetime.now() - timedelta(milliseconds=10)},
            ),
            (
                datetime.now() + timedelta(milliseconds=200),
                {
                    "min_datetime": datetime.now() - timedelta(milliseconds=10),
                    "max_datetime": datetime.now() + timedelta(milliseconds=400),
                },
            ),
            (
                datetime.now(),
                {
                    "min_datetime": datetime.now() - timedelta(milliseconds=10),
                    "max_datetime": datetime.now() + timedelta(milliseconds=10),
                },
            ),
        ],
    )
    def test_verify_datetime_custom_insert_success(
        self, test_data_verify: DataVerification, param: Any, config: dict
    ):
        assert (
            test_data_verify.verify_datetime(
                param=param, param_name="Test_Data", config=DateTimeConfig(**config)
            )
            is None
        )

    @pytest.mark.parametrize(
        ("param", "config", "exception", "error_message"),
        [
            (1, {}, ValueError, "Test_Data is not of type datetime"),
            (
                datetime.now(),
                {"min_datetime": datetime.now() + timedelta(milliseconds=10)},
                ValueError,
                r"Test_Data must be larger than *",
            ),
            (
                datetime.now(),
                {
                    "min_datetime": datetime.now() - timedelta(weeks=1),
                    "max_datetime": datetime.now() - timedelta(milliseconds=10),
                },
                ValueError,
                r"Test_Data must be smaller than *",
            ),
        ],
    )
    def test_verify_datetime_custom_insert_error(
        self,
        test_data_verify: DataVerification,
        param: Any,
        config: dict,
        exception: BaseException,
        error_message: str,
    ):
        with pytest.raises(exception, match=error_message):
            test_data_verify.verify_datetime(
                param=param, param_name="Test_Data", config=DateTimeConfig(**config)
            )
