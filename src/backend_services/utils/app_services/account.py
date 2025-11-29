from account.settings import settings

from utils.database.database import DatabaseSettings, DatabaseURL


db_settings = DatabaseSettings()
db_url_obj = settings.get_db_url()
db_url_obj.db_name = "account"
