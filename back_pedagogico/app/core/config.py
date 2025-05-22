import os
import logging # For logging errors in production config

# Determine the base directory of the application
basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class Config:
    """
    Base configuration class. Contains common configuration settings.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_hard_to_guess_string_CHANGE_ME' # IMPORTANT: Change this!
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration for File Uploads
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads') 
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size (example)


    @staticmethod
    def init_app(app):
        """
        This method can be used to perform application-specific initializations
        that depend on the configuration.
        """
        # Create the upload folder if it doesn't exist for the current config
        current_upload_folder = app.config.get('UPLOAD_FOLDER')
        if current_upload_folder and not os.path.exists(current_upload_folder):
            try:
                os.makedirs(current_upload_folder)
                app.logger.info(f"Upload folder created at: {current_upload_folder}")
            except OSError as e:
                app.logger.error(f"Could not create upload folder {current_upload_folder}: {e}")
        pass


class DevelopmentConfig(Config):
    """
    Development specific configuration.
    """
    DEBUG = True
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://root:111@127.0.0.1:3306/proyecto_pedagogico_db' # Using PyMySQL as per previous setup

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY_DEV') or 'jwt-secret-string-dev-CHANGE_ME' # IMPORTANT: Change this!


class TestingConfig(Config):
    """
    Testing specific configuration.
    """
    TESTING = True
    DEBUG = True 
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite') # Default to SQLite for tests
    
    WTF_CSRF_ENABLED = False 
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY_TEST') or 'jwt-secret-string-test-CHANGE_ME' # IMPORTANT: Change this!
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads_test') # Separate upload folder for tests


class ProductionConfig(Config):
    """
    Production specific configuration.
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY_PROD') 
    
    # Define UPLOAD_FOLDER specifically for production
    UPLOAD_FOLDER = os.environ.get('PROD_UPLOAD_FOLDER') or os.path.join(basedir, 'uploads_prod')


    @classmethod
    def init_app(cls, app):
        Config.init_app(app) # Call base class init_app to create the folder if needed

        # Checks for essential production configurations
        if not app.config.get('SQLALCHEMY_DATABASE_URI'):
            app.logger.critical("CRITICAL: DATABASE_URL is not set for production environment!")
            # Consider raising an error to prevent app startup without DB URL in production
            # raise ValueError("DATABASE_URL must be set in production.")

        if not app.config.get('JWT_SECRET_KEY'): # SECRET_KEY is inherited, JWT_SECRET_KEY is specific
            app.logger.critical("CRITICAL: JWT_SECRET_KEY_PROD is not set for production environment!")
            # Consider raising an error
            # raise ValueError("JWT_SECRET_KEY_PROD must be set in production.")
        
        # The base Config.init_app will handle creating the UPLOAD_FOLDER
        # defined in this ProductionConfig class.


# Dictionary to map configuration names to their respective classes
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig 
}
