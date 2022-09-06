from src.config.db_config import (
    database_connection
)
import datetime

PickupCompanies = database_connection()['pickup_companies']
PickupCompanyOwner = database_connection()['pickup_company_owner']
class PaperIndustry(object):
    @staticmethod
    def create_company(company_name, company_address, companys_owner_id, company_primary_email, company_primary_phone, **other_company_details):
        PickupCompanies.insert_one({
            "company_name": company_name,
            "companys_owner_id": companys_owner_id,
            "company_address": company_address,
            "company_primary_email": company_primary_email.lower(),
            "company_primary_phone": company_primary_phone,
            "company_name": company_name,
            "date_registered": datetime.datetime.now(),
            **other_company_details
        })

    @staticmethod
    def create_companys_owner(companys_owner_firstname: str, companys_owner_lastname: str, companys_owner_email: str, companys_owner_phone: str, users_id):
        new_companys_owner = PickupCompanyOwner.insert_one({
            "companys_owner_firstname": companys_owner_firstname,
            "companys_owner_lastname": companys_owner_lastname,
            "companys_owner_email": companys_owner_email.lower(),
            "companys_owner_phone": companys_owner_phone,
            "users_id": users_id,
            "date_registered": datetime.datetime.now(),
        })
        print("\n\t new_companys_owner-create: ", new_companys_owner.inserted_id)
        return new_companys_owner.inserted_id