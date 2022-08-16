import json
import logging
from xml.dom import ValidationErr
from flask_restful import Resource, request
import os

import secrets
secrets.token_hex()

from ..model import Tokens
from ..serializers.auth_serializers import (
    RegisterSerializer
)
from ..model.UsersAccount import (
    UsersAccount,
) 
BASE_API = os.getenv("BASE_API")

class UsersAccountController(Resource):
    logging.basicConfig(level=logging.INFO)
    def login(self, cleaned_request):
        print(cleaned_request)

    def sign_up(elf, cleaned_request):
        logging.info("\n\t Registering a user...")
        Users = UsersAccount()
        OTPToken = Tokens.Tokens()
        print("\n\t All users: ", Users.users.find({}))
        all_users = Users.users.find({})
        for user in all_users:
            print("\n\t user: ", user, user["_id"])
            del_stat = Users.find_by_id_and_delete(user['_id'])
            print("\n\t del_stat: ", del_stat)
        try:
            serializer = RegisterSerializer(**cleaned_request)
            print("\n\t serializer: ", serializer)
            if serializer.is_valid():
                hashed_password = OTPToken.hash_token(cleaned_request['password'])
                saved_user = UsersAccount.create(
                    email=cleaned_request['email'],
                    firstname=cleaned_request['firstname'],
                    lastname=cleaned_request['lastname'],
                    phone=cleaned_request['phone'],
                    password=hashed_password
                )
                print("\n\t saved_user: ", saved_user)
                if saved_user:
                    mail_status = Users.send_registration_email(receipients_email=cleaned_request['email'], fullname=f"{cleaned_request['firstname']} {cleaned_request['lastname']}")
                    print("\n\t mail_status: ", mail_status)
                    if mail_status['status']:
                        logging.info("Registration was successful.")
                        return {
                            "status": True,
                            "message": "Registration was successful. Please, check your email for verification.",
                            "status_code": 201
                        }
                
                print("\n\t sign_up: ", cleaned_request)
            raise ValidationErr(serializer.errors())
        except Exception as signup_error:
            logging.info("Registration failed.")
            return {
                "status": False,
                "message": str(signup_error),
                "status_code": 400
            }


    def post(self):
        try:
            url = request.url
            print("\n\t request.url: ", url)
            # print("\n\t request.base_url: ", request.base_url)
            cleaned_request = json.loads(request.data)
            print("\n\t cleaned_request: ", cleaned_request)
            if "login" in url:
                self.login(cleaned_request)
            elif 'register' in str(url):
                logging.info("\n\t Registering a user...")
                post_response = self.sign_up(cleaned_request)
                print("\n\t post_response: ", post_response)
                response_data = {"status": post_response['status'], "message": post_response['message']}
                return response_data, post_response['status_code']
        except Exception as post_error:
            print("\n\t post_error: ", post_error)


    def verify_auth_token(self, cleaned_request):
        try:
            print("\n\t verify_auth_token: ", cleaned_request)
            otp_code = cleaned_request['otp']
            otp_email = cleaned_request['email']
            print("\n\t otp_code: ", otp_code)
            users_details = UsersAccount.users.find_one({"email": otp_email})
            stringified_otp = ""
            for code in otp_code:
                stringified_otp += code
            if users_details:
                AuthToken = Tokens.Tokens
                otp_exists = AuthToken.verify_token(raw_token=stringified_otp, users_id=users_details['_id'])
                print("\n\t otp_exists: ", otp_exists)
                print("\n\t otp_email: ", otp_email)
                print("\n\t users_details: ", users_details)
                if otp_exists:
                    AuthToken.delete_token(stringified_otp)
                    login_token = AuthToken().generate_token(token_length=60, users_id=users_details["_id"], token_purpose="Login")
                    success_data = {
                        "status": True,
                        "login_token": login_token,
                        "status_code": 201,
                        "message": "Verification was successful"
                    }
                    print("\n\t Success: ", success_data)
                    return success_data
            raise ValidationErr("Unrecognised OTP")
        except Exception as verify_token_error:
            print("\n\t verify_token_error: ", verify_token_error)
            error_data = {
                "status": False,
                "message": str(verify_token_error),
                "status_code": 400,
            }
            return error_data


    def put(self):
        url = request.url
        cleaned_request = json.loads(request.data)
        print("\n\t request.base_url: ", request.base_url)
        if "verify-otp" in url:
            verify_response = self.verify_auth_token(cleaned_request)
            response_data = {"status": verify_response['status'], "message": verify_response['message']}
            return response_data, verify_response['status_code']



auth_routes = [
    f"{BASE_API}/users/login", 
    f"{BASE_API}/users/register",
    f"{BASE_API}/users/verify-otp",
]