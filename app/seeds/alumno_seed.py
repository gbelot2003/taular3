# Archivo: app/seeds/alumno_seed.py
import sys
import os

# Asegurarse de que el directorio raíz del proyecto está en sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app import create_app, db
from app.models.grado_model import Grado
from app.models.alumno_model import Alumno

def seed_alumnos():
    app = create_app()  # Crear la aplicación Flask
    with app.app_context():
        # Obtener los grados
        primero = Grado.query.filter_by(nombre='Septimo A').first()
        segundo = Grado.query.filter_by(nombre='Septimo B').first()

        # Crear algunos alumnos y asignarlos a grados
        alumno1 = Alumno(nombre='Juan', apellido='Pérez', email='juan.perez@example.com', grado=primero)
        alumno2 = Alumno(nombre='María', apellido='López', email='maria.lopez@example.com', grado=primero)
        alumno3 = Alumno(nombre='Carlos', apellido='Rodríguez', email='carlos.rodriguez@example.com', grado=segundo)
        alumno4 = Alumno(nombre='Ana', apellido='Martínez', email='ana.martinez@example.com', grado=segundo)

        # Agregar los alumnos a la sesión
        db.session.add_all([alumno1, alumno2, alumno3, alumno4])
        db.session.commit()

        print("Seeding completado: Alumnos agregados.")

if __name__ == '__main__':
    seed_alumnos()