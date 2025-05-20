import os

# Determine the base directory of the application
# This is useful for setting up paths, e.g., for SQLite databases
basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
# __file__ -> app/core/config.py
# os.path.dirname(__file__) -> app/core
# os.path.dirname(os.path.dirname(__file__)) -> app
# os.path.dirname(os.path.dirname(os.path.dirname(__file__))) -> root project directory (back_pedagogico)


class Config:
    """
    Base configuration class. Contains common configuration settings.
    Subclasses will inherit from this and can override or add specific settings.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_hard_to_guess_string_CHANGE_ME' # IMPORTANT: Change this!
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add other common configurations here, e.g., mail server settings

    @staticmethod
    def init_app(app):
        """
        This method can be used to perform application-specific initializations
        that depend on the configuration.
        For example, setting up logging based on the environment.
        """
        pass


class DevelopmentConfig(Config):
    """
    Development specific configuration.
    Inherits from Config and overrides settings for development.
    """
    DEBUG = True
    # The print statement for debugging has been removed.
    
    # Use DEV_DATABASE_URL from environment, or fallback to your PyMySQL string.
    # Ensure your .env file correctly sets DEV_DATABASE_URL.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://root:111@127.0.0.1:3306/proyecto_pedagogico_db'


    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY_DEV') or 'jwt-secret-string-dev-CHANGE_ME' # IMPORTANT: Change this!


class TestingConfig(Config):
    """
    Testing specific configuration.
    Inherits from Config and overrides settings for testing.
    """
    TESTING = True
    DEBUG = True # Often useful to have debug true for testing
    # Use TEST_DATABASE_URL from environment, or fallback to a local SQLite file for tests.
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    
    WTF_CSRF_ENABLED = False # Often disabled for testing forms if you use Flask-WTF
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY_TEST') or 'jwt-secret-string-test-CHANGE_ME' # IMPORTANT: Change this!


class ProductionConfig(Config):
    """
    Production specific configuration.
    Inherits from Config and overrides settings for production.
    """
    DEBUG = False
    # Ensure you set a strong, environment-variable-based DATABASE_URL for production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI is None:
        # You might want to raise an error or log a warning if DATABASE_URL is not set in production
        print("WARNING: DATABASE_URL is not set for production environment!")
        # Or, for a hard fail:
        # raise ValueError("No DATABASE_URL set for production environment")

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY_PROD') # Should be set via environment variable and be very strong
    if JWT_SECRET_KEY is None:
        print("WARNING: JWT_SECRET_KEY_PROD is not set for production environment!")
        # Or, for a hard fail:
        # raise ValueError("No JWT_SECRET_KEY_PROD set for production environment")

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        # Example: Add production-specific logging, error handling, etc.
        # import logging
        # from logging.handlers import SysLogHandler
        # syslog_handler = SysLogHandler()
        # syslog_handler.setLevel(logging.WARNING)
        # app.logger.addHandler(syslog_handler)


# Dictionary to map configuration names to their respective classes
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig # Default configuration to use if FLASK_CONFIG is not set
}
