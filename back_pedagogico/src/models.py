from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Administrador(db.Model):
    __tablename__ = 'administrador'
    __table_args__ = {'schema': 'mydb'}
    id_admin = db.Column(db.Integer, primary_key=True)
    nombre_admin = db.Column(db.String(45))
    password = db.Column(db.String(50), nullable=False)
    historias = db.relationship('Historia', backref='administrador', lazy=True)

class Imagen(db.Model):
    __tablename__ = 'imagenes'
    __table_args__ = {'schema': 'mydb'}
    id_imagen = db.Column(db.Integer, primary_key=True)
    url_imagen = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)

class Historia(db.Model):
    __tablename__ = 'historias'
    __table_args__ = {'schema': 'mydb'}
    id_historias = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.String(500), nullable=False)
    administrador_id_admin = db.Column(db.Integer, db.ForeignKey('mydb.administrador.id_admin'), nullable=False)
    etiquetas = db.relationship('Etiqueta', secondary='mydb.historias_etiquetas', backref='historias', lazy='dynamic')

class Etiqueta(db.Model):
    __tablename__ = 'etiquetas'
    __table_args__ = {'schema': 'mydb'}
    id_etiqueta = db.Column(db.Integer, primary_key=True)
    nombre_etiqueta = db.Column(db.String(100), nullable=False)

class HistoriasEtiquetas(db.Model):
    __tablename__ = 'historias_etiquetas'
    __table_args__ = {'schema': 'mydb'}
    id_historias = db.Column(db.Integer, db.ForeignKey('mydb.historias.id_historias'), primary_key=True)
    id_etiqueta = db.Column(db.Integer, db.ForeignKey('mydb.etiquetas.id_etiqueta'), primary_key=True)

class Persona(db.Model):
    __tablename__ = 'personas'
    __table_args__ = {'schema': 'mydb'}
    id_persona = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    procedencia = db.Column(db.String(30), nullable=False)
    profesion = db.Column(db.String(45))
    fecha_nacimiento = db.Column(db.Date)
    id_imagen = db.Column(db.Integer, db.ForeignKey('mydb.imagenes.id_imagen'))
