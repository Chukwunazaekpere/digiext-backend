from pymongo import MongoClient
import os
import logging

# PROD_DB_URL = "mongodb+srv://Chukwunazaekpere:Chemmaco%401958@authentification.cu4aa.mongodb.net/DigiextDB?retryWrites=true&w=majority"

def database_connection():
    try:
        logging.basicConfig(level=logging.INFO)
        logging.info("Digiext is initiating a databse connection...")
        DB_URL = os.getenv("DB_URL")
        PROD_DB_URL = os.getenv("PROD_DB_URL")
        print("\n\t database_connection-PROD_DB_URL: ", PROD_DB_URL)
        db_client = MongoClient(host=DB_URL)
        digiext_db = db_client["digiext_db"]
        logging.info("Digiext successfully connected to the databse...")
        return digiext_db
    except Exception as db_connection_error:
        print("\n\t db_connection_error: ", db_connection_error)
        return False