# Archivo: app/repositories/alumno_repository.py

from app.models.alumno_model import Alumno
from app.extensions import db

class AlumnoRepository:
    
    @staticmethod
    def get_all():
        """Obtiene todos los alumnos"""
        return Alumno.query.all()

    @staticmethod
    def get_by_id(alumno_id):
        """Obtiene un alumno por su ID"""
        return Alumno.query.get(alumno_id)

    @staticmethod
    def create(nombre, apellido, email, grado_id):
        """Crea un nuevo alumno"""
        nuevo_alumno = Alumno(
            nombre=nombre,
            apellido=apellido,
            email=email,
            grado_id=grado_id
        )
        db.session.add(nuevo_alumno)
        db.session.commit()
        return nuevo_alumno

    @staticmethod
    def update(alumno_id, nombre=None, apellido=None, email=None, grado_id=None):
        """Actualiza un alumno existente"""
        alumno = Alumno.query.get(alumno_id)
        if not alumno:
            return None

        if nombre:
            alumno.nombre = nombre
        if apellido:
            alumno.apellido = apellido
        if email:
            alumno.email = email
        if grado_id:
            alumno.grado_id = grado_id

        db.session.commit()
        return alumno

    @staticmethod
    def delete(alumno_id):
        """Elimina un alumno por su ID"""
        alumno = Alumno.query.get(alumno_id)
        if not alumno:
            return False

        db.session.delete(alumno)
        db.session.commit()
        return True