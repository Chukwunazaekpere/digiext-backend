from ..model import (
    UsersAccount,
)


class RegisterSerializer(object):
    Users = UsersAccount.UsersAccount().users
    def __init__(self, firstname: str, lastname: str, email: str, phone: str, password: str, confirm_password: str) -> None:
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.password = password
        self.confirm_password = confirm_password

    def validate_data_existence(self, **kwargs):
        try:
            user_by_email = self.Users.find_one({"email": self.email})
            print("\n\t user_by_email: ", user_by_email)
            if user_by_email:
                return {
                    "status": False,
                    "message": "A user with this email already exists"
                }
            phone = self.Users.find_one({"phone": self.phone})
            print("\n\t phone: ", phone)
            if phone:
                return {
                    "status": False,
                    "message": "A user with this phone number already exists"
                }
            user_by_name = self.Users.find_one({
                "firstname": self.firstname,
                "lastname": self.lastname
            })
            print("\n\t user_by_name: ", user_by_name)
            if user_by_name:
                return {
                    "status": False,
                    "message": "A user with this sequence of firstname and lastname already exists"
                }
            return {
                "status": True,
                "message": ""
            }
        except Exception as validator_error:
            print("\n\t validator_error: ", validator_error)
            return {
                "status": False,
                "message": validator_error
            }

    def password_similarity(self):
        if len(self.password) < 6:
            return {
                "status": False,
                "message": "Password length must be six characters long or more"
            }
        if self.password != self.confirm_password:
            return {
                "status": False,
                "message": "Password discrepancy"
            }
        return {
            "status": True,
            "message": ""
        }

    def is_valid(self):
        try:
            validate_data_existence = self.validate_data_existence()
            print("\n\t validate_data_existence: ", validate_data_existence)
            if validate_data_existence['status']:
                password_similarity = self.password_similarity()
                if password_similarity['status']:
                    return True
            return False
        except Exception as is_valid_error:
            print("\n\t is_valid_error: ", is_valid_error)
            return False


    def errors(self):
        try:
            validate_data_existence = self.validate_data_existence()
            error_message = validate_data_existence['message']
            print("\n\t validate_data_existence: ", validate_data_existence)

            if validate_data_existence['status']:
                password_similarity = self.password_similarity()
                error_message = password_similarity['message']
                if password_similarity['status']:
                    return ""
            return error_message
        except Exception as is_valid_error:
            print("\n\t is_valid_error: ", is_valid_error)
            return error_message