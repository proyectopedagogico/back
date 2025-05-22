import os
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, current_user
from werkzeug.utils import secure_filename # For securely saving filenames

from . import bp # Import the blueprint 'bp' from app/api/__init__.py
from app import db
from app.models.person_model import Person
from app.models.image_model import Image # Assuming your Image model is in image_model.py

def allowed_file(filename):
    """Checks if the filename has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/persons/<int:id_persona>/images', methods=['POST'])
@jwt_required() # Protect this route
def upload_person_image(id_persona):
    """
    Uploads an image for a specific person.
    The image is sent as form-data (file part).
    Optionally, a 'descripcion' can be sent as another form field.
    """
    # Check if the person exists
    person = db.session.get(Person, id_persona)
    if not person:
        return jsonify({"error": f"Persona con id {id_persona} no encontrada."}), 404

    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No se encontró la parte del archivo en la solicitud."}), 400
    
    file = request.files['file']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return jsonify({"error": "No se seleccionó ningún archivo."}), 400

    if file and allowed_file(file.filename):
        # Secure the filename to prevent directory traversal attacks etc.
        filename = secure_filename(file.filename)
        
        # To avoid filename collisions, you might want to add a unique prefix (e.g., UUID or timestamp)
        # For example: filename = f"{uuid.uuid4().hex}_{filename}"
        
        # Construct the full path to save the file
        # UPLOAD_FOLDER is defined in config.py
        upload_folder = current_app.config['UPLOAD_FOLDER']
        filepath = os.path.join(upload_folder, filename)
        
        try:
            file.save(filepath)

            # Create a new Image record in the database
            descripcion = request.form.get('descripcion') # Get 'descripcion' from form data
            
            new_image = Image(
                url_imagen=filename,  # Store the filename or a relative path
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
            # current_app.logger.error(f"Error saving file or DB record: {e}") # Uncomment for logging
            # Potentially remove the saved file if DB operation fails
            # if os.path.exists(filepath):
            #     os.remove(filepath)
            return jsonify({"error": "Error interno del servidor al guardar la imagen.", "details": str(e)}), 500
    else:
        return jsonify({"error": "Tipo de archivo no permitido."}), 400

# You might also want an endpoint to serve these images if they are not served directly
# by a web server like Nginx or Apache. For example:
# @bp.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
# (You would need to import send_from_directory from flask)
