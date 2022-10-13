import datetime
import json
from src.utilities.models import (
    UserLogs,
    UtilityModels
)

from src.utilities.logging_helper import logging_helper
import os
from flask_restful import Resource, request
from .validator import WasteAppointmentValidator
BASE_API = f"{os.getenv('BASE_API')}/appointments"

from .models import Appointments
from ..companies.models import Companies
class AppointmentsController(Resource):
    UsersAppointments = Appointments()
    RegisteredCompanies = Companies()
    def post(self):
        url = request.url

        if "create-wastes" in url:
            creation_response = self.create_waste_appointment(request.data)
            return creation_response, creation_response["status_code"]


    def create_waste_appointment(self, appointment_details):
        try:
            appointment_details = json.loads(appointment_details)
            print("\n\t appointment_details: ", appointment_details)
            data_to_validate = {
                "company_id": appointment_details["company_id"],
                "pick_up_interval": appointment_details["pick_up_interval"],
                "pick_up_time": appointment_details["pick_up_time"],
                "users_id": appointment_details["users_id"],
            }
            validation = WasteAppointmentValidator(**data_to_validate)
            if validation.is_valid():
                # print("\n\t Validation is valid")
                newly_created_appointment = self.UsersAppointments.create_waste_appointment(
                    users_id=data_to_validate["users_id"],
                    pick_up_interval=data_to_validate["pick_up_interval"],
                    pick_up_time=data_to_validate["pick_up_time"],
                    company_id=data_to_validate["company_id"]
                )
                appointed_company = self.RegisteredCompanies.find_by_id(company_id=data_to_validate["company_id"])
                print("\n\t appointed_company: ", appointed_company)

                # all_companies = self.RegisteredCompanies.get_companies(no_restrictions=True)
                # print("\n\t all_companies: ", all_companies[0])
                # for company in all_companies:
                #     if company["_id"] != appointed_company["_id"]:
                #         self.RegisteredCompanies.find_by_id_and_delete(company_id=company["_id"])

                appointed_company_keys = list(appointed_company.keys())
                print("\n\t newly_created_appointment: ", newly_created_appointment)
                company_bookings = appointed_company['company_bookings'] if "company_bookings" in appointed_company_keys else []
                company_bookings.append(newly_created_appointment)
                self.RegisteredCompanies.find_by_id_and_update(
                    company_id=data_to_validate["company_id"], 
                    data_to_update={"company_bookings": company_bookings}
                )
                # UserLogs.insert_one({
                #     "action": f"Created a new company, in the {industry_name}", 
                #     "users_id": authenticated_user["_id"],
                #     "date_created": datetime.now()
                # })
                return {
                    "message": f"Appointment with {appointed_company['company_name']} comapny has been successfully placed.",
                    "status_code": 201
                }
            raise validation.errors()
        except Exception as create_waste_appointment_error:
            logging_helper("error", create_waste_appointment_error)
            return {
                "message": create_waste_appointment_error,
                "status_code": 500
            }

    def get_user_appointments(self, users_id):
        try:
            users_appointments = self.UsersAppointments.get_users_appointments(users_id=users_id)
            # print("\n\t users_appointments: ", users_appointments)
            requiredAppointmentData = []
            for appointment in users_appointments:
                company_id = appointment['waste_company_id']
                company_details = self.RegisteredCompanies.find_by_id(company_id)
                # print("\n\t company_details: ", company_details)
                if company_details:
                    data = {
                        "company_name": company_details["company_name"],
                        "company_phone": company_details["company_primary_phone"],
                        "company_email": company_details["company_primary_email"],
                        "company_address": company_details["company_address"],
                        "pick_up_time": appointment["pick_up_time"],
                        "pick_up_interval": appointment["pick_up_interval"],
                        "status": appointment["status"],
                        "date_created": str(appointment["date_created"]),
                    }
                    requiredAppointmentData.append(data)
                    print("\n\t appointment: ", appointment)
            return {
                "data": requiredAppointmentData,
                "status_code": 200
            } 
        except Exception as get_user_appointments_error:
            print("\n\t get_user_appointments_error: ", get_user_appointments_error)
            return {
                "data": [],
                "status_code": 500
            }


    def get(self, users_id):
        print("\n\t users_id: ", users_id)
        url = request.url
        if "get-user-appointments" in url:
            response = self.get_user_appointments(users_id)
            print("\n\t response: ", response)
            return response, response["status_code"]

appointment_routes = [
    f"{BASE_API}/create-wastes-appointment",
    f"{BASE_API}/get-user-appointments/<users_id>",
]