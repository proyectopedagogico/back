from flask import Blueprint


# Se crea una instancia de Blueprint para la API.
# El primer argumento, 'api', es el nombre del blueprint.
# El segundo argumento, __name__, ayuda a Flask a localizar los recursos del blueprint.
bp = Blueprint('api', __name__)

# Importa aquí los módulos de rutas para registrarlas con el blueprint.
# Es importante importarlos después de que el Blueprint 'bp' haya sido creado.
# Estas importaciones están al final para evitar dependencias circulares, ya que
# los módulos de rutas importarán 'bp' desde este archivo.

from . import auth_routes # Para las rutas de autenticación (login, logout)
from . import story_routes # Para las rutas CRUD de historias (lo crearás más adelante)
from . import image_routes
# from . import admin_routes # Para otras rutas específicas de administración (si se necesitan por separado)

# También puedes añadir aquí manejadores de errores comunes para el blueprint de la API si es necesario.
# Por ejemplo:
# from flask import jsonify
# from app import db # Si necesitas db para, por ejemplo, hacer rollback en un error 500

# @bp.app_errorhandler(404)
# def not_found_error(error):
#     return jsonify({"error": "Not found", "message": str(error)}), 404

# @bp.app_errorhandler(500)
# def internal_error(error):
#     # db.session.rollback() # Ejemplo: hacer rollback de la sesión de bd en un error interno
#     return jsonify({"error": "Internal server error", "message": str(error)}), 500
