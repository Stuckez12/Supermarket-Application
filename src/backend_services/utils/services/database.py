from account.settings import settings

from utils.database.database import DatabaseSettings


account_db_settings = DatabaseSettings()
account_db_url_obj = settings.get_db_url()
account_db_url_obj.db_name = "account"
