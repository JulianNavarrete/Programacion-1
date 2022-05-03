from .. import jwt
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps


# Decorator to restrict access to admin users
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Verify if the JWT is correct
        verify_jwt_in_request()
        # Get the claims inside the JWT
        claims = get_jwt()
        # Verify if the user is an admin
        if claims['role'] == "admin":
            # Run function
            return fn(*args, **kwargs)
        else:
            return 'Only admins can access', 403

    return wrapper


# Defines the attribute that will be used to identify the user
@jwt.user_identity_loader
def user_identity_lookup(user):
    # Define ID as identification attribute
    return user.id


# Defines the attributes that will be stored in the token
@jwt.additional_claims_loader
def add_claims_to_access_token(user):
    claims = {
        'role': user.role,
        'id': user.id,
        'email': user.email
    }
    return claims

