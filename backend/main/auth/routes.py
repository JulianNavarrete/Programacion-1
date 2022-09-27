from flask import request, Blueprint, jsonify
from .. import db
from main.models import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from main.mail.functions import send_mail


# Blueprint to access auth methods
auth = Blueprint('auth', __name__, url_prefix='/auth')


# Login method
@auth.route('/login', methods=['POST'])
def login():
    # Find the user in the db by mail
    user = db.session.query(UserModel).filter(UserModel.email == request.get_json().get("email")).first_or_404()
    # Validate the password
    if user.validate_pass(request.get_json().get("password")):
        # Generate a new token
        # Returns user object as identity
        access_token = create_access_token(identity=user)
        # Return values and token
        data = {
            'id': str(user.id),
            'email': user.email,
            'access_token': access_token
        }

        return data, 200
    else:
        return 'Incorrect password', 401


# Register method
@auth.route('/register', methods=['POST'])
def register():
    user = UserModel.from_json(request.get_json())
    # Verify if the mail already exists in the db
    exists = db.session.query(UserModel).filter(UserModel.email == user.email).scalar() is not None
    if exists:
        return 'Duplicated mail', 409
    else:
        try:
            # Add user to the db
            db.session.add(user)
            db.session.commit()
            # Send welcome mail
            # sent = send_mail([user.email], "Welcome!", 'register', user=user)
        except Exception as error:
            db.session.rollback()
            return str(error), 409
        return user.to_json(), 201

