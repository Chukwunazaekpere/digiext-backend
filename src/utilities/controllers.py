from flask_restful import Resource, request
import os
BASE_API = os.getenv("BASE_API")

from ..paper_industry.models import (
    PickupCompanies
)
class UtilitiesControllers(Resource):
    def get_registered_companies(self, users_id):
        try:
            all_paper_pickup_companies = PickupCompanies.find()
            users_registered_companies = []
            for company in all_paper_pickup_companies:
                if str(company['users_id']) == users_id:
                    users_registered_companies.append(company)
            return {
                "data": users_registered_companies,
                "status": True,
                "status_code": 200
            }
        except Exception as error:
            return {
                "data": None,
                "status": False,
                "status_code": 400
            }
    
    def list_all_industries(self):
        industry_list = ["Paper", "Agriculture", "Manufacturing", "Food"]
        return {
            "status": True,
            "data": industry_list,
            "status_code": 200
        }
    
    def get_logs(self):
        industry_list = ["Paper", "Agriculture", "Manufacturing", "Food"]
        return {
            "status": True,
            "data": industry_list,
            "status_code": 200
        }

    def get(self):
        try:
            url = request.url
            print("\n\t Get industries: ", url.split("/"))
            if "industry-list" in url:
                industry_list = self.list_all_industries()
                print("\n\t industry_list: ", industry_list)
                return industry_list, 200
            elif "get-registered-companies" in url:
                response = self.get_registered_companies(users_id=users_id)
                return response, response["status_code"]
        except Exception as error:
            print("\n\t Exception: ", error)



utilities_routes = [
    f"{BASE_API}/utilities/get-industry-list",
    f"{BASE_API}/utilities/get-logs",
    f"{BASE_API}/utilities/companies/get-registered-companies?users-id"
]