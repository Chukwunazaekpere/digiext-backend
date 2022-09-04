

from xml.dom import ValidationErr


class PaperIndustrySerializer(object):
    def __init__(
        self, company_name, company_address, companys_boss_id, company_primary_email, 
        company_primary_phone, companys_boss_firstname, companys_boss_lastname, companys_boss_email, companys_boss_phone
        ) -> None:
        self.company_name = company_name
        self.company_address = company_address
        self.companys_boss_id = companys_boss_id
        self.company_primary_email = company_primary_email
        self.company_primary_phone = company_primary_phone
        self.companys_boss_firstname = companys_boss_firstname
        self.companys_boss_lastname = companys_boss_lastname
        self.companys_boss_email = companys_boss_email
        self.companys_boss_phone = companys_boss_phone


    def validate_new_pickup_company(self, ):
        if not self.company_name or len(self.company_name) < 3:
            raise ValidationErr("Ensure you have provided a valid company name, greater than two characters in length")
        elif not self.company_address:
            raise ValidationErr("Please provide an email address")
        elif not self.companys_boss_id:
            raise ValidationErr("No boss is related to this company")
        elif not self.company_primary_email or "@" not in self.company_primary_email:
            raise ValidationErr("Please provide the company valid email")
        elif not self.company_primary_phone or len(self.company_primary_phone) <= 10:
            raise ValidationErr("Please provide a valid company phone number")
        return True


    def validate_new_pickup_company_boss(self):
        if not self.companys_boss_firstname or len(self.companys_boss_firstname) < 3:
            raise ValidationErr("Ensure you have provided a valid first name for the companys' boss, greater than two characters in length")
        if not self.companys_boss_lastname or len(self.companys_boss_lastname) < 3:
            raise ValidationErr("Ensure you have provided a valid last name for the companys' boss, greater than two characters in length")
        elif not self.companys_boss_email or "@" not in self.companys_boss_email:
            raise ValidationErr("Please provide the company valid email")
        elif not self.companys_boss_phone or len(self.companys_boss_phone) <= 10:
            raise ValidationErr("Please provide a valid company phone number")
        return True


    def is_valid(self):
        boss_details = self.validate_new_pickup_company_boss()
        if type(boss_details) == str:
            return boss_details
        pickup_company_details = self.validate_new_pickup_company()
        if type(pickup_company_details) == str:
            return pickup_company_details
        return True