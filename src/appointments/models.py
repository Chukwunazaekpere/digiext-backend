from datetime import datetime
from config.db_config import database_connection

from src.utilities.logging_helper import logging_helper
class Appointments(object):
    appointments = database_connection()['appointments']
    Appointment_Status = [
        "Active",
        "Inactive",
    ]
    def __init__(self) -> None:
        pass

    def create_waste_appointment(self, users_id, pick_up_time, company_id, pick_up_interval):
        try:
            created_appointment = self.appointments.insert_one({
                "users_id": users_id,
                "pick_up_time": pick_up_time,
                "pick_up_interval": pick_up_interval,
                "waste_company_id": company_id,
                "status": self.Appointment_Status[0],
                "date_created": datetime.now()
            })
            return created_appointment.inserted_id
        except Exception as create_waste_appointment_error:
            logging_helper("error", create_waste_appointment_error)
            return None


    def get_users_appointments(self, users_id):
        try:
            users_appointments = self.appointments.find({"users_id": users_id})
            # logging_helper("info", "")
            return users_appointments
        except Exception as get_users_appointments_error:
            logging_helper("error", get_users_appointments_error)

    def update_users_appointments(self, users_id, update_data):
        try:
            users_appointments = self.appointments.find_one_and_update({"users_id": users_id}, {
                **update_data
            })
            # logging_helper("info", "")users
            return users_appointments
        except Exception as get_users_appointments_error:
            logging_helper("error", get_users_appointments_error)


