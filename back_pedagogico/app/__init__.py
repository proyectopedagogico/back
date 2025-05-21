from flask import Flask, jsonify # Added jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from .core.config import config
# NOTE: The API blueprint import is now moved into the create_app function below.

# Initialize Flask extensions globally
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager() # Initialize JWTManager instance globally
# CORS will be initialized directly in create_app

# --- JWT Configuration Callbacks ---
# These functions are decorated with callbacks from the 'jwt' instance.
# They tell Flask-JWT-Extended how to behave in certain situations.

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
    This function is called whenever a protected endpoint is accessed,
    and will return the user object or None if the user does not exist.
    """
    identity = jwt_data["sub"] # 'sub' is the default claim for identity
    # Assuming identity is the user ID (which we set as a string)
    # Import AdminUser here to avoid circular imports at module level if AdminUser imports db
    from .models.admin_user_model import AdminUser
    return AdminUser.query.get(int(identity)) # Convert identity back to int for DB query

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    """
    Callback for when an expired JWT is encountered.
    """
    return jsonify({
        'message': 'El token ha expirado.',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    """
    Callback for when an invalid JWT is encountered (e.g., malformed).
    """
    return jsonify({
        'message': 'El token es inválido.',
        'error': 'invalid_token',
        'details': error_string
    }), 422 # Unprocessable Entity is often used for invalid tokens

@jwt.unauthorized_loader
def missing_token_callback(error_string):
    """
    Callback for when a JWT is required but not found.
    """
    return jsonify({
        'message': 'Se requiere un token de acceso.',
        'error': 'authorization_required',
        'details': error_string
    }), 401

# --- End of JWT Configuration Callbacks ---


# Application Factory Function
def create_app(config_name):
    """
    Creates and configures an instance of the Flask application.

    Args:
        config_name (str): The name of the configuration to use (e.g., 'development', 'production').

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    # Load configuration from the config object
    app.config.from_object(config[config_name])
    config[config_name].init_app(app) # Initialize the configuration for the app

    # Initialize Flask extensions with the app instance
    db.init_app(app)
    jwt.init_app(app) # Associate the jwt instance with the app
    CORS(app) # Initialize CORS with default settings

    with app.app_context():
        from .models import admin_user_model

    migrate.init_app(app, db)

    from .api import bp as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    @app.route('/hello')
    def hello():
        return "Hello, World from Flask App Factory with Extensions and API Blueprint registered!"

    return app