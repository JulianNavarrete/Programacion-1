# Import the functions which creates the app
from main import create_app
import os

# Call to the functions and return the app
app = create_app()

from main import db

# Do a push on the context of the app
# This allows to access the properties od the app on any part of the system
app.app_context().push()

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=os.getenv("PORT"))
    