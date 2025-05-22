from .. import db # Import the SQLAlchemy db instance from the parent package (app/__init__.py)
import bcrypt # For password hashing

class AdminUser(db.Model):
    """
    AdminUser model for storing administrator credentials,
    aligned with the final database schema.
    """
    __tablename__ = 'administrador' # Matches the table name in your SQL schema

    id_admin = db.Column(db.Integer, primary_key=True) # AUTO_INCREMENT is default for Integer PK
    nombre_admin = db.Column(db.String(45), unique=True, nullable=True) # Matches SQL schema (NULL DEFAULT NULL)
    
    # Using password_hash to store hashed passwords securely.
    password_hash = db.Column(db.String(128), nullable=False) # Matches SQL schema

    def __init__(self, nombre_admin, password):
        """
        Constructor for the AdminUser model.
        Hashes the password upon creation.
        """
        self.nombre_admin = nombre_admin
        self.set_password(password)

    def set_password(self, password):
        """
        Hashes the provided password and stores it.
        """
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """
        Checks if the provided password matches the stored hashed password.
        """
        if self.password_hash: # Ensure there is a hash to check against
            return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
        return False

    def __repr__(self):
        return f'<AdminUser {self.nombre_admin}>'

    def to_dict(self):
        """
        Serializes the AdminUser object to a dictionary.
        """
        return {
            'id_admin': self.id_admin,
            'nombre_admin': self.nombre_admin
            # IMPORTANT: Never return password_hash
        }