from app import db # Import the SQLAlchemy db instance from app/__init__.py
from datetime import datetime, timezone # For handling timestamps

# Association table for the many-to-many relationship between Stories and Tags
# This table does not need its own Python model class if it only contains foreign keys.
story_tags_table = db.Table('story_tags',
    db.Column('story_id', db.Integer, db.ForeignKey('historias.id_historias'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    # Assuming the Tag model's table is named 'tags' and its primary key is 'id'
)

class Story(db.Model):
    """
    Story model for storing life stories, aligned with the provided database schema,
    and including a many-to-many relationship with Tags.
    """
    __tablename__ = 'historias'  # Matches the table name in your schema

    id_historias = db.Column(db.Integer, primary_key=True) # PK, matches 'id_historias'
    contenido = db.Column(db.Text, nullable=False) # Matches 'contenido VARCHAR(500)', using Text for flexibility
    
    # Foreign Key to link to the Person model
    id_persona = db.Column(db.Integer, db.ForeignKey('personas.id_persona'), nullable=False)
    
    # Foreign Key to link to the AdminUser model
    administrador_id_admin = db.Column(db.Integer, db.ForeignKey('admin_users.id'), nullable=False)

    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationship to AdminUser
    admin_manager = db.relationship('AdminUser', backref=db.backref('managed_stories', lazy='dynamic'))
    
    # Relationship to Tags (many-to-many)
    # 'tags' will be a list-like attribute to access/manage the tags for this story.
    # 'secondary' points to our association table.
    # 'backref' creates 'stories' attribute in the Tag model.
    tags = db.relationship('Tag', secondary=story_tags_table,
                        lazy='subquery', # or 'dynamic' or True (select)
                        backref=db.backref('stories', lazy=True))
    
    # The relationship to Person is already defined in the Person model via backref='persona'.
    # So, you can access the person of a story via 'una_historia.persona'.

    def __init__(self, contenido, id_persona, administrador_id_admin): # Removed etiqueta_id from constructor
        self.contenido = contenido
        self.id_persona = id_persona
        self.administrador_id_admin = administrador_id_admin
        # Tags will be added to the 'self.tags' collection after the Story object is created and committed.

    def __repr__(self):
        return f'<Story {self.id_historias}>'

    def to_dict(self):
        """
        Serializes the Story object to a dictionary.
        Useful for API responses.
        """
        # Import Tag model here to avoid circular import if Tag model also has a to_dict
        from .tag_model import Tag 

        return {
            'id_historias': self.id_historias,
            'contenido': self.contenido,
            'id_persona': self.id_persona,
            'nombre_persona': self.persona.nombre if self.persona else None,
            'administrador_id_admin': self.administrador_id_admin,
            'tags': [tag.to_dict() for tag in self.tags] if self.tags else [], # Serialize associated tags
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
