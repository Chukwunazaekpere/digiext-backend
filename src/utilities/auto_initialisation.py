from xml.dom import ValidationErr
from src.accounts.model import (
    UsersAccount,
    Tokens
)
from .logging_helper import logging_helper
from src.accounts.model.UsersAccount import (
    Users
)
from src.companies.models import Industries
import os

Token = Tokens.Tokens()
def register_default_user():
    logging_helper("info", "Creating a default user")
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
            logging_helper("info", "\n\t User was successfully created..........")
            return True
        raise ValidationErr("User already exists")
    except Exception as error:
        logging_helper("info", f"\n\t User exists.......... {error}")
        return False


def create_default_industries():
    try:
        logging_helper("info", "\n\t Creating default industries.")
        industry_list = ["Wastes", "Machineries", "Uber", "Manufacturing", "Food", "Maintenance"]
        Industry = Industries()

        for industry in industry_list:
            creation_status = Industry.create_industry(industry_name=industry)
            # creation_status = Industry.delete_industry(industry_name="Electrical")
            print("\n\t creation_status: ", creation_status)
            if creation_status["status"]: 
                logging_helper("info", f"\n\t Created {industry} industry")
            else:
                logging_helper("info", f"\n\t {industry} industry already exists")
        logging_helper("info", f"\n\t Finished default industry creation")
        return True
    except Exception as error:
        logging_helper("error", f"\n\t {error} ")




