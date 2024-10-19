# Archivo: app/repositories/clase_repository.py

from app.models.clase_model import Clase
from app.extensions import db

class ClaseRepository:

    @staticmethod
    def get_all():
        """Obtiene todas las clases"""
        return Clase.query.all()

    @staticmethod
    def get_by_id(clase_id):
        """Obtiene una clase por su ID"""
        return Clase.query.get(clase_id)

    @staticmethod
    def get_by_grado(grado_id):
        """Obtiene todas las clases pertenecientes a un grado específico"""
        return Clase.query.filter_by(grado_id=grado_id).all()

    @staticmethod
    def create(nombre, grado_id, maestro_id, horario_inicio, horario_fin):
        """Crea una nueva clase"""
        nueva_clase = Clase(
            nombre=nombre,
            grado_id=grado_id,
            maestro_id=maestro_id,
            horario_inicio=horario_inicio,
            horario_fin=horario_fin
        )
        db.session.add(nueva_clase)
        db.session.commit()
        return nueva_clase

    @staticmethod
    def update(clase_id, nombre=None, grado_id=None, maestro_id=None, horario_inicio=None, horario_fin=None):
        """Actualiza una clase existente"""
        clase = Clase.query.get(clase_id)
        if not clase:
            return None

        if nombre:
            clase.nombre = nombre
        if grado_id:
            clase.grado_id = grado_id
        if maestro_id:
            clase.maestro_id = maestro_id
        if horario_inicio:
            clase.horario_inicio = horario_inicio
        if horario_fin:
            clase.horario_fin = horario_fin

        db.session.commit()
        return clase

    @staticmethod
    def delete(clase_id):
        """Elimina una clase por su ID"""
        clase = Clase.query.get(clase_id)
        if not clase:
            return False

        db.session.delete(clase)
        db.session.commit()
        return True
