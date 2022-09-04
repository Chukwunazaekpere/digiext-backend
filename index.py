import os
# from .server import digiext_server
from server import digiext_server

DEBUG = os.getenv("DEBUG")
PORT = os.getenv("PORT")

digiext_server.run(
    debug=DEBUG,
    port=PORT
)