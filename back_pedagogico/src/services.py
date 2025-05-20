from .models import db, Historia

def get_all_histories_service():
    return [h.to_dict() for h in Historia.query.all()]

def get_history_service(historia_id):
    historia = Historia.query.get(historia_id)
    return historia.to_dict() if historia else None

def add_history_service(nombre, contenido, soft_skill, foto=None):
    historia = Historia(
        nombre=nombre,
        contenido=contenido,
        soft_skill=soft_skill,
        foto=foto
    )
    db.session.add(historia)
    db.session.commit()
    return historia.to_dict()

def delete_history_service(historia_id):
    historia = Historia.query.get(historia_id)
    if historia:
        db.session.delete(historia)
        db.session.commit()
        return True
    return False

def answer_history_service(historia_id, respuesta):
    historia = Historia.query.get(historia_id)
    if historia:
        historia.respuesta = respuesta
        db.session.commit()
        return historia.to_dict()
    return None

def fill_initial_data():
    if not Historia.query.first():
        ejemplos = [
            Historia(
                nombre="Ana Pérez",
                contenido="Aprendí resiliencia al enfrentar desafíos en el taller.",
                soft_skill="Resiliencia",
                foto="assets/ana.jpg"
            ),
            Historia(
                nombre="Lucía Gómez",
                contenido="La comunicación fue clave para liderar mi equipo.",
                soft_skill="Comunicación",
                foto="assets/lucia.jpg"
            ),
            Historia(
                nombre="Carmen Ruiz",
                contenido="La empatía me ayudó a conectar con mis compañeras.",
                soft_skill="Empatía",
                foto="assets/carmen.jpg"
            )
        ]
        db.session.add_all(ejemplos)
        db.session.commit()
