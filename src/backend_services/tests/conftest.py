import pytest

from utils.data_verification import DataVerification


@pytest.fixture(scope="function")
def test_data_verify():
    yield DataVerification()
