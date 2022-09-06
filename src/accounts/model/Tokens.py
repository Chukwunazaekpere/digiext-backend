from datetime import datetime
import hashlib
import logging
import secrets
from src.config.db_config import database_connection
# database_connection = config.db_config.database_connection
from . import UsersAccount
import os
from flask import Flask

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(Flask(__name__))

APP_SECRET = os.getenv("APP_SECRET") 


Users = UsersAccount.Users
tokens = database_connection()['tokens']
class Tokens(object):
    tokens = database_connection()['tokens']
    """
    This method generates a given token of the stated length and saves the token
    """
    def generate_token(self, token_length: int, users_id: str, token_purpose: str):
        logging.info("Generating token")
        try:
            required_token = secrets.token_hex(token_length)[0: token_length]
            hashed_token = self.hash_token(raw_token=required_token)
            print("\n\t hashed_token: ", hashed_token)
            tokens.insert_one({
                "users_id": users_id,
                "token": hashed_token,
                "token_purpose": token_purpose,
                "date_created": datetime.now()
            })
            print("\n\t required_token: ", required_token)

            if "login" in token_purpose.lower():
                print("\n\t contains login: ", hashed_token)
                required_token = hashed_token
            return required_token
        except Exception as generate_token_error:
            print("\n\t generate_token_error: ", generate_token_error)
            return None    
    
    @staticmethod
    def find_one(token: str):
        token_exists = tokens.find_one({"token": token})
        if token_exists:
            return token_exists
        return None
    

    @staticmethod
    def delete_token(token: str):
        try:
            tokens.delete_one({"token": token})
            return True
        except Exception as token_deletion_error:
            return False
        

    @staticmethod
    def hash_token(raw_token):
        logging.basicConfig(level=logging.INFO)
        logging.info("Hashing token")
        try:
            print("\n\t raw_token: ", raw_token)
            # hash_sequence = hashlib.sha512()
            # hash_sequence.update(("%s%s" % (APP_SECRET, raw_token)).encode("UTF-8"))
            # hashed_token = hash_sequence.hexdigest()
            hashed_token = bcrypt.generate_password_hash(password=raw_token)
            print("\n\t hashed_token: ", hashed_token)
            return hashed_token
        except Exception as hash_error:
            print("\n\t hash_error: ", hash_error)
            return None

    @staticmethod
    def compare_token(hashed_password, raw_token):
        logging.basicConfig(level=logging.INFO)
        logging.info("Comparing token")
        try:
            print("\n\t raw_token: ", raw_token)
            password_compare = bcrypt.check_password_hash(pw_hash=hashed_password, password=raw_token)
            print("\n\t password_compare: ", password_compare)
            return password_compare
        except Exception as hash_error:
            print("\n\t compare_token: ", hash_error)
            return None

    @staticmethod
    def verify_token(raw_token, users_id):
        try:
            tokens = database_connection()['tokens']
            Users = UsersAccount.UsersAccount().users
            print("\n\t raw_token: ", raw_token)
            hash_sequence = hashlib.sha512()
            hash_sequence.update(("%s%s" % (APP_SECRET, raw_token)).encode("UTF-8"))
            hashed_token = hash_sequence.hexdigest()
            saved_token = tokens.find_one({"token": hashed_token})
            if saved_token:
                saved_user = Users.find_one()
                saved_users_id = saved_user["_id"]
                if users_id == saved_users_id:
                    return True
            return False
        except Exception as hash_error:
            print("\n\t hash_error: ", hash_error)
            return False

