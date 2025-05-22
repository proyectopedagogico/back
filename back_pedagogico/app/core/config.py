import os

# Determine the base directory of the application
basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class Config:
    """
    Base configuration class. Contains common configuration settings.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_hard_to_guess_string_CHANGE_ME' # IMPORTANT: Change this!
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration for File Uploads
    # It's good practice to place the upload folder outside the app package,
    # but for simplicity in a pedagogical project, it can be within instance or static.
    # Or, ideally, at the root of the project or a dedicated media root.
    # We'll define it relative to the project's base directory.
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads') # Creates an 'uploads' folder in your project root
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size (example)


    @staticmethod
    def init_app(app):
        """
        This method can be used to perform application-specific initializations
        that depend on the configuration.
        """
        # Create the upload folder if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
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
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    
    WTF_CSRF_ENABLED = False 
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY_TEST') or 'jwt-secret-string-test-CHANGE_ME' # IMPORTANT: Change this!
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads_test') # Separate upload folder for tests


class ProductionConfig(Config):
    """
    Production specific configuration.
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI is None:
        print("WARNING: DATABASE_URL is not set for production environment!")

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY_PROD') 
    if JWT_SECRET_KEY is None:
        print("WARNING: JWT_SECRET_KEY_PROD is not set for production environment!")

    # UPLOAD_FOLDER for production might point to a persistent storage or a configured volume
    # UPLOAD_FOLDER = os.environ.get('PROD_UPLOAD_FOLDER') or os.path.join(basedir, 'uploads_prod')


    @classmethod
    def init_app(cls, app):
        Config.init_app(app) # Call base class init_app
        # Create the upload folder for production if it doesn't exist and UPLOAD_FOLDER is defined
        # This might be handled by deployment scripts in a real production environment
        upload_folder_prod = app.config.get('UPLOAD_FOLDER')
        if upload_folder_prod and not os.path.exists(upload_folder_prod):
             try:
                os.makedirs(upload_folder_prod)
             except OSError as e:
                app.logger.error(f"Could not create production upload folder {upload_folder_prod}: {e}")


# Dictionary to map configuration names to their respective classes
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig 
}