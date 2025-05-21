from app import db # Import the SQLAlchemy db instance from app/__init__.py
from datetime import datetime, timezone # For handling timestamps

# Association table for the many-to-many relationship between Stories and Tags
# Name and foreign keys updated to match the new schema: 'historias_has_etiquetas'
historias_has_etiquetas_table = db.Table('historias_has_etiquetas',
    db.Column('historias_id_historias', db.Integer, db.ForeignKey('historias.id_historias'), primary_key=True),
    db.Column('etiquetas_etiqueta_id', db.Integer, db.ForeignKey('etiquetas.etiqueta_id'), primary_key=True)
)

class Story(db.Model):
    """
    Story model for storing life stories, aligned with the new database schema,
    and including a many-to-many relationship with Tags.
    """
    __tablename__ = 'historias'  # Matches the table name in your new schema

    id_historias = db.Column(db.Integer, primary_key=True) # PK, matches 'id_historias'
    contenido = db.Column(db.String(500), nullable=False) # Matches 'contenido VARCHAR(500)'
    
    # Foreign Key to link to the Person model
    # Matches 'id_persona INT(11)' or 'Personas_id_persona INT(11)' in your 'historias' table.
    # We'll use 'id_persona' as the column name in the model for simplicity and consistency.
    id_persona = db.Column(db.Integer, db.ForeignKey('personas.id_persona'), nullable=False)
    
    # Foreign Key to link to the AdminUser model
    # Matches 'Administrador_id_admin INT(11)' in your 'historias' table
    administrador_id_admin = db.Column(db.Integer, db.ForeignKey('admin_users.id'), nullable=False)

    # The 'etiqueta_id INT(10)' column directly in the 'historias' table from your new schema
    # is omitted here because we are implementing a many-to-many relationship for tags
    # via the 'historias_has_etiquetas' table. If this direct 'etiqueta_id' has a different
    # purpose (e.g., a single primary tag), it would need to be added back.

    # Timestamps (good practice, can be kept or removed if not in schema)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationship to AdminUser
    admin_manager = db.relationship('AdminUser', backref=db.backref('managed_stories', lazy='dynamic'))
    
    # Relationship to Tags (many-to-many) using the 'historias_has_etiquetas_table'
    tags = db.relationship('Tag', secondary=historias_has_etiquetas_table,
                           lazy='subquery',
                           backref=db.backref('stories', lazy=True))
    
    # The relationship to Person is already defined in the Person model via backref='persona'.
    # So, you can access the person of a story via 'una_historia.persona'.

    def __init__(self, contenido, id_persona, administrador_id_admin):
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
        from .tag_model import Tag # Local import to avoid circular dependency issues

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