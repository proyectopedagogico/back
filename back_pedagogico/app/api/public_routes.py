from flask import request, jsonify, current_app, url_for
from . import bp 
from app import db
from app.models.story_model import Story, historias_has_etiquetas_table # Import association table
from app.models.person_model import Person # Import Person model for joins
from app.models.tag_model import Tag # Import Tag model for joins

@bp.route('/public/stories', methods=['GET'])
def get_public_stories():
    """
    Retrieves a paginated list of all stories for public viewing.
    Accepts 'lang', 'page', 'per_page', 'procedencia', 'profesion', and 'tag' query parameters.
    """
    try:
        lang_code = request.args.get('lang', 'es', type=str)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Get filter parameters from query string
        procedencia_filter = request.args.get('procedencia', type=str)
        profesion_filter = request.args.get('profesion', type=str)
        tag_filter = request.args.get('tag', type=str) # Filter by tag name

        # Start with a base query
        query = Story.query

        # Join with Person model if filtering by procedencia or profesion
        if procedencia_filter or profesion_filter:
            query = query.join(Person, Story.Personas_id_persona == Person.id_persona)

        # Apply filters
        if procedencia_filter:
            query = query.filter(Person.procedencia.ilike(f"%{procedencia_filter}%"))
        if profesion_filter:
            query = query.filter(Person.profesion.ilike(f"%{profesion_filter}%"))
        
        # Join with Tag model if filtering by tag name
        if tag_filter:
            query = query.join(historias_has_etiquetas_table, (historias_has_etiquetas_table.c.historias_id_historias == Story.id_historias))\
                         .join(Tag, (historias_has_etiquetas_table.c.etiquetas_etiqueta_id == Tag.etiqueta_id))\
                         .filter(Tag.name.ilike(f"%{tag_filter}%"))

        # Order and paginate
        pagination = query.order_by(Story.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        stories = pagination.items
        stories_list = [story.to_dict(language_code=lang_code) for story in stories]
        
        # Prepare pagination metadata, including filter parameters in links
        filter_params = {}
        if procedencia_filter:
            filter_params['procedencia'] = procedencia_filter
        if profesion_filter:
            filter_params['profesion'] = profesion_filter
        if tag_filter:
            filter_params['tag'] = tag_filter

        meta = {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total_pages': pagination.pages,
            'total_items': pagination.total,
            'next_url': url_for('api.get_public_stories', page=pagination.next_num, per_page=per_page, lang=lang_code, **filter_params, _external=True) if pagination.has_next else None,
            'prev_url': url_for('api.get_public_stories', page=pagination.prev_num, per_page=per_page, lang=lang_code, **filter_params, _external=True) if pagination.has_prev else None
        }
        
        return jsonify({
            'items': stories_list,
            '_meta': meta
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving public stories: {e}", exc_info=True)
        return jsonify({"error": "Internal server error while fetching stories.", "details": str(e)}), 500

@bp.route('/public/stories/<int:id_historias>', methods=['GET'])
def get_public_story_detail(id_historias):
    """
    Retrieves a specific story by its ID for public viewing.
    Accepts a 'lang' query parameter for language preference.
    """
    try:
        lang_code = request.args.get('lang', 'es', type=str)
        
        story = db.session.get(Story, id_historias)
        
        if story is None:
            return jsonify({"error": "Story not found."}), 404 # English error
            
        return jsonify(story.to_dict(language_code=lang_code)), 200
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving public story {id_historias}: {e}", exc_info=True)
        return jsonify({"error": "Internal server error while fetching the story.", "details": str(e)}), 500