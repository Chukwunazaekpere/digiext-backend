

from xml.dom import ValidationErr
from .models import ( 
    Companies,
    Industries
)

class CompanySerializer(object):
    def __init__(
        self, company_name, company_address, company_email, company_cac,
        company_phone, 
        ) -> None:
        self.company_name = company_name
        self.company_address = company_address
        self.company_email = company_email
        # print("\n\t company_email: ", self.company_email)
        self.company_phone = company_phone
        self.company_cac = company_cac


    def validate_new_company(self, ):
        if not self.company_name or len(self.company_name) < 3:
            raise ValidationErr("Ensure you have provided a valid company name, greater than two characters in length")
        elif not self.company_address:
            raise ValidationErr("Please provide an email address")
        elif not self.company_email or "@" not in self.company_email:
            raise ValidationErr("Please provide the company valid email")
        elif not self.company_phone or len(self.company_phone) <= 10:
            raise ValidationErr("Please provide a valid company phone number")
        return True

    # def validate_owner_bio_data(self):
    #     bio_data_by_name = PickupCompanyOwner.find_one({
    #         "firstname": self.firstname, 
    #         "lastname": self.lastname, 
    #     })
    #     bio_data_by_email = PickupCompanyOwner.find_one({"email": self.email})
    #     bio_data_by_phone = PickupCompanyOwner.find_one({"phone": self.phone})
    #     print("\n\t bio_data_by_phone: ", bio_data_by_phone)
    #     if bio_data_by_name:
    #         return "You can't register more than one company in the paper indusstry"
    #     if bio_data_by_email:
    #         return "A paper company owner has been registered with this email already"
    #     if bio_data_by_phone:
    #         return "A paper company owner has been registered with this phone already"
    #     return True


    def is_valid(self):
        pickup_company_details = self.validate_new_company()
        if type(pickup_company_details) == str:
            return False
        
        # owner_bio_data = self.validate_owner_bio_data()
        # if type(owner_bio_data) == str:
        #     return False
        return True

    def errors(self):
        pickup_company_details = self.validate_new_company()
        if type(pickup_company_details) == str:
            return pickup_company_details

        # owner_bio_data = self.validate_owner_bio_data()
        # print("\n\t owner_bio_data: ", owner_bio_data)
        # if type(owner_bio_data) == str:
        #     return owner_bio_data
