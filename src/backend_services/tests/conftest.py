import os
import pytest

from utils.data_verification import DataVerification


@pytest.fixture(autouse=True, scope="session")
def check_testing_environment():
    assert os.environ.get("PYTHON_ENV") == "testing"


@pytest.fixture(scope="function")
def test_data_verify():
    yield DataVerification()
