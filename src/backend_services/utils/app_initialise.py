import logging

from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, DatabaseError, InterfaceError
from typing import Self

from utils.database import db_connection, get_db
from utils.schemas import DatabaseSettings, DatabaseURL


class Initialise:
    def __init__(self, url_obj: DatabaseURL, db_settings: DatabaseSettings):
        self.db_factory = lambda: get_db(db_connection(url_obj, db_settings))

    def check_database_connection(self: Self):
        with self.db_factory() as db:
            try:
                db.execute(text("SELECT 1"))

            except (OperationalError, DatabaseError, InterfaceError):
                logging.error("Unable to connect to the database on startup")

                raise ConnectionError("Unable to connect to database")

    def database(self: Self, ini_location: str):
        alembic_cfg = Config(ini_location)
        command.upgrade(alembic_cfg, "head")

    def database_data(self: Self):
        pass
