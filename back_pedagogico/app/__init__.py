from flask import Flask, jsonify
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
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    from .models.admin_user_model import AdminUser # Import here to avoid early import issues
    return AdminUser.query.get(int(identity))

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({
        'message': 'El token ha expirado.',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    return jsonify({
        'message': 'El token es inválido.',
        'error': 'invalid_token',
        'details': error_string
    }), 422

@jwt.unauthorized_loader
def missing_token_callback(error_string):
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
    """
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    with app.app_context():
        # Import all your models here
        from .models import admin_user_model, person_model, image_model, story_model, tag_model, story_translation_model

    migrate.init_app(app, db)

    # Import and register blueprints here, inside create_app
    from .api import bp as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    @app.route('/hello')
    def hello():
        return "Hello, World from Flask App Factory with Extensions and API Blueprint registered!"

    return app
