import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Type


class DevelopmentSettings(BaseSettings):
    SERVER_HOST: str = Field(..., validation_alias="API_SERVICE_HOST")
    SERVER_PORT: int = Field(..., validation_alias="API_SERVICE_PORT")


class TestSettings(BaseSettings):
    SERVER_HOST: str = Field(..., validation_alias="API_SERVICE_HOST")
    SERVER_PORT: int = Field(..., validation_alias="API_SERVICE_PORT")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        frozen=True,
        populate_by_name=False,
        validate_default=True,
    )


SETTING_TYPE = DevelopmentSettings | TestSettings


def get_settings() -> SETTING_TYPE:
    environment = os.getenv("PYTHON_ENV", "development")

    all_envs: dict[str, Type[SETTING_TYPE]] = {
        "development": DevelopmentSettings,
        "testing": TestSettings,
    }

    settings = all_envs.get(environment)

    if settings is None:
        raise SystemError(
            "PYTHON_ENV environment param has invalid value."
            f"Expected one of the following: {[env for env in all_envs.keys()]}"
            f"Received this invalid value instead: {environment}"
        )

    return settings()  # type: ignore[call-arg]


settings = get_settings()

IS_DEVELOPMENT_ENV = isinstance(settings, DevelopmentSettings)
IS_TESTING_ENV = isinstance(settings, TestSettings)
