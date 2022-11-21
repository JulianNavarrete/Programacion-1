import os
from flask import Flask
from dotenv import load_dotenv

# Method for initialize all modules and will return the app
def create_app():
    # Initialize Flask
    app = Flask(__name__, static_url_path='/static')

    # Load environment  variables
    load_dotenv()

    #
    # Here will be initialized the rest of the app modules
    #
    app.config['API_URL'] = os.getenv('API_URL')

    from main.routes import user, poem, main
    app.register_blueprint(main.main)
    app.register_blueprint(user.user)
    app.register_blueprint(poem.poem)

    # Return initialized app
    return app
