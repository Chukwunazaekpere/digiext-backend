from email import message
import json
from traceback import print_tb
from flask_restful import Resource, request
from .serializers import PaperIndustrySerializer
from .models import PaperIndustry
import os
BASE_API = os.getenv("BASE_API")


class PaperIndustryControllers(Resource):

    def post(self):
        try:
            base_url = request.base_url
            print("\n\t base_url: ", base_url)
            cleaned_data = json.loads(request.data)
            print("\n\t cleaned_data: ", cleaned_data)
            if "register-company" in base_url:
                reg_status = self.register_company(cleaned_data)
                print("\n\t reg_status: ", reg_status)
                return reg_status, reg_status['status_code']

        except:
            pass

    def register_company(self, cleaned_data):
        try:
            company_details = cleaned_data['company-details']
            company_owner_details = cleaned_data['company-owner-details']
            company_data = {**company_details, **company_owner_details}
            serializer = PaperIndustrySerializer(**company_data)
            print("\n\t serializer.is_valid: ", serializer.is_valid())
            if serializer.is_valid():
                PaperIndustry.create_company(**company_data)
                return
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

