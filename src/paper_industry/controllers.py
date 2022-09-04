from flask_restful import Resource, request
from .serializers import PaperIndustrySerializer
from .models import PaperIndustry

class PaperIndustryControllers(object):

    def post(self):
        base_url = request.base_url
        if "register-comapny" in base_url:
            cleaned_data = request.data
            self.register_company(cleaned_data)

    def register_company(self, cleaned_data):
        serializer = PaperIndustrySerializer(**cleaned_data)
        company_data = cleaned_data['company_data']
        company_boss_data = cleaned_data['company_boss_data']
        if serializer.is_valid():
            PaperIndustry.create_company(**company_data)
            


