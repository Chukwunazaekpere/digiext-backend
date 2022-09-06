from pymongo import MongoClient
import os
import logging


def database_connection():
    try:
        logging.basicConfig(level=logging.INFO)
        logging.info("Digiext is initiating a databse connection...")
        DB_URL = os.getenv("DB_URL")
        DB_NAME = os.getenv("DB_NAME")
        # print()
        db_client = MongoClient(host=DB_URL)
        digiext_db = db_client[DB_NAME]
        logging.info("Digiext successfully connected to the databse...")
        return digiext_db
    except Exception as db_connection_error:
        print("\n\t db_connection_error: ", db_connection_error)
        return False