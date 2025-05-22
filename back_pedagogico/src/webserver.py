from flask import Flask, jsonify, request
from src.models import db, Administrador, Imagen, Historia, Persona, Etiqueta
import src.services as services

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/proyecto-pedagogico'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return "¡Conexión exitosa con MySQL!"

@app.route("/historias", methods=["GET"])
def all_histories_route():
    historias = services.get_all_historias()
    return jsonify([{
        "id_historias": h.id_historias,
        "Personas_id_persona": h.Personas_id_persona,
        "Administrador_id_admin": h.Administrador_id_admin,
        "etiqueta_id_principal": h.etiqueta_id_principal
    } for h in historias])

@app.route("/historias/<int:id_historias>", methods=["GET"])
def get_historia(id_historias):
    historia = services.get_historia_by_id(id_historias)
    if historia:
        return jsonify({
            "id_historias": historia.id_historias,
            "Personas_id_persona": historia.Personas_id_persona,
            "Administrador_id_admin": historia.Administrador_id_admin,
            "etiqueta_id_principal": historia.etiqueta_id_principal
        })
    else:
        return jsonify({"error": "Historia no encontrada"}), 404

@app.route("/historias", methods=["POST"])
def create_historia():
    data = request.json
    Personas_id_persona = data.get("Personas_id_persona")
    Administrador_id_admin = data.get("Administrador_id_admin")
    etiqueta_id_principal = data.get("etiqueta_id_principal")
    historia = services.create_historia(Personas_id_persona, Administrador_id_admin, etiqueta_id_principal)
    return jsonify({
        "id_historias": historia.id_historias,
        "Personas_id_persona": historia.Personas_id_persona,
        "Administrador_id_admin": historia.Administrador_id_admin,
        "etiqueta_id_principal": historia.etiqueta_id_principal
    }), 201

@app.route("/etiquetas", methods=["GET"])
def all_etiquetas_route():
    etiquetas = services.get_all_etiquetas()
    return jsonify([{
        "etiqueta_id": e.etiqueta_id,
        "name": e.name
    } for e in etiquetas])
