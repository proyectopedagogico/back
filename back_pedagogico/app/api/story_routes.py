from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user # current_user will be the AdminUser object

from . import bp # Import the blueprint 'bp' from app/api/__init__.py
from app import db
from app.models.story_model import Story
from app.models.person_model import Person
# from app.models.tag_model import Tag # Import if you handle tags during story creation

@bp.route('/stories', methods=['POST'])
@jwt_required() # Protect this route, only authenticated admins can create stories
def create_story():
    """
    Creates a new story.
    Expects a JSON payload with story details.
    The admin creating the story is identified by the JWT.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Required fields for a story
    contenido = data.get('contenido')
    id_persona = data.get('id_persona') # ID of the person this story is about

    if not contenido:
        return jsonify({"error": "El campo 'contenido' es obligatorio."}), 400
    if id_persona is None: # Check for None as id_persona could be 0 if that's a valid ID
        return jsonify({"error": "El campo 'id_persona' es obligatorio."}), 400

    # Verify if the person exists
    person = Person.query.get(id_persona)
    if not person:
        return jsonify({"error": f"La persona con id {id_persona} no existe."}), 404

    # Get the ID of the authenticated admin user from the JWT
    # current_user is populated by our @jwt.user_lookup_loader
    administrador_id_admin = current_user.id

    # Optional fields
    # title = data.get('title') # If you decide to add a title to stories directly
    # image_url = data.get('image_url') # If a story has a main image
    # etiqueta_ids = data.get('etiqueta_ids') # Example: a list of tag IDs to associate

    try:
        new_story = Story(
            contenido=contenido,
            id_persona=id_persona,
            administrador_id_admin=administrador_id_admin
            # Add other fields like title, image_url if you include them
        )

        # Handling tags (if etiqueta_ids are provided and you want to link them)
        # if etiqueta_ids:
        #     for tag_id in etiqueta_ids:
        #         tag = Tag.query.get(tag_id)
        #         if tag:
        #             new_story.tags.append(tag)
        #         else:
        #             # Handle case where a tag_id is invalid, maybe collect errors
        #             pass 

        db.session.add(new_story)
        db.session.commit()
        
        # Return the created story, including its new ID and any relationships
        return jsonify(new_story.to_dict()), 201 # 201 Created

    except Exception as e:
        db.session.rollback()
        # Log the error for debugging
        # current_app.logger.error(f"Error creating story: {e}")
        return jsonify({"error": "Error interno del servidor al crear la historia.", "details": str(e)}), 500
    
    
@bp.route('/stories', methods=['GET'])
@jwt_required() # Protect this route
def get_stories():
    """
    Retrieves a list of all stories.
    """
    try:
        stories = Story.query.all()
        # Convert each story object to its dictionary representation
        stories_list = [story.to_dict() for story in stories]
        return jsonify(stories_list), 200
    except Exception as e:
        # current_app.logger.error(f"Error retrieving stories: {e}") # Uncomment for logging
        return jsonify({"error": "Error interno del servidor al obtener las historias.", "details": str(e)}), 500


@bp.route('/stories/<int:id_historias>', methods=['GET'])
@jwt_required() # Protect this route
def get_story(id_historias):
    """
    Retrieves a specific story by its ID.
    """
    try:
        # Story.query.get_or_404(id_historias) is a convenient way to get a record or raise a 404 error
        story = db.session.get(Story, id_historias) # More direct way with SQLAlchemy 2.0 style
        if story is None:
            return jsonify({"error": "Historia no encontrada."}), 404
            
        return jsonify(story.to_dict()), 200
    except Exception as e:
        # current_app.logger.error(f"Error retrieving story {id_historias}: {e}") # Uncomment for logging
        return jsonify({"error": "Error interno del servidor al obtener la historia.", "details": str(e)}), 500


@bp.route('/stories/<int:id_historias>', methods=['PUT'])
@jwt_required() # Protect this route
def update_story(id_historias):
    """
    Updates an existing story.
    Expects a JSON payload with fields to update.
    """
    try:
        story = db.session.get(Story, id_historias)
        if story is None:
            return jsonify({"error": "Historia no encontrada."}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        # Update fields if they are provided in the request data

        if 'contenido' in data:
            story.contenido = data['contenido']
        
        # To update 'id_persona', ensure the new person exists
        if 'id_persona' in data:
            new_id_persona = data.get('id_persona')
            if new_id_persona is None:
                return jsonify({"error": "El campo 'id_persona' no puede ser nulo si se intenta actualizar."}), 400
            person = db.session.get(Person, new_id_persona)
            if not person:
                return jsonify({"error": f"La persona con id {new_id_persona} no existe."}), 404
            story.id_persona = new_id_persona
        # Add updates for other fields from your Story model as needed:
        # story.title = data.get('title', story.title) # If you add a title
        # story.origin = data.get('origin', story.origin)
        # story.age_group = data.get('age_group', story.age_group)
        # story.profession = data.get('profession', story.profession)
        # story.image_url = data.get('image_url', story.image_url)
        # story.notable_elements = data.get('notable_elements', story.notable_elements)

        # Note: Updating 'administrador_id_admin' might not be typical unless transferring ownership.
        # Handling tags (if implemented) would require more complex logic here:
        # - Clear existing tags for the story.
        # - Add new tags based on IDs provided in 'data'.

        db.session.commit()
        return jsonify(story.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        # current_app.logger.error(f"Error updating story {id_historias}: {e}") # Uncomment for logging
        return jsonify({"error": "Error interno del servidor al actualizar la historia.", "details": str(e)}), 500


@bp.route('/stories/<int:id_historias>', methods=['DELETE'])
@jwt_required() # Protect this route
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
        
        return jsonify({"message": "Historia eliminada correctamente."}), 200 # Or 204 No Content
    except Exception as e:
        db.session.rollback()
        # current_app.logger.error(f"Error deleting story {id_historias}: {e}") # Uncomment for logging
        return jsonify({"error": "Error interno del servidor al eliminar la historia.", "details": str(e)}), 500


