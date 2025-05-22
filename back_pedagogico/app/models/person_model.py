from app import db # Import the SQLAlchemy db instance from app/__init__.py
from datetime import datetime, timezone # For handling timestamps

class Person(db.Model):
    """
    Person model for storing information about the individuals
    whose life stories are being told, aligned with the final database schema.
    """
    __tablename__ = 'personas'  # Matches the table name in your SQL schema

    # Columns according to your final SQL schema
    id_persona = db.Column(db.Integer, primary_key=True) # AUTO_INCREMENT is default for Integer PK
    nombre = db.Column(db.String(50), nullable=True) # VARCHAR(50) NULL DEFAULT NULL
    procedencia = db.Column(db.String(30), nullable=False) # VARCHAR(30) NOT NULL
    profesion = db.Column(db.String(45), nullable=True) # VARCHAR(45) NULL DEFAULT NULL
    fecha_nacimiento = db.Column(db.TIMESTAMP, nullable=True) # TIMESTAMP NULL DEFAULT NULL
    
    # Timestamps as per SQL schema
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    # A person can have many stories (one-to-many relationship with Stories)
    # 'historias' will be an attribute to access the stories of this person.
    # 'backref' creates a 'persona' attribute in the Story model to access this Person.
    # This aligns with 'Personas_id_persona' FK in the 'historias' table.
    historias = db.relationship('Story', foreign_keys='Story.Personas_id_persona', backref='persona', lazy='dynamic')
    
    # A person can have many images (one-to-many relationship with Images)
    # 'imagenes' will be an attribute to access the images of this person.
    # 'backref' creates a 'persona' attribute in the Image model to access this Person.
    # This aligns with 'Personas_id_persona' FK in the 'imagenes' table.
    imagenes = db.relationship('Image', foreign_keys='Image.personas_id_persona', backref='persona_imagenes', lazy='dynamic') # Changed backref name to avoid conflict if 'persona' is used in Image for other purposes

    def __init__(self, procedencia, nombre=None, profesion=None, fecha_nacimiento=None): # Adjusted for nullable fields and mandatory procedencia
        self.nombre = nombre
        self.procedencia = procedencia # procedencia is NOT NULL in schema
        self.profesion = profesion
        self.fecha_nacimiento = fecha_nacimiento

    def __repr__(self):
        return f'<Person {self.id_persona}: {self.nombre or "Sin nombre"}>'

    def to_dict(self):
        """
        Serializes the Person object to a dictionary.
        Useful for API responses.
        """
        return {
            'id_persona': self.id_persona,
            'nombre': self.nombre,
            'procedencia': self.procedencia,
            'profesion': self.profesion,
            'fecha_nacimiento': self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }