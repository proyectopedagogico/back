# app/api/auth_routes.py

from flask import request, jsonify
from . import bp # Import the blueprint 'bp' from app/api/__init__.py
from app.models.admin_user_model import AdminUser # Import the AdminUser model
from app import db # Import the db instance from app/__init__.py
from flask_jwt_extended import create_access_token, jwt_required, get_jwt # For creating and managing JWTs
# bcrypt is used within the AdminUser model, so no direct import needed here for check_password

@bp.route('/admin/login', methods=['POST'])
def admin_login():
    """
    Authenticates an admin user and returns a JWT access token.
    Expects a JSON payload with 'username' (or 'email') and 'password'.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    username = data.get('username') # Or 'email', depending on your admin model
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    # Fetch the admin user from the database based on 'username'.
    # We use .first() because username should be unique.
    admin_user = AdminUser.query.filter_by(username=username).first()

    # If user doesn't exist or password doesn't match, return 401 Unauthorized.
    if not admin_user or not admin_user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    # If credentials are valid, create an access token.
    # The identity can be anything that uniquely identifies the user.
    # Flask-JWT-Extended expects the identity to be a string for the 'sub' claim.
    access_token = create_access_token(identity=str(admin_user.id)) # Convert admin_user.id to string
    
    return jsonify(access_token=access_token, message="Login successful"), 200


@bp.route('/admin/logout', methods=['POST'])
@jwt_required() # Protect this route, only logged-in users can logout
def admin_logout():
    """
    Logs out an admin user.
    This typically involves revoking a JWT token if you are using a denylist.
    For JWTs, "logout" often means the client just discards the token.
    If you implement token blocklisting, you'd add the token's JTI here.
    """
    # To implement true token revocation, you'd need a token blocklist (e.g., in Redis or a DB table)
    # and add the JTI (JWT ID) of the current token to it.
    # jti = get_jwt()['jti']
    # blocklist.add(jti) # Example if 'blocklist' is your revocation mechanism
    
    # For now, a simple success message is sufficient if not implementing full blocklisting.
    return jsonify({"message": "Logout successful. Please discard your token."}), 200

# Further JWT configuration might be needed in app/__init__.py or a dedicated auth setup:
# - @jwt.user_lookup_loader: To load the user object from the token's identity.
# - @jwt.expired_token_loader: To customize response for expired tokens.
# - @jwt.invalid_token_loader: To customize response for invalid tokens.
# - @jwt.unauthorized_loader: To customize response when no token is present.
