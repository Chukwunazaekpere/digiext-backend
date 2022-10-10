from src.utilities.logging_helper import logging_helper


from xml.dom import ValidationErr


class WasteAppointmentValidator(object):
    def __init__(self, users_id, pick_up_time, company_id, pick_up_interval) -> None:
        self.users_id = users_id
        self.pick_up_time = pick_up_time
        self.company_id = company_id
        self.pick_up_interval = pick_up_interval

    def validate_waste_appointment(self):
        try:
            if not self.users_id:
                raise ValueError("Please provide users id")
            if not self.pick_up_time:
                raise ValueError("Pick-up time is needed")
            if not self.company_id:
                raise ValueError("Please provide a company id")
            if not self.pick_up_interval:
                raise ValueError("Pick-up interval is needed")
            return True
        except Exception as validate_waste_appointment_error:
            logging_helper("error", validate_waste_appointment_error)
            return validate_waste_appointment_error

    def is_valid(self):
        status = self.validate_waste_appointment()
        if type(status) == bool:
            return True
        return False

    def errors(self):
        status = self.validate_waste_appointment()
        return status
