from flask import request, jsonify, current_app
from . import bp  # Import the blueprint 'bp' from app/api/__init__.py
from app import db
from app.models.story_model import Story
# We might not need Person, Tag models directly here if Story.to_dict() handles them

@bp.route('/public/stories', methods=['GET'])
def get_public_stories():
    """
    Retrieves a list of all stories for public viewing.
    Accepts a 'lang' query parameter for language preference.
    """
    try:
        lang_code = request.args.get('lang', 'es')  # Default to Spanish
        
        # Add any filtering logic here if only "published" stories should be shown
        # For now, we retrieve all stories
        stories = Story.query.order_by(Story.created_at.desc()).all() # Example: order by creation date
        
        stories_list = [story.to_dict(language_code=lang_code) for story in stories]
        return jsonify(stories_list), 200
        
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
        lang_code = request.args.get('lang', 'es')  # Default to Spanish
        
        story = db.session.get(Story, id_historias)
        
        if story is None:
            return jsonify({"error": "Story not found."}), 404
            
        return jsonify(story.to_dict(language_code=lang_code)), 200
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving public story {id_historias}: {e}", exc_info=True)
        return jsonify({"error": "Internal server error while fetching the story.", "details": str(e)}), 500
