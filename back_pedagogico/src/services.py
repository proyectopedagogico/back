from src.models import db, Historia, Etiqueta

def get_all_historias():
    return Historia.query.all()

def get_historia_by_id(historia_id):
    return Historia.query.get(historia_id)

def create_historia(contenido, administrador_id):
    historia = Historia(contenido=contenido, administrador_id_admin=administrador_id)
    db.session.add(historia)
    db.session.commit()
    return historia

def get_all_etiquetas():
    return Etiqueta.query.all()
