from app import db
from datetime import datetime, timezone

# Association table for the many-to-many relationship between Stories and Tags
# Aligned with the 'historias_has_etiquetas' table from the final SQL schema.
historias_has_etiquetas_table = db.Table('historias_has_etiquetas',
    db.Column('historias_id_historias', db.Integer, db.ForeignKey('historias.id_historias', ondelete='CASCADE'), primary_key=True),
    db.Column('etiquetas_etiqueta_id', db.Integer, db.ForeignKey('etiquetas.etiqueta_id', ondelete='CASCADE'), primary_key=True)
)

class Story(db.Model):
    """
    Story model for storing life stories, aligned with the final database schema.
    Content is now handled via the StoryTranslation model.
    """
    __tablename__ = 'historias'

    id_historias = db.Column(db.Integer, primary_key=True) # AUTO_INCREMENT is default
    Personas_id_persona = db.Column(db.Integer, db.ForeignKey('personas.id_persona', ondelete='CASCADE'), nullable=False)
    Administrador_id_admin = db.Column(db.Integer, db.ForeignKey('administrador.id_admin', ondelete='RESTRICT'), nullable=False)
    etiqueta_id_principal = db.Column(db.Integer, db.ForeignKey('etiquetas.etiqueta_id', ondelete='SET NULL'), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # --- Relationships ---
    # Relationship to AdminUser
    # The 'admin_manager' attribute allows access to the AdminUser object from a Story instance.
    # 'backref' creates 'managed_stories' attribute in the AdminUser model.
    admin_manager = db.relationship('AdminUser', foreign_keys=[Administrador_id_admin], backref=db.backref('managed_stories', lazy='dynamic'))
    
    # Relationship to Person (defined by Personas_id_persona)
    # The 'persona' attribute is created by the backref in the Person model.
    # Ensure Person model has: historias = db.relationship('Story', foreign_keys='Story.Personas_id_persona', backref='persona', lazy='dynamic')
    # (This is already in the Canvas flask_person_model_py_final)

    # Relationship to Tags (many-to-many)
    # The 'tags' attribute allows access to a list of Tag objects associated with this story.
    # 'secondary' points to our association table 'historias_has_etiquetas_table'.
    # 'backref' creates 'stories' attribute in the Tag model.
    tags = db.relationship('Tag', secondary=historias_has_etiquetas_table,
                           backref=db.backref('stories', lazy='dynamic'),
                           lazy='dynamic') # 'dynamic' is good for collections that can be large
    
    # Relationship for the direct 'etiqueta_id_principal' (one "primary" tag)
    # The 'primary_tag' attribute allows access to the Tag object for the principal tag.
    # 'backref' creates 'primary_tagged_stories' attribute in the Tag model.
    primary_tag = db.relationship('Tag', foreign_keys=[etiqueta_id_principal], backref=db.backref('primary_tagged_stories', lazy='select')) # 'select' (or default True) is often fine for one-to-one/many-to-one

    # Relationship to StoryTranslations (one-to-many)
    # The 'translations' attribute allows access to a list of StoryTranslation objects for this story.
    # 'cascade="all, delete-orphan"' ensures that if a story is deleted, its translations are also deleted.
    translations = db.relationship('StoryTranslation', backref='story', lazy='dynamic', cascade="all, delete-orphan")


    def __init__(self, Personas_id_persona, Administrador_id_admin, etiqueta_id_principal=None):
        # Content is no longer initialized here directly; it's handled by StoryTranslation.
        self.Personas_id_persona = Personas_id_persona
        self.Administrador_id_admin = Administrador_id_admin
        self.etiqueta_id_principal = etiqueta_id_principal
        # Tags (many-to-many) and translations are handled via their respective collections/relationships
        # after the Story object is created and committed.

    def __repr__(self):
        return f'<Story ID:{self.id_historias} by Person ID:{self.Personas_id_persona}>'

    def get_translated_content(self, language_code):
        """
        Helper method to get content in a specific language from its translations.
        Returns None if no translation is found for the given language code.
        """
        if not self.translations: # Check if the relationship query is None or empty
            return None
        translation = self.translations.filter_by(codigo_idioma=language_code).first()
        return translation.contenido_traducido if translation else None

    def to_dict(self, language_code='es'): # Default to Spanish or your primary language
        """
        Serializes the Story object to a dictionary, including content in the specified language.
        """
        # Local import of Tag and StoryTranslation to avoid potential circular import issues
        # if those models also had to_dict methods calling back to Story.
        from .tag_model import Tag 
        from .story_translation_model import StoryTranslation

        content_for_lang = self.get_translated_content(language_code)
        # You might want a fallback if content for the requested language is not found
        # e.g., content_for_lang = content_for_lang or self.get_translated_content('default_lang_code')

        return {
            'id_historias': self.id_historias,
            'Personas_id_persona': self.Personas_id_persona,
            'nombre_persona': self.persona.nombre if hasattr(self, 'persona') and self.persona else None,
            'Administrador_id_admin': self.Administrador_id_admin,
            'etiqueta_id_principal': self.etiqueta_id_principal,
            'nombre_etiqueta_principal': self.primary_tag.name if self.primary_tag else None,
            'contenido': content_for_lang, # Content now comes from translations
            'tags': [tag.to_dict() for tag in self.tags] if self.tags else [], # List of associated tags (many-to-many)
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            # Optionally, include all translations if needed for some admin views:
            # 'all_translations': [trans.to_dict() for trans in self.translations if self.translations]
        }
