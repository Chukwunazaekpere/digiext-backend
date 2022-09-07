from datetime import datetime
from xml.dom import ValidationErr
from ..utilities.authenticate import authenticate_requests
import json
from flask_restful import Resource, request
from .serializers import CompanySerializer
from .models import (
    Companies,
    Industries
)

from src.accounts.model.UsersAccount import UsersAccount
import os
BASE_API = os.getenv("BASE_API")
from src.utilities.models import (
    UserLogs,
    UtilityModels
)

class CompanyControllers(Resource):
    Company = Companies()
    Industry = Industries()
    
    def post(self):
        try:
            authorization = request.headers["Authorization"]
            authorization_token = authorization.split(" ")[1]
            print("\n\t authorization_token: ", authorization_token)
            authenticate_request = authenticate_requests(token=authorization_token)
            error_message = authenticate_request["message"]
            if authenticate_request["status"]:
                authenticated_user = authenticate_request["user"]
                base_url = request.base_url
                print("\n\t base_url: ", base_url)
                cleaned_data = json.loads(request.data)
                print("\n\t cleaned_data: ", cleaned_data)
                if "register-company" in base_url:
                    reg_status = self.register_company(cleaned_data, authenticated_user)
                    print("\n\t reg_status: ", reg_status)
                    return reg_status, reg_status['status_code']
            raise ValidationErr(error_message)
        except Exception as error:
            print("\n\t PaperIndustryControllers-error: ", error)


    def register_company(self, cleaned_data, authenticated_user):
        try:
            company_details = cleaned_data['company-details']
            industry_name = cleaned_data['industry']
            print("\n\t company_details: ", company_details)
            serializer = CompanySerializer(**company_details)
            if serializer.is_valid():
                industry_details = self.Industry.find_by_industry_name(industry_name)
                if industry_details:
                    new_company = self.Company.create_company(
                        industry_id=industry_details["_id"],
                        companys_owner_id=authenticated_user["_id"],
                        company_address=company_details["company_address"],
                        company_name=company_details["company_name"],
                        company_primary_email=company_details["company_email"],
                        company_cac=company_details["company_cac"],
                        company_primary_phone=company_details["company_phone"],
                    )
                    Users = UsersAccount()
                    Users.find_by_id_and_update(authenticated_user["_id"], {
                        "registered_companies": authenticated_user["registered_companies"].append(new_company)
                    })
                    new_log = UserLogs.insert_one({
                        "action": f"Created a new company, in the {industry_name}", 
                        "users_id": authenticated_user["_id"],
                        "date_created": datetime.now()
                    })
                return {
                    "message": str("Your paper company has been successfully registered with Digiext."),
                    "status_code": 201
                }
            # print("\n\t serializer.errors: ", serializer.errors())
            raise ValueError(serializer.errors())
        except Exception as error:
            print("\n\t error: ", error)
            return {
                "message": str(error),
                "status_code": 400
            }
            
    
    def get(self):
        try:
            authorization = request.headers["Authorization"]
            authorization_token = authorization.split(" ")[1]
            print("\n\t authorization_token: ", authorization_token)
            authenticate_request = authenticate_requests(token=authorization_token)
            error_message = authenticate_request["message"]
            url = request.url
            # print("\n\t Get industries: ", url.split("/"))
            if "industry-list" in url:
                industry_list = self.list_all_industries()
                print("\n\t industry_list: ", industry_list)
                return industry_list, 200
            elif "get-registered-companies" in url:
                args = request.args
                args = args.to_dict()
                users_id = args["users-id"]
                # print(args)
                response = self.get_registered_companies(users_id=users_id)
                return response, response["status_code"]
        except Exception as error:
            print("\n\t Exception: ", error)

    
    def list_all_industries(self):
        all_industries = self.Industry.find()
        print("\n\t all_industries: ", all_industries)
        return {
            "status": True,
            "data": all_industries,
            "status_code": 200
        }


    def get_registered_companies(self, users_id):
        try:
            user_registered_companies = self.Company.find_company_by_users_id(users_id)
            print("\n\t users_registered_companies: ", list(user_registered_companies))
            return {
                "data": user_registered_companies,
                "status": True,
                "status_code": 200
            }
        except Exception as error:
            print("\n\t get_registered_companies_error: ", error)
            return {
                "data": None,
                "status": False,
                "status_code": 400
            }

company_routes = [
    f"/{BASE_API}/companies/register-company",
    f"/{BASE_API}/companies/get-industry-list",
    f"/{BASE_API}/companies/get-registered-companies"
]

