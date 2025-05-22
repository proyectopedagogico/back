# app/api/auth_routes.py

from flask import request, jsonify
from . import bp # Import the blueprint 'bp' from app/api/__init__.py
from app.models.admin_user_model import AdminUser # Import the AdminUser model
# Ensure db is available if needed for direct operations,
# though AdminUser.query already uses it.
# from app import db 
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

@bp.route('/admin/login', methods=['POST'])
def admin_login():
    """
    Authenticates an admin user and returns a JWT access token.
    Expects a JSON payload with 'nombre_admin' and 'password'.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400 # English error message

    # Use 'nombre_admin' to match the AdminUser model and the expected payload
    nombre_admin_from_request = data.get('nombre_admin') 
    password = data.get('password')

    # Debug prints
    print(f"DEBUG: Received nombre_admin: {nombre_admin_from_request}")
    print(f"DEBUG: Received password (length): {len(password) if password else 0}") # Print length for security

    if not nombre_admin_from_request or not password:
        print("DEBUG: Missing nombre_admin or password in request.")
        return jsonify({"error": "Missing nombre_admin or password."}), 400 # English error message

    # Fetch the admin user from the database by 'nombre_admin'.
    # Renamed variable to 'admin_user' for clarity.
    admin_user = AdminUser.query.filter_by(nombre_admin=nombre_admin_from_request).first()

    if admin_user:
        print(f"DEBUG: User found in DB: {admin_user.nombre_admin}")
        print(f"DEBUG: Stored password_hash (first 10 chars): {admin_user.password_hash[:10] if admin_user.password_hash else 'None'}")
        password_matches = admin_user.check_password(password)
        print(f"DEBUG: Password check result: {password_matches}")
    else:
        print(f"DEBUG: User NOT found in DB with nombre_admin: {nombre_admin_from_request}")

    # If user doesn't exist or password doesn't match, return 401 Unauthorized.
    if not admin_user or not admin_user.check_password(password): # check_password will be called again, but it's okay for debugging
        print("DEBUG: Invalid credentials condition met.")
        return jsonify({"error": "Invalid credentials."}), 401 # English error message

    # If credentials are valid, create an access token.
    # Use admin_user.id_admin (or the correct PK from your AdminUser model) and convert it to string.
    print(f"DEBUG: Credentials valid. Creating token for admin ID: {admin_user.id_admin}")
    access_token = create_access_token(identity=str(admin_user.id_admin)) 
    
    return jsonify(access_token=access_token, message="Login successful"), 200 # English message


@bp.route('/admin/logout', methods=['POST'])
@jwt_required() # Protect this route, only logged-in users can logout
def admin_logout():
    """
    Logs out an admin user.
    This typically involves revoking a JWT if using a denylist.
    For JWTs, "logout" often means the client simply discards the token.
    If implementing token blocklisting, you would add the token's JTI here.
    """
    # To implement true token revocation, you would need a token blocklist
    # (e.g., in Redis or a DB table) and add the JTI (JWT ID) of the current token to it.
    # jti = get_jwt()['jti']
    # blocklist.add(jti) # Example if 'blocklist' is your revocation mechanism
    
    # For now, a simple success message is sufficient if not implementing full blocklisting.
    return jsonify({"message": "Logout successful. Please discard your token."}), 200 # English message

# Additional JWT configurations might be needed in app/__init__.py or a dedicated auth setup file:
# - @jwt.user_lookup_loader: To load the user object from the token's identity.
# - @jwt.expired_token_loader: To customize the response for expired tokens.
# - @jwt.invalid_token_loader: To customize the response for invalid tokens.
# - @jwt.unauthorized_loader: To customize the response when no token is present.