import logging
import os

from alembic import command
from alembic.config import Config
from grpc import ServicerContext, StatusCode
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, DatabaseError, InterfaceError
from sqlalchemy_utils import create_database, database_exists
from typing import Callable, Self

from utils.database import db_connection, get_database_url, get_db
from utils.schemas import DatabaseSettings, DatabaseURL


class Initialise:
    def __init__(
        self: Self,
        database_url: DatabaseURL,
        database_settings: DatabaseSettings,
        grpc_context: ServicerContext | None = None,
    ):
        self.db_gen = get_db(db_connection(database_url, database_settings))

        self.db_url = get_database_url(database_url)
        self.db = next(self.db_gen)
        self.grpc_context = grpc_context

    def _raise_error(self: Self, error: str, error_type: StatusCode):
        print("error occurred here")
        if self.grpc_context is not None:
            self.grpc_context.abort(error_type, error)

            return None

        raise ValueError(error)

    def create_database_if_not_exists(self: Self):
        print("Does db exist")
        if not database_exists(self.db_url):
            print("it does not")
            if os.environ.get("PYTHON_ENV") == "testing":
                print("we creating")
                logging.info("Database does not exist. Creating new database")
                create_database(self.db_url)
                print("we done made it")

                print(f"URL: {self.db_url}")

            else:
                print("why not env correct")
                error_message = (
                    "Trying to access database that does not exist\n"
                    "Manually create database then restart server\n"
                    f"Database URL: {self.db_url}"
                )
                self._raise_error(error_message, error_type=StatusCode.NOT_FOUND)

        else:
            print("database exists ?????")
            logging.info("Database already exists")

    def check_database_connection(self: Self):
        try:
            self.db.execute(text("SELECT 1"))
            logging.info("Database reachable")
            print("reachable db")

        except (OperationalError, DatabaseError, InterfaceError):
            logging.error("Unable to connect to the database on startup")

            self._raise_error(
                "Unable to connect to database", error_type=StatusCode.UNAVAILABLE
            )

    def initialise_database(self: Self, ini_location: str, seed_db: Callable):
        if os.environ.get("PYTHON_ENV") != "testing":
            logging.info("Environment disallows seeding database")
            return None

        alembic_cfg = Config(ini_location)
        command.upgrade(alembic_cfg, "head")

        seed_db()

        logging.info("Database seeded")

    def wrap_up_initialisation(self: Self):
        self.db_gen.close()
