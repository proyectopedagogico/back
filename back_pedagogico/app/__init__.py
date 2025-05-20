from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from .core.config import config
# NOTE: The API blueprint import is now moved into the create_app function below.

# Initialize Flask extensions globally
# These will be bound to a specific app instance in the create_app factory
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
# CORS will be initialized directly in create_app

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
    jwt.init_app(app)
    CORS(app) # Initialize CORS with default settings

    # IMPORTANT: Import models AFTER db has been initialized with the app
    # and BEFORE migrate is initialized with the app and db.
    # This ensures that db.Model is correctly configured when models are defined.
    with app.app_context():
        # Importing models within an app_context can sometimes help ensure
        # they are correctly associated with the application, especially for extensions.
        from .models import admin_user_model # Ensure this is the correct module name
        # If you have other models, import them here as well:
        # from .models import story_model

    # Initialize Flask-Migrate after models are imported and known to db.metadata
    migrate.init_app(app, db)

    # Register Blueprints AFTER app and extensions are initialized.
    # Import blueprints here, inside create_app, to avoid circular dependencies at module level.
    from .api import bp as api_blueprint # MOVED HERE
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Example for a simple main blueprint (if you had one for non-API routes)
    # from .main import main as main_blueprint # Import and register other blueprints similarly
    # app.register_blueprint(main_blueprint)

    @app.route('/hello')
    def hello():
        return "Hello, World from Flask App Factory with Extensions and API Blueprint registered!"

    return app