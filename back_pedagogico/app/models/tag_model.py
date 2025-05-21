from app import db # Import the SQLAlchemy db instance from app/__init__.py
from datetime import datetime, timezone # For handling timestamps

class Tag(db.Model):
    """
    Tag model for categorizing stories, aligned with the new database schema.
    """
    __tablename__ = 'etiquetas' # Table name from the new schema

    etiqueta_id = db.Column(db.Integer, primary_key=True) # Primary key, matches 'etiqueta_id'
    name = db.Column(db.String(50), unique=True, nullable=False) # Matches 'name VARCHAR(50)'
    
    # Timestamps (good practice, can be kept or removed if not in schema)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    # The relationship to stories will be defined via the association table
    # ('historias_has_etiquetas' in the new schema)
    # and the 'backref' in the Story model's 'tags' relationship.

    def __init__(self, name): # Constructor uses the 'name' field
        self.name = name

    def __repr__(self):
        return f'<Tag {self.etiqueta_id}: {self.name}>' # Uses 'etiqueta_id' and 'name'

    def to_dict(self):
        """
        Serializes the Tag object to a dictionary.
        """
        return {
            'etiqueta_id': self.etiqueta_id, # Changed 'id' to 'etiqueta_id'
            'name': self.name,             # Changed 'nombre' to 'name'
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
