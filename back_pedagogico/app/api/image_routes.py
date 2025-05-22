import os
from flask import request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
import uuid # For generating unique filenames

from . import bp 
from app import db
from app.models.person_model import Person
from app.models.image_model import Image

def allowed_file(filename):
    """Checks if the filename has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/persons/<int:id_persona>/images', methods=['POST'])
@jwt_required()
def upload_person_image(id_persona):
    """
    Uploads an image for a specific person.
    The image is sent as form-data (file part).
    Optionally, a 'descripcion' can be sent as another form field.
    """
    person = db.session.get(Person, id_persona)
    if not person:
        return jsonify({"error": f"Persona con id {id_persona} no encontrada."}), 404

    if 'file' not in request.files:
        return jsonify({"error": "No se encontró la parte del archivo en la solicitud."}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No se seleccionó ningún archivo."}), 400

    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        # Generate a unique filename to prevent overwrites and keep original extension
        extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
        unique_filename = f"{uuid.uuid4().hex}.{extension}" if extension else f"{uuid.uuid4().hex}"
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        filepath = os.path.join(upload_folder, unique_filename)
        
        try:
            file.save(filepath)

            descripcion = request.form.get('descripcion')
            
            new_image = Image(
                url_imagen=unique_filename,  # Store the unique filename
                personas_id_persona=id_persona,
                descripcion=descripcion
            )
            db.session.add(new_image)
            db.session.commit()

            return jsonify({
                "message": "Archivo subido y registrado exitosamente.",
                "image_details": new_image.to_dict()
            }), 201

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error saving file or DB record: {e}", exc_info=True)
            # Potentially remove the saved file if DB operation fails
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception as e_remove:
                    current_app.logger.error(f"Error removing partially uploaded file {filepath}: {e_remove}")
            return jsonify({"error": "Error interno del servidor al guardar la imagen.", "details": str(e)}), 500
    else:
        return jsonify({"error": "Tipo de archivo no permitido."}), 400

# Endpoint to serve uploaded images (optional, for development/testing)
# In production, your web server (Nginx/Apache) should ideally serve static files.
@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serves an uploaded file from the UPLOAD_FOLDER."""
    # Ensure the filename is secure before passing to send_from_directory
    # although send_from_directory itself does some path safety checks.
    secure_name = secure_filename(filename)
    if secure_name != filename: # Basic check if secure_filename altered it significantly (e.g. removed path components)
        # This might indicate a potentially malicious filename
        return jsonify({"error": "Nombre de archivo inválido."}), 400
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], secure_name)