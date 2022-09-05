

from xml.dom import ValidationErr


class PaperIndustrySerializer(object):
    def __init__(
        self, company_name, company_address, company_email, company_cac,
        company_phone, firstname, lastname, email, phone
        ) -> None:
        self.company_name = company_name
        self.company_address = company_address
        self.company_email = company_email
        self.company_phone = company_phone
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.company_cac = company_cac
        self.phone = phone


    def validate_new_pickup_company(self, ):
        if not self.company_name or len(self.company_name) < 3:
            raise ValidationErr("Ensure you have provided a valid company name, greater than two characters in length")
        elif not self.company_address:
            raise ValidationErr("Please provide an email address")
        elif not self.company_email or "@" not in self.company_email:
            raise ValidationErr("Please provide the company valid email")
        elif not self.company_phone or len(self.company_phone) <= 10:
            raise ValidationErr("Please provide a valid company phone number")
        return True


    def validate_new_pickup_company_boss(self):
        if not self.firstname or len(self.firstname) < 3:
            raise ValidationErr("Ensure you have provided a valid first name for the companys' boss, greater than two characters in length")
        if not self.lastname or len(self.lastname) < 3:
            raise ValidationErr("Ensure you have provided a valid last name for the companys' boss, greater than two characters in length")
        elif not self.email or "@" not in self.email:
            raise ValidationErr("Please provide the company valid email")
        elif not self.phone or len(self.phone) <= 10:
            raise ValidationErr("Please provide a valid company phone number")
        return True


    def is_valid(self):
        boss_details = self.validate_new_pickup_company_boss()
        if type(boss_details) == str:
            return False
        pickup_company_details = self.validate_new_pickup_company()
        if type(pickup_company_details) == str:
            return False
        return True

    def errors(self):
        boss_details = self.validate_new_pickup_company_boss()
        if type(boss_details) == str:
            return boss_details
        pickup_company_details = self.validate_new_pickup_company()
        if type(pickup_company_details) == str:
            return pickup_company_details
