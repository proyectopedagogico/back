from app import db 
from datetime import datetime, timezone 

class Person(db.Model):
    """
    Person model for storing information about the individuals
    whose life stories are being told.
    """
    __tablename__ = 'personas'  

    id_persona = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    procedencia = db.Column(db.String(30), nullable=True)
    profesion = db.Column(db.String(45), nullable=True) 
    fecha_nacimiento = db.Column(db.TIMESTAMP, nullable=True)

    # Relationships
    # A person can have many stories (one-to-many relationship with Stories)
    # 'historias' will be an attribute to access the stories of this person.
    # 'backref' creates a 'persona' attribute in the Story model to access this Person.
    historias = db.relationship('Story', backref='persona', lazy=True)
    
    # A person can have many images (one-to-many relationship with Images)
    # 'imagenes' will be an attribute to access the images of this person.
    # 'backref' creates a 'persona' attribute in the Image model to access this Person.
    imagenes = db.relationship('Image', backref='persona', lazy=True)

    # The columns Historias_id_historias and Imágenes_id_imagen in your Personas table
    # are a bit unusual. Normally, foreign keys would be in the 'many' tables
    # (Historias and Imágenes would point to Personas).
    # If the intention is for a Person to be directly linked to ONE main story
    # or ONE main image, the FK would be here. However, the column names
    # suggest they might be reverse FKs or misplaced in the diagram.
    # For now, we will model the relationships as described above (Person has many Stories/Images).
    # If you need a one-to-one relationship or a specific FK here, we can adjust it.


    def __init__(self, nombre, procedencia=None, profesion=None, fecha_nacimiento=None):
        self.nombre = nombre
        self.procedencia = procedencia
        self.profesion = profesion
        self.fecha_nacimiento = fecha_nacimiento

    def __repr__(self):
        return f'<Person {self.id_persona}: {self.nombre}>'

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
            'fecha_nacimiento': self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None
            # You could add stories and images here if you want to nest them,
            # but they are often handled with separate endpoints.
            # 'historias': [story.to_dict_summary() for story in self.historias], # Example
            # 'imagenes': [image.to_dict_summary() for image in self.imagenes]  # Example
        }
