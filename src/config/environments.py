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
    os.environ["PORT"] = os.getenv("PORT")
    os.environ["DB_NAME"] = os.getenv("DB_NAME")

    os.environ['APP_SECRET'] = os.getenv("APP_SECRET")
    os.environ['MAIL_PORT'] = os.getenv("MAIL_PORT")
    os.environ['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
    os.environ['MAIL_USERNAME'] = os.getenv("ADMIN_EMAIL")
    os.environ['MAIL_PASSWORD'] = os.getenv("DIGIEXT_APP_PASSWORD")
    
    os.environ['CONFIG_EMAIL'] = os.getenv("CONFIG_EMAIL")
    os.environ['CONFIG_PHONE'] = os.getenv("CONFIG_PHONE")
    os.environ['CONFIG_FIRSTNAME'] = os.getenv("CONFIG_FIRSTNAME")
    os.environ['CONFIG_LASTNAME'] = os.getenv("CONFIG_LASTNAME")
    os.environ['CONFIG_PASSWORD'] = os.getenv("CONFIG_PASSWORD")





class DevEnvVariables(BaseConfig):
    def __init__(self) -> None:
        print("\n\t LOCAL_DB_URL: ", os.getenv("LOCAL_DB_URL"))
        os.environ["DB_URL"] = os.getenv("LOCAL_DB_URL")
        os.environ["DEBUG"] = "True"



class ProdEnvVariables(BaseConfig):
    def __init__(self) -> None:
        print("\n\t PROD_DB_URL: ", os.getenv("PROD_DB_URL"))
        os.environ["DB_URL"] = os.getenv("PROD_DB_URL")
        os.environ["DEBUG"] = "False"


    
