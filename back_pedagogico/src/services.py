from src.models import db, Historia, Etiqueta

def get_all_historias():
    return Historia.query.all()

def get_historia_by_id(id_historias):
    return Historia.query.get(id_historias)

def create_historia(Personas_id_persona, Administrador_id_admin, etiqueta_id_principal=None):
    historia = Historia(
        Personas_id_persona=Personas_id_persona,
        Administrador_id_admin=Administrador_id_admin,
        etiqueta_id_principal=etiqueta_id_principal
    )
    db.session.add(historia)
    db.session.commit()
    return historia

def get_all_etiquetas():
    return Etiqueta.query.all()
