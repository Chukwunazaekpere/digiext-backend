import os
# from server import digiext_server
import server

DEBUG = os.getenv("DEBUG")
PORT = os.getenv("PORT")

digiext_server = server.digiext_server
digiext_server.run(
    debug=DEBUG,
    port=PORT
)