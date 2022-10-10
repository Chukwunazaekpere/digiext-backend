from datetime import datetime
from xml.dom import ValidationErr
from config.db_config import database_connection
import secrets
from pymongo.collection import ObjectId


class Industries(object):
    Industry = database_connection()["industries"]

    def create_industry(self, industry_name):
        try:
            industry_exists = self.find_by_industry_name(industry_name)
            industry_code = secrets.token_hex(4)
            if not industry_exists:
                new_industry = self.Industry.insert_one({
                    "industry_name": industry_name,
                    "industry_code": industry_code,
                    "date_created": datetime.now()
                })
                return {
                    "data": new_industry.inserted_id,
                    "status": True
                }
            raise ValidationErr("An industry with this name already exists.")
        except Exception as error:
            return {
                "data": error,
                "status": False
            }

    def delete_industry(self, industry_name):
        try:
            self.Industry.find_one_and_delete({"industry_name": industry_name})
            print("\n\t Delete industry: ", )
            return {
                "status": True
            }
        except Exception as delete_industry_exception:
            print("\n\t Delete industry: ", delete_industry_exception)
            return {
                "status": False
            }


    """
    Check if an industry exists, using its name
    """
    def find_by_industry_name(self, industry_name):
        industry_exists = self.Industry.find_one({"industry_name": industry_name})
        if industry_exists:
            return industry_exists
        return None

    
    """Get all industries"""
    def find(self):
        industries = self.Industry.find()
        print("\n\t industries: ", industries.collection)
        industry_list = []
        if industries:
            for industry in industries:
                print("\n\t industry: ", industry)
                industry_list.append(industry["industry_name"])
        return industry_list





class Companies(object):
    Company = database_connection()["companies"]
    def create_company(self, industry_id, company_name, company_logo, company_slogan, company_address, companys_owner_id, company_primary_email, company_primary_phone, **other_company_details):
        new_company = self.Company.insert_one({
            "company_name": company_name,
            "company_logo": company_logo,
            "company_slogan": company_slogan,
            "companys_owner_id": companys_owner_id,
            "company_address": company_address,
            "company_primary_email": company_primary_email.lower(),
            "company_primary_phone": company_primary_phone,
            "companys_owner_id": companys_owner_id,
            "industry_id": industry_id,
            "date_registered": datetime.now(),
            **other_company_details
        })
        return new_company.inserted_id

    
    """Get all companies"""
    def find(self):
        companies = self.Company.find()
        print("\n\t companies: ", companies.collection)
        company_list = []
        if companies:
            for company in companies:
                print("\n\t company: ", company)
                company_list.append(company["company_name"])
        return company_list

    def get_companies(self, no_restrictions):
        companies = self.Company.find()
        if no_restrictions:
            return companies
        # print("\n\t companies: ", companies.collection)
        company_list = []
        if companies:
            for company in companies:
                data={"company_name": company["company_name"], "_id": company["_id"]}
                company_list.append(data)
        return company_list

    """Get a company by id"""
    def find_by_id(self, company_id):
        # company_id = str(ObjectId(company_id))
        print("\n\t find_by_id: ", company_id)
        company = self.Company.find_one({"_id": ObjectId(company_id)})
        print("\n\t company-find_by_id: ", company)
        if company:
            return company
        return None


    def find_by_id_and_update(self, company_id, data_to_update):
        company = self.Company.find_one_and_update({"_id": ObjectId(company_id)}, {"$set": {**data_to_update}})
        print("\n\t company: ", company)
        if company:
            return company
        return None

    def find_by_id_and_delete(self, company_id):
        company = self.Company.find_one_and_delete({"_id": ObjectId(company_id)})
        print("\n\t deleted company: ", company)
        if company:
            return True
        return False

    """Get all industries"""
    def find_company_by_users_id(self, users_id):
        try:
            companies = self.Company.find({"companys_owner_id": ObjectId(users_id)})
            print("\n\t companies: ", companies)                
            company_list = []
            if companies:
                for company in companies:
                    print("\n\t find_company_by_users_id-company: ", company)
                    company_data = {
                        "company_name": company["company_name"],
                        "company_address": company["company_address"],
                        "company_primary_email": company["company_primary_email"].lower(),
                        "company_primary_phone": company["company_primary_phone"],
                        # "companys_owner_id": company["companys_owner_id"],
                        # "industry_id": company["industry_id"],
                        "date_registered": str(company["date_registered"]),
                    }
                    company_list.append(company_data)
                return company_list
            else:
                raise ValidationErr()
        except Exception as find_company_by_users_id_error:
            print("\n\t find_company_by_users_id_error: ", find_company_by_users_id_error)

    # @staticmethod
    # def create_companys_owner(companys_owner_firstname: str, companys_owner_lastname: str, companys_owner_email: str, companys_owner_phone: str, users_id):
    #     new_companys_owner = PickupCompanyOwner.insert_one({
    #         "companys_owner_firstname": companys_owner_firstname,
    #         "companys_owner_lastname": companys_owner_lastname,
    #         "companys_owner_email": companys_owner_email.lower(),
    #         "companys_owner_phone": companys_owner_phone,
    #         "users_id": users_id,
    #         "date_registered": datetime.datetime.now(),
    #     })
    #     print("\n\t new_companys_owner-create: ", new_companys_owner.inserted_id)
    #     return new_companys_owner.inserted_id
        