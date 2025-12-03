from utils.app_services.account import db_settings, db_url_obj
from utils.database import db_connection, get_db as get_db_


def get_db():
    return get_db_(db_connection(db_url_obj, db_settings))
