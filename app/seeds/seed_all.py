# Archivo: app/seeds/seed_all.py

import sys
import os

# Asegurarse de que el directorio raíz del proyecto está en sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app import create_app, db
from app.seeds.user_seed import seed_data as seed_users
# from app.seeds.grado_seed import seed_grados
# from app.seeds.clase_seed import seed_clases
# from app.seeds.alumno_seed import seed_alumnos
# from app.seeds.parcial_seed import seed_parciales

def seed_all():
    app = create_app()  # Crear la aplicación Flask
    with app.app_context():
        # Limpiar la base de datos (opcional, si deseas reiniciar el contenido)
        db.drop_all()
        db.create_all()

        # Ejecutar los seeds individuales
        print("Seeding users...")
        seed_users()

        # print("Seeding grados...")
        # seed_grados()

        # print("Seeding clases...")
        # seed_clases()

        # print("Seeding alumnos...")
        # seed_alumnos()

        # print("Seeding parciales...")
        # seed_parciales()

        print("Seeding completado para todas las tablas.")

if __name__ == '__main__':
    seed_all()