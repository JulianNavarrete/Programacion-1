import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
import main.resources as resources

api = Api()


# Method for initialize all modules and will return the app
def create_app():
    # Initialize Flask
    app = Flask(__name__)

    # Load environment  variables
    load_dotenv()

    # Here will be initialized the rest of the app modules
    api.add_resource(resources.QualificationResource, '/qualification/<id>')
    api.add_resource(resources.QualificationsResource, '/qualifications')
    api.add_resource(resources.PoemResource, '/poem/<id>')
    api.add_resource(resources.PoemsResource, '/poems')
    api.add_resource(resources.UserResource, '/user/<id>')
    api.add_resource(resources.UsersResource, '/users')

    # Return initialized app
    api.init_app(app)
    return app
