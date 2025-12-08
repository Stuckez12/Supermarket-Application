import logging

from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, DatabaseError, InterfaceError
from sqlalchemy.orm import Session
from typing import Self


class Initialise:
    def __init__(self, db: Session):
        self.db = db

    def check_database_connection(self: Self):
        try:
            self.db.execute(text("SELECT 1"))

        except (OperationalError, DatabaseError, InterfaceError):
            logging.error("Unable to connect to the database on startup")

            raise ConnectionError("Unable to connect to database")

    def database(self: Self, ini_location: str):
        alembic_cfg = Config(ini_location)
        command.upgrade(alembic_cfg, "head")
