import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

api = Api()
db = SQLAlchemy()
jwt = JWTManager()


# Method for initialize all modules and will return the app
def create_app():
    # Initialize Flask
    app = Flask(__name__)

    # Load environment variables
    load_dotenv()

    # If the database file does not exist, create it (only for SQLite)
    if not os.path.exists(os.getenv('DATABASE_PATH') + os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE_PATH') + os.getenv('DATABASE_NAME'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.getenv('DATABASE_PATH') + os.getenv('DATABASE_NAME')
    db.init_app(app)

    import main.resources as resources
    # Here will be initialized the rest of the app modules
    api.add_resource(resources.ScoreResource, '/score/<id>')
    api.add_resource(resources.ScoresResource, '/scores')
    api.add_resource(resources.PoemResource, '/poem/<id>')
    api.add_resource(resources.PoemsResource, '/poems')
    api.add_resource(resources.UserResource, '/user/<id>')
    api.add_resource(resources.UsersResource, '/users')

    # Flask.register_blueprint(app)
    api.init_app(app)

    # Load secret key
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    # Load time-to-live
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    jwt.init_app(app)

    from main.auth import routes
    # Import blueprint
    app.register_blueprint(routes.auth)

    # Return initialized app
    return app

