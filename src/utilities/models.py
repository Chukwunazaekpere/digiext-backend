from datetime import datetime
import logging
from config.db_config import (
    database_connection
)

UserLogs = database_connection()["user_logs"]
class UtilityModels(object):

    @staticmethod
    def create_user_logs(action: str, users_id: str):
        logging.basicConfig(level=logging.INFO)
        logging("Creating user log.")
        UserLogs.insert_one({
            "action": action,
            "users_id": users_id,
            "date_created": datetime.now()
        })
        