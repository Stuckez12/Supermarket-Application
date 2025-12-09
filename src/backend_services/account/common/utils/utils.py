from typing import Generator
from sqlalchemy.orm import Session

from utils.app_services.account import account_db_settings, account_db_url_obj
from utils.database import db_connection, get_db


def get_db_gen() -> Generator[Session, None, None]:
    return get_db(db_connection(account_db_url_obj, account_db_settings))
