import os

from pydantic_settings import BaseSettings
from typing import Type


class DevelopmentSettings(BaseSettings):
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> BaseSettings:
    environment = os.getenv("PYTHON_ENV", "development")

    all_envs: dict[str, Type[BaseSettings]] = {"development": DevelopmentSettings}

    return all_envs[environment]()


settings = get_settings()
