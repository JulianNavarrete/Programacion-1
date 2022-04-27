import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

api = Api()
db = SQLAlchemy()


# Method for initialize all modules and will return the app
def create_app():
    # Initialize Flask
    app = Flask(__name__)

    # Load environment  variables
    load_dotenv()

    if not os.path.exists(os.getenv('DATABASE_PATH') + os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE_PATH') + os.getenv('DATABASE_NAME'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.getenv('DATABASE_PATH') + os.getenv('DATABASE_NAME')
    db.init_app(app)

    import main.resources as resources
    # Here will be initialized the rest of the app modules
    api.add_resource(resources.QualificationResource, '/score/<id>')
    api.add_resource(resources.QualificationsResource, '/scores')
    api.add_resource(resources.PoemResource, '/poem/<id>')
    api.add_resource(resources.PoemsResource, '/poems')
    api.add_resource(resources.UserResource, '/user/<id>')
    api.add_resource(resources.UsersResource, '/users')

    # Return initialized app
    api.init_app(app)
    return app

