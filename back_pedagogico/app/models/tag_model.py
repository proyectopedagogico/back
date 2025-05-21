from app import db 
from datetime import datetime, timezone 

class Tag(db.Model):
    """
    Tag model for categorizing stories.
    """
    __tablename__ = 'tags' # Define the table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False) # Tag name, e.g., "Superación", "Emprendimiento"
    
    # Timestamps (good practice)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    # The relationship to stories will be defined via the association table
    # and the 'backref' in the Story model's 'tags' relationship.

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Tag {self.id}: {self.name}>'

    def to_dict(self):
        """
        Serializes the Tag object to a dictionary.
        """
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
