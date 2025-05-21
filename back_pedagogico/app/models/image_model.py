from app import db # Import the SQLAlchemy db instance from app/__init__.py
from datetime import datetime, timezone # For handling timestamps

class Image(db.Model):
    """
    Image model for storing image information related to a person.
    """
    __tablename__ = 'imagenes'  # Matches the table name in your schema

    # Columns according to your schema
    id_imagen = db.Column(db.Integer, primary_key=True)
    url_imagen = db.Column(db.String(255), nullable=False) # VARCHAR(32) in schema might be too short for full URLs
    descripcion = db.Column(db.Text, nullable=True) # TEXT(500) in schema

    # Foreign Key to link to the Person model
    # 'id_persona' in your 'Imágenes' table schema links to 'Personas.id_persona'
    id_persona = db.Column(db.Integer, db.ForeignKey('personas.id_persona'), nullable=False)

    # Timestamps (good practice, though not explicitly in your 'Imágenes' schema)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    # updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


    def __init__(self, url_imagen, id_persona, descripcion=None):
        self.url_imagen = url_imagen
        self.id_persona = id_persona
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
            'url_imagen': self.url_imagen,
            'descripcion': self.descripcion,
            'id_persona': self.id_persona,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
