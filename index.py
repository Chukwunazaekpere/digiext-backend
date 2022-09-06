import os
from flask_bcrypt import Bcrypt
# from .server import digiext_server
from server import digiext_server
# bcrypt = Bcrypt(digiext_server)

DEBUG = os.getenv("DEBUG")
PORT = os.getenv("PORT")

digiext_server.run(
    debug=DEBUG,
    port=PORT
)