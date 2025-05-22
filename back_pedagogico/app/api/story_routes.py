from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, current_user 

from . import bp 
from app import db
# Ensure AdminUser is imported if needed by current_user, though JWT handles the object loading
# from app.models.admin_user_model import AdminUser 
from app.models.story_model import Story
from app.models.story_translation_model import StoryTranslation
from app.models.person_model import Person
from app.models.tag_model import Tag

# NOTE: Authentication routes (admin_login, admin_logout) have been removed from this file.
# They should be in a separate app/api/auth_routes.py file and imported by app/api/__init__.py.

@bp.route('/stories', methods=['POST'])
@jwt_required()
def create_story():
    """
    Creates a new story with its translations and tags.
    Expects a JSON payload with story details.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "El cuerpo de la solicitud debe ser JSON."}), 400

    personas_id_persona = data.get('Personas_id_persona')
    traducciones_data = data.get('traducciones')

    if personas_id_persona is None:
        return jsonify({"error": "El campo 'Personas_id_persona' es obligatorio."}), 400
    if not traducciones_data or not isinstance(traducciones_data, list) or not traducciones_data:
        return jsonify({"error": "El campo 'traducciones' es obligatorio y debe ser una lista no vacía de traducciones."}), 400

    person = db.session.get(Person, personas_id_persona)
    if not person:
        return jsonify({"error": f"La persona con id {personas_id_persona} no existe."}), 404

    # current_user is populated by @jwt.user_lookup_loader in app/__init__.py
    # Ensure your AdminUser model has 'id_admin' as its primary key attribute
    administrador_id_admin = current_user.id_admin 

    etiqueta_id_principal = data.get('etiqueta_id_principal')
    if etiqueta_id_principal is not None:
        principal_tag = db.session.get(Tag, etiqueta_id_principal)
        if not principal_tag:
            return jsonify({"error": f"La etiqueta principal con id {etiqueta_id_principal} no existe."}), 404
    
    many_to_many_tag_ids = data.get('tag_ids', []) 

    try:
        new_story = Story(
            Personas_id_persona=personas_id_persona,
            Administrador_id_admin=administrador_id_admin,
            etiqueta_id_principal=etiqueta_id_principal
        )
        db.session.add(new_story)
        db.session.flush() 

        for trans_data in traducciones_data:
            codigo_idioma = trans_data.get('codigo_idioma')
            contenido_traducido = trans_data.get('contenido_traducido')
            if not codigo_idioma or not contenido_traducido:
                db.session.rollback() 
                return jsonify({"error": "Cada traducción debe tener 'codigo_idioma' y 'contenido_traducido'."}), 400
            
            translation = StoryTranslation(
                historias_id_historias=new_story.id_historias,
                codigo_idioma=codigo_idioma,
                contenido_traducido=contenido_traducido
            )
            db.session.add(translation)

        if many_to_many_tag_ids:
            new_tags_list = []
            for tag_id in many_to_many_tag_ids:
                tag = db.session.get(Tag, tag_id)
                if tag:
                    new_tags_list.append(tag)
                else:
                    current_app.logger.warn(f"Tag con id {tag_id} no encontrado al crear historia.")
            new_story.tags = new_tags_list
        
        db.session.commit()
        
        return jsonify(new_story.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al crear la historia: {e}", exc_info=True)
        return jsonify({"error": "Error interno del servidor al crear la historia.", "details": str(e)}), 500

@bp.route('/stories', methods=['GET'])
@jwt_required()
def get_stories():
    """
    Retrieves a list of all stories.
    """
    try:
        lang_code = request.args.get('lang', 'es') 
        stories = Story.query.all()
        stories_list = [story.to_dict(language_code=lang_code) for story in stories]
        return jsonify(stories_list), 200
    except Exception as e:
        current_app.logger.error(f"Error al obtener historias: {e}", exc_info=True)
        return jsonify({"error": "Error interno del servidor al obtener las historias.", "details": str(e)}), 500

@bp.route('/stories/<int:id_historias>', methods=['GET'])
@jwt_required()
def get_story(id_historias):
    """
    Retrieves a specific story by its ID.
    """
    try:
        lang_code = request.args.get('lang', 'es')
        story = db.session.get(Story, id_historias)
        if story is None:
            return jsonify({"error": "Historia no encontrada."}), 404
            
        return jsonify(story.to_dict(language_code=lang_code)), 200
    except Exception as e:
        current_app.logger.error(f"Error al obtener la historia {id_historias}: {e}", exc_info=True)
        return jsonify({"error": "Error interno del servidor al obtener la historia.", "details": str(e)}), 500

@bp.route('/stories/<int:id_historias>', methods=['PUT'])
@jwt_required()
def update_story(id_historias):
    """
    Updates an existing story, its translations, and tags.
    """
    try:
        story = db.session.get(Story, id_historias)
        if story is None:
            return jsonify({"error": "Historia no encontrada."}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "El cuerpo de la solicitud debe ser JSON."}), 400

        if 'Personas_id_persona' in data:
            new_id_persona = data.get('Personas_id_persona')
            person = db.session.get(Person, new_id_persona)
            if not person:
                return jsonify({"error": f"La persona con id {new_id_persona} no existe."}), 404
            story.Personas_id_persona = new_id_persona
        
        if 'etiqueta_id_principal' in data: 
            etiqueta_id_principal = data.get('etiqueta_id_principal')
            if etiqueta_id_principal is not None:
                principal_tag = db.session.get(Tag, etiqueta_id_principal)
                if not principal_tag:
                    return jsonify({"error": f"La etiqueta principal con id {etiqueta_id_principal} no existe."}), 404
            story.etiqueta_id_principal = etiqueta_id_principal

        if 'traducciones' in data:
            traducciones_data = data.get('traducciones')
            if not isinstance(traducciones_data, list):
                return jsonify({"error": "'traducciones' debe ser una lista."}), 400
            
            # Efficiently delete old translations
            StoryTranslation.query.filter_by(historias_id_historias=story.id_historias).delete()
            
            for trans_data in traducciones_data:
                codigo_idioma = trans_data.get('codigo_idioma')
                contenido_traducido = trans_data.get('contenido_traducido')
                if not codigo_idioma or not contenido_traducido:
                    db.session.rollback()
                    return jsonify({"error": "Cada traducción debe tener 'codigo_idioma' y 'contenido_traducido'."}), 400
                new_trans = StoryTranslation(
                    historias_id_historias=story.id_historias,
                    codigo_idioma=codigo_idioma,
                    contenido_traducido=contenido_traducido
                )
                db.session.add(new_trans)

        if 'tag_ids' in data:
            tag_ids = data.get('tag_ids', [])
            updated_tags = []
            if tag_ids: 
                for tag_id in tag_ids:
                    tag = db.session.get(Tag, tag_id)
                    if tag:
                        updated_tags.append(tag)
                    else:
                        current_app.logger.warn(f"Tag con id {tag_id} no encontrado al actualizar historia.")
            story.tags = updated_tags 
        
        db.session.commit()
        return jsonify(story.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al actualizar la historia {id_historias}: {e}", exc_info=True)
        return jsonify({"error": "Error interno del servidor al actualizar la historia.", "details": str(e)}), 500

@bp.route('/stories/<int:id_historias>', methods=['DELETE'])
@jwt_required()
def delete_story(id_historias):
    """
    Deletes a specific story by its ID.
    """
    try:
        story = db.session.get(Story, id_historias)
        if story is None:
            return jsonify({"error": "Historia no encontrada."}), 404

        db.session.delete(story)
        db.session.commit()
        
        return jsonify({"message": "Historia eliminada correctamente."}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al eliminar la historia {id_historias}: {e}", exc_info=True)
        return jsonify({"error": "Error interno del servidor al eliminar la historia.", "details": str(e)}), 500
