from .. import db # Import the SQLAlchemy db instance from the parent package (app/__init__.py)
import bcrypt # For password hashing

class AdminUser(db.Model):
    """
    AdminUser model for storing administrator credentials.
    """
    __tablename__ = 'admin_users' # Optional: specify the table name

    id = db.Column(db.Integer, primary_key=True)
    # You can choose to use 'username' or 'email' as the primary identifier for login
    username = db.Column(db.String(80), unique=True, nullable=False)
    # email = db.Column(db.String(120), unique=True, nullable=False) # Alternative/additional
    password_hash = db.Column(db.String(128), nullable=False) # Store hashed passwords

    def __init__(self, username, password):
        """
        Constructor for the AdminUser model.
        Hashes the password upon creation.
        """
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        """
        Hashes the provided password and stores it.
        """
        # Generate a salt and hash the password
        # bcrypt.gensalt() returns bytes, so decode to utf-8 if storing as string
        # password.encode('utf-8') ensures the password is bytes before hashing
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """
        Checks if the provided password matches the stored hashed password.
        """
        # password.encode('utf-8') ensures the input password is bytes
        # self.password_hash.encode('utf-8') ensures the stored hash is bytes
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __repr__(self):
        return f'<AdminUser {self.username}>'

    # If you need to serialize this model to JSON for API responses (e.g., user profile)
    # you might add a to_dict() method, though for admin login, you usually just return a token.
    # def to_dict(self):
    #     return {
    #         'id': self.id,
    #         'username': self.username
    #         # IMPORTANT: Never return password_hash
    #     }
