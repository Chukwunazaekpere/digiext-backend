import os
from .server import digiext_server

DEBUG = os.getenv("DEBUG")
PORT = os.getenv("PORT")


if __name__ == "__main__":
    digiext_server.run(
        debug=DEBUG,
        port=PORT
    )