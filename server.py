import os
from src.config.environments import (
    DevEnvVariables,
    ProdEnvVariables
)
from flask import Flask
from flask_restful import Api
from src.accounts.controllers.AuthController import (
    UsersAccountController,
    auth_routes
)
from src.utilities.controllers import (
    UtilitiesControllers,
    utilities_routes
)
import logging
from flask_mail import Mail, Message


BASE_API = os.getenv("BASE_API")
FLASK_ENV = os.getenv("FLASK_ENV")
print("\n\t FLASK_ENV-server: ", FLASK_ENV)

logging.basicConfig(level=logging.INFO)

digiext_server = Flask(__name__)
digiext_api = Api(digiext_server)

if FLASK_ENV == "development":
    DevEnvVariables()
else:
    ProdEnvVariables()

digiext_server.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
digiext_server.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
digiext_server.config['MAIL_USERNAME'] = os.getenv("ADMIN_EMAIL")
digiext_server.config['MAIL_DISPLAY_NAME'] = "Digiext"
digiext_server.config['MAIL_PASSWORD'] = os.getenv("DIGIEXT_APP_PASSWORD")
digiext_server.config['MAIL_USE_TLS'] = False
digiext_server.config['MAIL_USE_SSL'] = True


send_mail = Mail(digiext_server)
digiext_api.add_resource(UsersAccountController, *auth_routes)
digiext_api.add_resource(UtilitiesControllers, *utilities_routes)
