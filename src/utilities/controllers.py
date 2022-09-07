from flask_restful import Resource, request
import os
BASE_API = os.getenv("BASE_API")


class UtilitiesControllers(Resource):
  
    
    
    
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



utilities_routes = [
    f"{BASE_API}/utilities/get-industry-list",
    f"{BASE_API}/utilities/get-logs",
]