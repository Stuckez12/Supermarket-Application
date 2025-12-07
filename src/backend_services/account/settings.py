import logging
import os

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings
from typing import Type

from utils.schemas import DatabaseURL


class DevelopmentSettings(BaseSettings):
    SERVER_HOST: str = Field(..., validation_alias="ACCOUNT_SERVICE_HOST")
    SERVER_PORT: int = Field(..., validation_alias="ACCOUNT_SERVICE_PORT")
    SERVER_MAX_WORKERS: int = Field(..., validation_alias="ACCOUNT_SERVICE_MAX_WORKERS")

    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int

    def get_db_url(self):
        return DatabaseURL(
            username=self.DATABASE_USERNAME,
            password=self.DATABASE_PASSWORD,
            host=self.DATABASE_HOST,
            port=self.DATABASE_PORT,
            db_name="NONE",
        )

    PGADMIN_EMAIL: str
    PGADMIN_PASSWORD: str

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        frozen=False,
        populate_by_name=False,
        validate_default=True,
    )


class TestSettings(BaseSettings):
    SERVER_HOST: str = Field(..., validation_alias="ACCOUNT_SERVICE_HOST")
    SERVER_PORT: int = Field(..., validation_alias="ACCOUNT_SERVICE_PORT")
    SERVER_MAX_WORKERS: int = Field(..., validation_alias="ACCOUNT_SERVICE_MAX_WORKERS")

    DATABASE_USERNAME: str | None = None
    DATABASE_PASSWORD: str | None = None
    DATABASE_HOST: str | None = None
    DATABASE_PORT: int | None = None

    def get_db_url(self):
        return DatabaseURL(
            username=self.TEST_DATABASE_USERNAME,
            password=self.TEST_DATABASE_PASSWORD,
            host=self.TEST_DATABASE_HOST,
            port=self.TEST_DATABASE_PORT,
            db_name="NONE",
        )

    TEST_DATABASE_USERNAME: str
    TEST_DATABASE_PASSWORD: str
    TEST_DATABASE_HOST: str
    TEST_DATABASE_PORT: int

    model_config = ConfigDict(
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

    all_envs: dict[str, Type[BaseSettings]] = {
        "development": DevelopmentSettings,
        "testing": TestSettings,
    }

    return all_envs.get(environment)()


settings = get_settings()
