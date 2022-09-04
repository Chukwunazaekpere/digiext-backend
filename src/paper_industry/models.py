from src.config.db_config import (
    database_connection
)
import datetime

pickup_companies = database_connection()['pickup_companies']
class PaperIndustry(object):
    pickup_company_boss = database_connection()['pickup_company_boss']

    @staticmethod
    def create_company(company_name, company_address, companys_boss_id, company_primary_email, company_primary_phone, **other_company_details):
        pickup_companies.insert_one({
            "company_name": company_name,
            "companys_boss_id": companys_boss_id,
            "company_address": company_address,
            "company_primary_email": company_primary_email.lower(),
            "company_primary_phone": company_primary_phone,
            "company_name": company_name,
            "date_registered": datetime.datetime.now(),
            **other_company_details
        })

    def create_companys_boss(self, companys_boss_firstname: str, companys_boss_lastname: str, companys_boss_email: str, companys_boss_phone: str):
        new_companys_boss = self.pickup_company_boss.insert_one({
            "companys_boss_firstname": companys_boss_firstname,
            "companys_boss_lastname": companys_boss_lastname,
            "companys_boss_email": companys_boss_email.lower(),
            "companys_boss_phone": companys_boss_phone,
            "date_registered": datetime.datetime.now(),
        })
        return new_companys_boss._id