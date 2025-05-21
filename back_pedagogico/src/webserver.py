from flask import Flask, jsonify, request
from src.models import db, Administrador, Imagen, Historia, Persona, Etiqueta
import src.services as services

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/mydb'
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
        "id": h.id_historias,
        "contenido": h.contenido
    } for h in historias])

@app.route("/historias/<int:historia_id>", methods=["GET"])
def get_historia(historia_id):
    historia = services.get_historia_by_id(historia_id)
    if historia:
        return jsonify({
            "id": historia.id_historias,
            "contenido": historia.contenido
        })
    else:
        return jsonify({"error": "Historia no encontrada"}), 404

@app.route("/historias", methods=["POST"])
def create_historia():
    data = request.json
    contenido = data.get("contenido")
    administrador_id = data.get("administrador_id_admin")
    historia = services.create_historia(contenido, administrador_id)
    return jsonify({
        "id": historia.id_historias,
        "contenido": historia.contenido
    }), 201

@app.route("/etiquetas", methods=["GET"])
def all_etiquetas_route():
    etiquetas = services.get_all_etiquetas()
    return jsonify([{
        "id": e.id_etiqueta,
        "nombre": e.nombre_etiqueta
    } for e in etiquetas])
