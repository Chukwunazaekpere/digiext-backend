from pymongo import MongoClient
import os
import logging

def database_connection():
    try:
        logging.basicConfig(level=logging.INFO)
        logging.info("Digiext is initiating a databse connection...")
        PROD_DB_URL = os.getenv("PROD_DB_URL")
        LOCAL_DB_URL = os.getenv("LOCAL_DB_URL")

        FLASK_ENV = os.getenv("FLASK_ENV")
        db_client = MongoClient(host=PROD_DB_URL if FLASK_ENV != "development" else LOCAL_DB_URL)
        digiext_db = db_client["digiext_db"]
        logging.info("Digiext successfully connected to the databse...")
        return digiext_db
    except Exception as db_connection_error:
        print("\n\t db_connection_error: ", db_connection_error)
        return False