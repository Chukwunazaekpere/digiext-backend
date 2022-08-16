from pickle import TRUE
from dotenv import load_dotenv
import os

load_dotenv(
    os.path.join(os.path.dirname( __file__), ".env")
)
print("\m\t ENV: ",  os.path.join(os.path.dirname( __file__), ".env"))

class BaseConfig(object):
    os.environ["FLASK_ENV"] = os.getenv("FLASK_ENV")
    print("\n\t FLASK_ENV: ", os.getenv("FLASK_ENV"))
    PORT = os.getenv("PORT")
    os.environ["BASE_API"] = os.getenv("BASE_API")
    os.environ['APP_SECRET'] = os.getenv("APP_SECRET")
    os.environ['APP_SALT'] = os.getenv("APP_SALT")
    os.environ['MAIL_PORT'] = os.getenv("MAIL_PORT")
    os.environ['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
    os.environ['MAIL_USERNAME'] = os.getenv("ADMIN_EMAIL")
    os.environ['MAIL_PASSWORD'] = os.getenv("DIGIEXT_APP_PASSWORD")




class DevEnvVariables(BaseConfig):
    print("\n\t LOCAL_DB_URL: ", os.getenv("LOCAL_DB_URL"))
    def load_env_variables():
        os.environ["DB_URL"] = os.getenv("LOCAL_DB_URL")
        os.environ["DEBUG"] = "True"



class ProdEnvVariables(BaseConfig):
    def load_env_variables():
        os.environ["DB_URL"] = os.getenv("PROD_DB_URL")
        os.environ["DEBUG"] = "False"


    
