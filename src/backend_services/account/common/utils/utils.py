from typing import Generator
from sqlalchemy.orm import Session

from utils.app_services.account import db_settings, db_url_obj
from utils.database import db_connection, get_db


def get_db_gen() -> Generator[Session, None, None]:
    return get_db(db_connection(db_url_obj, db_settings))
