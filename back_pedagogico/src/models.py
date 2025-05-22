from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Administrador(db.Model):
    __tablename__ = 'administrador'
    __table_args__ = {'schema': 'proyecto-pedagogico'}
    id_admin = db.Column(db.Integer, primary_key=True)
    nombre_admin = db.Column(db.String(45), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    historias = db.relationship('Historia', back_populates='administrador')

class Etiqueta(db.Model):
    __tablename__ = 'etiquetas'
    __table_args__ = {'schema': 'proyecto-pedagogico'}
    etiqueta_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.TIMESTAMP)
    historias = db.relationship('HistoriasHasEtiquetas', back_populates='etiqueta')
    historias_principales = db.relationship('Historia', back_populates='etiqueta_principal', foreign_keys='Historia.etiqueta_id_principal')

class Persona(db.Model):
    __tablename__ = 'personas'
    __table_args__ = {'schema': 'proyecto-pedagogico'}
    id_persona = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    procedencia = db.Column(db.String(30), nullable=False)
    profesion = db.Column(db.String(45))
    fecha_nacimiento = db.Column(db.TIMESTAMP)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    historias = db.relationship('Historia', back_populates='persona')
    imagenes = db.relationship('Imagen', back_populates='persona')

class Historia(db.Model):
    __tablename__ = 'historias'
    __table_args__ = {'schema': 'proyecto-pedagogico'}
    id_historias = db.Column(db.Integer, primary_key=True)
    Personas_id_persona = db.Column(db.Integer, db.ForeignKey('proyecto-pedagogico.personas.id_persona'), nullable=False)
    Administrador_id_admin = db.Column(db.Integer, db.ForeignKey('proyecto-pedagogico.administrador.id_admin'), nullable=False)
    etiqueta_id_principal = db.Column(db.Integer, db.ForeignKey('proyecto-pedagogico.etiquetas.etiqueta_id'))
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

    persona = db.relationship('Persona', back_populates='historias')
    administrador = db.relationship('Administrador', back_populates='historias')
    etiqueta_principal = db.relationship('Etiqueta', back_populates='historias_principales', foreign_keys=[etiqueta_id_principal])
    traducciones = db.relationship('HistoriaTraduccion', back_populates='historia')
    etiquetas = db.relationship('HistoriasHasEtiquetas', back_populates='historia')

class HistoriaTraduccion(db.Model):
    __tablename__ = 'historias_traducciones'
    __table_args__ = {'schema': 'proyecto-pedagogico'}
    id_traduccion = db.Column(db.Integer, primary_key=True)
    historias_id_historias = db.Column(db.Integer, db.ForeignKey('proyecto-pedagogico.historias.id_historias'), nullable=False)
    codigo_idioma = db.Column(db.String(5), nullable=False)
    contenido_traducido = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

    historia = db.relationship('Historia', back_populates='traducciones')

class Imagen(db.Model):
    __tablename__ = 'imagenes'
    __table_args__ = {'schema': 'proyecto-pedagogico'}
    id_imagen = db.Column(db.Integer, primary_key=True)
    Personas_id_persona = db.Column(db.Integer, db.ForeignKey('proyecto-pedagogico.personas.id_persona'), nullable=False)
    url_imagen = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

    persona = db.relationship('Persona', back_populates='imagenes')

class HistoriasHasEtiquetas(db.Model):
    __tablename__ = 'historias_has_etiquetas'
    __table_args__ = (
        db.PrimaryKeyConstraint('historias_id_historias', 'etiquetas_etiqueta_id'),
        {'schema': 'proyecto-pedagogico'}
    )
    historias_id_historias = db.Column(db.Integer, db.ForeignKey('proyecto-pedagogico.historias.id_historias'), nullable=False)
    etiquetas_etiqueta_id = db.Column(db.Integer, db.ForeignKey('proyecto-pedagogico.etiquetas.etiqueta_id'), nullable=False)

    historia = db.relationship('Historia', back_populates='etiquetas')
    etiqueta = db.relationship('Etiqueta', back_populates='historias')
