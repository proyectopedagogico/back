from app import db # Import the SQLAlchemy db instance from app/__init__.py
from datetime import datetime, timezone # For handling timestamps

class Image(db.Model):
    """
    Image model for storing image information related to a person,
    aligned with the final database schema.
    """
    __tablename__ = 'imagenes'  # Matches the table name in your SQL schema

    # Columns according to your final SQL schema
    id_imagen = db.Column(db.Integer, primary_key=True) # AUTO_INCREMENT is default for Integer PK
    
    # Foreign Key to link to the Person model
    # Matches 'Personas_id_persona INT(11) NOT NULL' in your 'imagenes' table.
    personas_id_persona = db.Column(db.Integer, db.ForeignKey('personas.id_persona'), nullable=False)
    
    url_imagen = db.Column(db.String(255), nullable=False) # VARCHAR(255) NOT NULL
    descripcion = db.Column(db.Text, nullable=True) # TEXT NULL DEFAULT NULL
    
    # Timestamps as per SQL schema
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # The relationship to Person ('persona_imagenes') is defined by the backref
    # in the Person model:
    # In Person model: imagenes = db.relationship('Image', foreign_keys='Image.personas_id_persona', backref='persona_imagenes', lazy='dynamic')
    # This allows you to access the person via an_image_instance.persona_imagenes

    def __init__(self, url_imagen, personas_id_persona, descripcion=None):
        self.url_imagen = url_imagen
        self.personas_id_persona = personas_id_persona
        self.descripcion = descripcion

    def __repr__(self):
        return f'<Image {self.id_imagen}: {self.url_imagen}>'

    def to_dict(self):
        """
        Serializes the Image object to a dictionary.
        Useful for API responses.
        """
        return {
            'id_imagen': self.id_imagen,
            'personas_id_persona': self.personas_id_persona,
            'url_imagen': self.url_imagen,
            'descripcion': self.descripcion,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }