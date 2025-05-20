from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

class Historia(db.Model):
    __tablename__ = 'historias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    soft_skill = db.Column(db.String(100))
    respuesta = db.Column(db.Text)
    foto = db.Column(db.String(255))  # Ruta relativa al archivo de foto

    def to_dict(self):
        # Comprobar si la foto existe físicamente en la carpeta assets
        foto_path = self.foto if self.foto else ""
        existe_foto = False
        if foto_path:
            # Obtener la ruta absoluta a la carpeta raíz del proyecto
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            full_path = os.path.join(base_dir, foto_path)
            existe_foto = os.path.isfile(full_path)
        return {
            "id": self.id,
            "nombre": self.nombre,
            "contenido": self.contenido,
            "soft_skill": self.soft_skill,
            "respuesta": self.respuesta,
            "foto": self.foto,
            "foto_existe": existe_foto  # Nuevo campo booleano
        }
