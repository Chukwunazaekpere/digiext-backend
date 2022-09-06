from datetime import datetime
import json
import logging
from xml.dom import ValidationErr
from flask_restful import Resource, request
import os
from src.utilities.authenticate import authenticate_requests
from ..model import Tokens
from ..serializers.auth_serializers import (
    RegisterSerializer
)
from ..model.UsersAccount import (
    UsersAccount,
) 
from ..model.UsersAccount import Users as DBUsers
from src.utilities.models import UtilityModels, UserLogs

BASE_API = os.getenv("BASE_API")
BASE_API = f"{BASE_API}/users"

class UsersAccountController(Resource):
    logging.basicConfig(level=logging.INFO)
    Users = UsersAccount()
    def login(self, cleaned_request):
        try:
            print("\n\t Login: ", cleaned_request)
            password = cleaned_request['password']
            email = cleaned_request['email']
            user_exists = self.Users.find_one({"email": email})
            error_message = "User does not exist."
            if user_exists:
                print("\n\t user_exists: ", user_exists)
                existing_password = user_exists['password']
                password_is_same = Tokens.Tokens.compare_token(hashed_password=existing_password, raw_token=password)
                error_message = "Unrecognised credentials."
                if password_is_same:
                    login_token = Tokens.Tokens()
                    users_id = user_exists["_id"]
                    auth_token = login_token.generate_token(
                        token_length=60, 
                        users_id=users_id, 
                        token_purpose="Login-Token", 
                    )
                    token_and_id = f"{auth_token}:{users_id}"
                    return {
                        "data": token_and_id,
                        "status_code": 200,
                        "status": True,
                        "message": "Login successfull",
                    }
            raise ValidationErr(error_message)
        except Exception as login_error:
            print("\n\t login_error: ", login_error)
            return {
                "message": str(login_error),
                "status_code": 400,
                "status": False,
                "data": None
            }


    def sign_up(self, cleaned_request):
        logging.info("\n\t Registering a user...")
        OTPToken = Tokens.Tokens()
        all_users = self.Users.find()
        print("\n\t All users: ", all_users)
        for user in all_users:
            print("\n\t user: ", user, user["_id"])
            del_stat = self.Users.find_by_id_and_delete(user['_id'])
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
                    mail_status = self.Users.send_registration_email(receipients_email=cleaned_request['email'], fullname=f"{cleaned_request['firstname']} {cleaned_request['lastname']}")
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
                post_response = self.login(cleaned_request)
                response_data = {"data": post_response['data'], "status": post_response['status'], "message": post_response['message']}
                return response_data, post_response['status_code']
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
            all_users = self.Users.find()
            print("\n\t All users: ", all_users)
            for user in all_users:
                print("\n\t user: ", user)

            print("\n\t verify_auth_token: ", cleaned_request)
            otp_code = cleaned_request['otp']
            otp_email = cleaned_request['email']
            print("\n\t otp_code: ", otp_code)
            users_details = DBUsers.find_one({"email": otp_email})
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
        elif "authenticate" in url:
            authenticate_response = self.authenticate_user(cleaned_request=cleaned_request)
            print("\n\t authenticate_response: ", authenticate_response)
            return authenticate_response, authenticate_response['status_code']


    def get_profile_details(self, users_id):
        user = self.Users.find_one({"_id": users_id})
        if user:
            return {
                "data": user
            }
        return None
    

    def authenticate_user(self, cleaned_request):
        try:
            # print("\n\t cleaned_request: ", cleaned_request)
            users_id = cleaned_request["id"]
            auth_token = cleaned_request["token"]
            found_token = authenticate_requests(token=f"{auth_token}:{users_id}")
            error_message = "Token life has been exceeded."
            if found_token['status']:
                user = found_token["user"]
                # print("\n\t user: ", user)
                saved_users_id = user["_id"]
                error_message = "Token comparison failed"
                if users_id == str(saved_users_id):
                    new_log = UserLogs.insert_one({
                        "action": "Opened App", 
                        "users_id": saved_users_id,
                        "date_created": datetime.now()
                    })
                    # print("\n\t new Log: ", new_log)
                    return {
                        # "data": None,
                        "status": True,
                        "status_code": 200
                    }
            raise ValidationErr(error_message)
        except Exception as authenticate_user_exception:
            print(authenticate_user_exception)
            return {
                # "data": None,
                "status": False,
                "status_code": 403,
                "message": str(authenticate_user_exception)
            }

    
    def get(self, users_id):
        try:
            url = request.url
            print("\n\t url: ", url)
            # users_id = request.args.get("users_id")
            print("\n\t args: ", request.args.get("users_id"))
            print("\n\t users_id: ", users_id)
            if "profiles" in url:
                profile_response = self.get_profile_details(users_id=users_id)
            elif "authenticate" in url:
                authenticate_response = self.authenticate_user(token=users_id)
                print("\n\t authenticate_response: ", authenticate_response)
                return authenticate_response, authenticate_response['status_code']
        except Exception as error:
            print("\n\t error: ", error)

        

        

auth_routes = [
    f"{BASE_API}/login", 
    f"{BASE_API}/register",
    f"{BASE_API}/verify-otp",
    f"{BASE_API}/profiles/<users_id>",
    f"{BASE_API}/authenticate-user/<users_id>",
    f"{BASE_API}/authenticate-user",
]