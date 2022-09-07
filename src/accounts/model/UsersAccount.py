from datetime import datetime
import os
from config.db_config import (
    database_connection
)
from flask_mail import Message
from flask import render_template, render_template_string
from . import Tokens 
import server
# from src import server


Users = database_connection()["users"]
class UsersAccount(object):
    def get_fullname(self, users_id_or_email):
        try:
            user_by_id = Users.find_one({"": users_id_or_email})
            if user_by_id:
                users_fullname = f"{user_by_id['firstname']} {user_by_id['lastname']}"
                return users_fullname
            else:
                user_by_email = Users.find_one({"email": users_id_or_email})
                users_fullname = f"{user_by_email['firstname']} {user_by_email['lastname']}"
                return users_fullname
        except Exception as get_fullname_error:
            print("\n\t get_fullname_error: ", get_fullname_error)
            return None

    @staticmethod
    def find_by_id_and_delete(id):
        try:
            Users.delete_one({
                "_id": id
            })
            return True
        except Exception as find_by_id_and_delete_error:
            print("\n\t find_by_id_and_delete_error: ", find_by_id_and_delete_error)
            return False


    @staticmethod
    def create(firstname, lastname, email, phone, password):
        try:
            new_user = Users.insert_one({
                "firstname": firstname,
                "lastname": lastname,
                "email": email,
                "phone": phone,
                "password": password,
                "registered_companies": [],
                "requested_services": [],
                "date_registered": datetime.now()
            })
            return new_user
        except Exception as save_user_error:
            print("\n\t save_user_error: ", save_user_error)
            return False

    @staticmethod
    def find():
        all_users = Users.find({})
        return all_users
    

    @staticmethod
    def exists(users_id):
        users = database_connection()["users"]
        try:
            new_user = users.find_one({"id": users_id})
            if new_user:
                return True
            raise ValueError("User not found")
        except:
            return False

    
    def send_registration_email(self, receipients_email: str, fullname: str):
        mail_subject = "Registration Token From Digiext"
        print("\n\t receipients_email: ", receipients_email)
        try:
            tokens = Tokens.Tokens()
            receipient_details = Users.find_one({"email": receipients_email})
            if receipient_details:
                otp_code = tokens.generate_token(
                    token_length= 4,
                    token_purpose= "Registration",
                    users_id=receipient_details['_id'],
                )
                print("\n\t otp_code to send: ", otp_code)
                context={
                    "fullname": fullname,
                    "otp_code": otp_code,
                    "phone": f"{receipient_details['phone']}",
                    "year": datetime.now().year,
                    "subject":"Registration Mail From Digiext",
                }
                print("\n\t receipient_details: ", receipient_details)
                email_message = Message(
                    subject=mail_subject,
                    sender=os.getenv("ADMIN_EMAIL"),
                    recipients=[receipients_email],
                    html=render_template(template_name_or_list="otp.html", **context)
                )
                print("\n\t email_message: ", email_message)
                server.send_mail.send(email_message)
                return {
                    "status": True,
                    "message": f"Registration email has been successfully sent."
                }
            print("\n\t receipient_details: ", receipient_details)
            # raise ValidationErr(receipient_details)
        except Exception as send_reg_mail_error:
            print("\n\t send_reg_mail_error: ", send_reg_mail_error)
            return {
                "status": False,
                "message": f"Unable to send mail: {send_reg_mail_error}"
            }


        

