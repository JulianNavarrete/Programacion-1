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
    app.config['API_URL'] = os.getenv('API_URL')
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    from main.routes import main, poems, users
    app.register_blueprint(routes.main.main)
    app.register_blueprint(routes.poems.poems)
    app.register_blueprint(routes.users.users)


    # Return initialized app
    return app
