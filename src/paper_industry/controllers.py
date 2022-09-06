from curses import flash
from datetime import datetime
from xml.dom import ValidationErr
from ..utilities.authenticate import authenticate_requests
import json
from traceback import print_tb
from flask_restful import Resource, request
from .serializers import PaperIndustrySerializer
from .models import PaperIndustry
import os
BASE_API = os.getenv("BASE_API")
from src.utilities.models import (
    UserLogs,
    UtilityModels
)
from ..paper_industry.models import (
    PickupCompanies
)
class PaperIndustryControllers(Resource):
    def post(self):
        try:
            authorization = request.headers["Authorization"]
            print("\n\t authorization: ", authorization)
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
            company_owner_details = cleaned_data['company-owner-details']
            company_data = {**company_details, **company_owner_details}
            print("\n\t company_data: ", company_data)
            serializer = PaperIndustrySerializer(**company_data)
            # print("\n\t serializer.is_valid: ", serializer.is_valid())
            if serializer.is_valid():
                new_companys_owner_id = PaperIndustry.create_companys_owner(
                    companys_owner_email=company_data["email"],
                    companys_owner_firstname=company_data["firstname"],
                    companys_owner_lastname=company_data["lastname"],
                    companys_owner_phone=company_data["phone"],
                    users_id=authenticated_user["_id"]
                )
                PaperIndustry.create_company(
                    company_address=company_data["company_address"],
                    company_name=company_data["company_name"],
                    company_primary_email=company_data["company_email"],
                    company_cac=company_data["company_cac"],
                    companys_owner_id=new_companys_owner_id,
                    company_primary_phone=company_data["company_phone"],
                )
                new_log = UserLogs.insert_one({
                    "action": "Created a new company.", 
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
            
 

paper_industry_routes = [
    f"/{BASE_API}/paper-industry/register-company",
]

