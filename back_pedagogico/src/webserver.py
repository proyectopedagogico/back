from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from .models import db
from .services import (
    get_all_histories_service,
    get_history_service,
    add_history_service,
    delete_history_service,
    answer_history_service,
    fill_initial_data
)
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///historias.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    fill_initial_data()

# Endpoints API

@app.route("/historias", methods=["GET"])
def all_histories_route():
    historias = get_all_histories_service()
    return jsonify(historias)

@app.route("/historias/<int:historia_id>", methods=["GET"])
def get_history_route(historia_id):
    historia = get_history_service(historia_id)
    return jsonify(historia) if historia else ("Historia no encontrada", 404)

@app.route("/historias", methods=["POST"])
def add_history_route():
    data = request.get_json()
    historia = add_history_service(
        nombre=data.get("nombre"),
        contenido=data.get("contenido"),
        soft_skill=data.get("soft_skill"),
        foto=data.get("foto")  # Espera la ruta relativa, ej: "assets/nueva.jpg"
    )
    return jsonify(historia), 201

@app.route("/historias/<int:historia_id>", methods=["DELETE"])
def delete_history_route(historia_id):
    deleted = delete_history_service(historia_id)
    if deleted:
        return "", 204
    else:
        return ("Historia no encontrada", 404)

@app.route("/historias/<int:historia_id>/respuesta", methods=["POST"])
def answer_history_route(historia_id):
    data = request.get_json()
    historia = answer_history_service(historia_id, data.get("respuesta"))
    return jsonify(historia) if historia else ("Historia no encontrada", 404)

# Endpoint para servir imágenes de la carpeta assets
@app.route('/assets/<path:filename>')
def assets(filename):
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
    return send_from_directory(assets_dir, filename)
