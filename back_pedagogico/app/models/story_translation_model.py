from app import db
from datetime import datetime, timezone

class StoryTranslation(db.Model):
    """
    Model for storing translations of story content.
    """
    __tablename__ = 'historias_traducciones'

    id_traduccion = db.Column(db.Integer, primary_key=True) # AUTO_INCREMENT is default
    historias_id_historias = db.Column(db.Integer, db.ForeignKey('historias.id_historias', ondelete='CASCADE'), nullable=False)
    codigo_idioma = db.Column(db.String(5), nullable=False)  # e.g., 'es', 'en', 'eu'
    contenido_traducido = db.Column(db.Text, nullable=False)
    # If you decide to have translatable titles for stories:
    # titulo_traducido = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Unique constraint for (historias_id_historias, codigo_idioma)
    __table_args__ = (db.UniqueConstraint('historias_id_historias', 'codigo_idioma', name='uq_historia_idioma'),)

    def __init__(self, historias_id_historias, codigo_idioma, contenido_traducido): #, titulo_traducido=None):
        self.historias_id_historias = historias_id_historias
        self.codigo_idioma = codigo_idioma
        self.contenido_traducido = contenido_traducido
        # self.titulo_traducido = titulo_traducido

    def __repr__(self):
        return f'<StoryTranslation {self.id_traduccion} for Story {self.historias_id_historias} [{self.codigo_idioma}]>'

    def to_dict(self):
        return {
            'id_traduccion': self.id_traduccion,
            'historias_id_historias': self.historias_id_historias,
            'codigo_idioma': self.codigo_idioma,
            'contenido_traducido': self.contenido_traducido,
            # 'titulo_traducido': self.titulo_traducido,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }