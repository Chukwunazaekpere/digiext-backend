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
    AuthToken = Tokens.Tokens
    def login(self, cleaned_request):
        try:
            print("\n\t Login: ", cleaned_request)
            password = cleaned_request['password']
            email = cleaned_request['email']
            user_exists = DBUsers.find_one({"email": email})
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
            if serializer.is_valid():
                hashed_password = OTPToken.hash_token(cleaned_request['password'])
                print("\n\t hashed_password: ", hashed_password)
                saved_user = UsersAccount.create(
                    email=cleaned_request['email'],
                    firstname=cleaned_request['firstname'],
                    lastname=cleaned_request['lastname'],
                    phone=cleaned_request['phone'],
                    password=hashed_password
                )
                print("\n\t saved_user: ", saved_user)
                if saved_user:
                    mail_status = self.Users.send_registration_email(
                        receipients_email=cleaned_request['email'], 
                        fullname=f"{cleaned_request['firstname']} {cleaned_request['lastname']}", 
                        email_template="otp.html",
                        mail_subject="Registration Token From Digiext"
                    )
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
                response_data = {"auth_token": post_response['data'], "status": post_response['status'], "message": post_response['message']}
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
            print("\n\t otp_email: ", otp_email)
            users_details = DBUsers.find_one({"email": otp_email})
            stringified_otp = ""
            for code in otp_code:
                stringified_otp += code
            if users_details:
                otp_exists = self.AuthToken.verify_token(raw_token=stringified_otp, users_id=users_details['_id'])
                print("\n\t otp_exists: ", otp_exists)
                if otp_exists["status"]:
                    self.AuthToken.delete_token(otp_exists["hashed_token"])
                    login_token = self.AuthToken().generate_token(token_length=60, users_id=users_details["_id"], token_purpose="Login")
                    success_data = {
                        "status": True,
                        "auth_token": login_token,
                        "status_code": 201,
                        "message": "Verification was successful"
                    }
                    print("\n\t Success: ", success_data)
                    return success_data
            raise ValidationErr(otp_exists["message"])
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
            response_data = {"auth_token": verify_response["auth_token"], "status": verify_response['status'], "message": verify_response['message']}
            return response_data, verify_response['status_code']
        elif "authenticate" in url:
            authenticate_response = self.authenticate_user(cleaned_request=cleaned_request)
            print("\n\t authenticate_response: ", authenticate_response)
            return authenticate_response, authenticate_response['status_code']
        elif "update" in url:
            profile_update_response = self.update_users_details(request_data=cleaned_request)
            return profile_update_response, profile_update_response["status_code"]
        elif "verify-credentials" in url:
            verify_credentials_otp = self.verify_credentials_otp(request_data=cleaned_request)
            return verify_credentials_otp, verify_credentials_otp["status_code"]
        

    def verify_credentials_otp(self, request_data):
        otp_code = request_data["otpCode"]
        users_id = request_data["usersId"]
        user = self.Users.find_one(id=users_id)
        if user:
            otp_exists = self.AAuthToken.verify_token(raw_token=otp_code, users_id=users_id)




    def get_profile_details(self, users_id):
        try:
            print("\n\t -get_profile_detailsusers_id: ", users_id)
            user = self.Users.find_one(id=users_id)
            print("\n\t User: ", user)
            if user:
                data = {
                    **user,
                    "_id": str(user['_id'])
                }
                return {
                    "data": data,
                    "status_code": 200
                }
        except:
            return {
                    "data": None,
                    "status_code": 500
                }

    

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

    def get_user_logs(self, users_id):
        try:
            users_log = UserLogs.find({"users_id": users_id})
            if users_log:
                for log in users_log:
                    print("\n\t log: ", log)
            return {
                "data": users_log,
                "status_code": 200
            }
        except Exception as log_exception:
            print("\n\t log_exception: ", log_exception)
            return {
                "data": users_log,
                "status_code": 500
            }

    def update_users_details(self, request_data):
        try:
            print("\n\t request_data: ", request_data)
            users_id = request_data["usersId"]
            existing_data = self.Users.find_one(users_id)
            if existing_data:
                print("\n\t existing_data: ", existing_data)
                data_to_update = {
                    "firstname": request_data["firstname"],
                    "lastname": request_data["lastname"],
                    "phone": request_data["phone"],
                }
                self.Users.find_by_id_and_update(id=users_id, data={**data_to_update})
                return {
                    "message": "Profile has been successfully updated.",
                    "status_code": 200,
                }
            raise ValidationErr("An error was encountered")
        except Exception as update_profile_error:
            return {
                "message": "Profile was not updated this time.",
                "status_code": 500,
            }

    def change_credentials(self, users_id):
        try:
            user = self.Users.find_one(users_id)
            if user:
                mail_status = self.Users.send_registration_email(
                    receipients_email=user['email'], 
                    fullname=f"{user['firstname']} {user['lastname']}", 
                    email_template="change_credentials.html",
                    mail_subject="COC Token From Digiext"
                )
                if mail_status:
                    return {
                        "message": "Digiext honoured your request. Please check your email to continue.",
                        "status_code": 200,
                        "data": {"otp_code": mail_status["otp_code"]}
                    }
            raise ValidationErr("Error")
        except Exception as change_credentials_error:
            return {
                "message": "Digiext could not honour your request. Please try again.",
                "status_code": 500
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
                return profile_response, profile_response["status_code"]
            elif "authenticate" in url:
                authenticate_response = self.authenticate_user(token=users_id)
                print("\n\t authenticate_response: ", authenticate_response)
                return authenticate_response, authenticate_response['status_code']
            elif "details" in url:
                user_details_response = self.get_profile_details(users_id=users_id)
                return user_details_response, user_details_response["status_code"]
            elif "logs" in url:
                user_logs_response = self.get_user_logs(users_id=users_id)
                return user_logs_response, user_logs_response["status_code"]
            elif "credentials" in url:
                credentials_response = self.change_credentials(users_id=users_id)
                return credentials_response, credentials_response["status_code"]
         
        except Exception as error:
            print("\n\t error: ", error)

        

        

auth_routes = [
    f"{BASE_API}/login", 
    f"{BASE_API}/register",
    f"{BASE_API}/verify-otp",
    f"{BASE_API}/profiles/<users_id>",
    f"{BASE_API}/authenticate-user/<users_id>",
    f"{BASE_API}/authenticate-user",
    f"{BASE_API}/details/<users_id>",
    f"{BASE_API}/update-profile-details",
    f"{BASE_API}/logs/<users_id>",
    f"{BASE_API}/change-credentials/<users_id>",
    f"{BASE_API}/users/verify-credentials-otp",
]
