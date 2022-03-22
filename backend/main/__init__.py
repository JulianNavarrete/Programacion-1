import os
from flask import Flask
from dotenv import load_dotenv

# Method for initialize all modules and will return the app
def create_app():
    # Initialize Flask
    app = Flask(__name__)

    # Load environment  variables
    load_dotenv()

    #
    # Here will be initialized the rest of the app modules
    #

    # Return initialized app
    return app
