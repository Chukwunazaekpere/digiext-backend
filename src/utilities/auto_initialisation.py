
import logging
from xml.dom import ValidationErr
from src.accounts.model import (
    UsersAccount,
    Tokens
)
from src.accounts.model.UsersAccount import (
    Users
)
import os

Token = Tokens.Tokens()
def register_default_user():
    logging.basicConfig(level=logging.INFO)
    logging.info("Creating a default user")
    email = os.getenv("CONFIG_EMAIL")
    phone = os.getenv("CONFIG_PHONE")
    firstname = os.getenv("CONFIG_FIRSTNAME")
    lastname = os.getenv("CONFIG_LASTNAME")
    password = os.getenv("CONFIG_PASSWORD")
    try:
        user_exists = Users.find_one({
            "firstname": firstname,
            "lastname": lastname,
        })
        print("\n\t user_exists", user_exists)
        if not user_exists:
            hashed_password = Token.hash_token(password)
            Users.insert_one({
                "email":  email, 
                "lastname": lastname,
                "firstname": firstname,
                "phone": phone,
                "password": hashed_password
            })
            logging.info("\n\t User was successfully created..........")
            return True
        raise ValidationErr("User already exists")
    except Exception as error:
        print("\n\t User exists..........", error)
        return False

