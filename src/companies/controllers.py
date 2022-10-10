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
from pymongo.collection import ObjectId

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
                print("\n\t base_url-post: ", base_url)
                print("\n\t cleaned_data: ", request.data)
                print("\n\t request.files: ", request.files)
                cleaned_data = json.loads(request.data)
                print("\n\t cleaned_data: ", cleaned_data)
                if "register-company" in base_url:
                    reg_status = self.register_company(cleaned_data, authenticated_user)
                    print("\n\t reg_status: ", reg_status)
                    return reg_status, reg_status['status_code']
            raise ValidationErr(error_message)
        except Exception as error:
            print("\n\t CompanyControllers-error: ", error)


    def register_company(self, cleaned_data, authenticated_user):
        try:
            company_details = cleaned_data['company-details']
            industry_name = cleaned_data['industry']
            print("\n\t register_company-industry_name: ", industry_name)
            serializer = CompanySerializer(**company_details)
            if serializer.is_valid():
                industry_details = self.Industry.find_by_industry_name(industry_name)
                if industry_details:
                    print("\n\t industry_details: ", industry_details)
                    new_company = self.Company.create_company(
                        industry_id=industry_details["_id"],
                        companys_owner_id=authenticated_user["_id"],
                        company_address=company_details["company_address"],
                        company_name=company_details["company_name"],
                        company_logo=company_details['company_logo'],
                        company_slogan=company_details['company_slogan'],
                        company_primary_email=company_details["company_email"],
                        company_cac=company_details["company_cac"],
                        company_primary_phone=company_details["company_phone"],
                    )
                    Users = UsersAccount()
                    user_registering_company = Users.find_one(authenticated_user["_id"])
                    keys = list(user_registering_company.keys())
                    registered_companies = (user_registering_company["registered_companies"]).append("new_company") if "registered_companies" in keys else [new_company]
                    print("\n\t user_registering_company-2: ",user_registering_company)
                    Users.find_by_id_and_update(
                        id=authenticated_user["_id"], 
                        data={"registered_companies": registered_companies}
                    )
                    print("\n\t user_registering_company-2: ",user_registering_company)
                    print("\n\t authenticated_user: ", authenticated_user["_id"])
                    new_log = UserLogs.insert_one({
                        "action": f"Created a new company, in the {industry_name}", 
                        "users_id": authenticated_user["_id"],
                        "date_created": datetime.now()
                    })
                    return {
                        "message": str("Your company has been successfully registered with Digiext."),
                        "status_code": 201
                    }
            print("\n\t serializer.errors: ", serializer.errors())
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
            elif "get-wastes-services" in url:
                response = self.get_wastes_services()
                return response, response['status_code']
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

    def get_wastes_services(self):
        try:
            all_companies = Companies.Company.find()
            all_waste_companies = []
            for company in all_companies:
                if "wastes" in company["company_name"].lower():
                    data = {
                        **company,
                        "_id": str(company["_id"]),
                        "industry_id": str(company["industry_id"]),
                        "companys_owner_id": str(company["companys_owner_id"]),
                        "date_registered": str(company["date_registered"]),
                        "company_bookings": []
                    }
                    all_waste_companies.append(data)
            print("\n\t all_waste_companies: ", all_waste_companies)
            return { 
                "data": all_waste_companies,
                "status_code": 200
            }
        except Exception as get_wastes_services_error:
            print("\n\t get_wastes_services_error: ", get_wastes_services_error)
            return { 
                "data": [],
                "status_code": 500
            }
company_routes = [
    f"/{BASE_API}/companies/register-company",
    f"/{BASE_API}/companies/get-industry-list",
    f"/{BASE_API}/companies/get-registered-companies",
    f"/{BASE_API}/companies/company-list/get-wastes-services"
]

