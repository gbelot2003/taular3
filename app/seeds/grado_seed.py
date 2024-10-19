# Archivo: app/seeds/grado_seed.py
import sys
import os

# Asegurarse de que el directorio raíz del proyecto está en sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app import create_app, db
from app.models.grado_model import Grado

def seed_grados():
    app = create_app()  # Crear la aplicación Flask
    with app.app_context():
        # Crear algunos grados escolares
        grado1 = Grado(nombre='Septimo A', descripcion='Septimo A')
        grado2 = Grado(nombre='Septimo B', descripcion='Septimo B')
        grado3 = Grado(nombre='Octavo A', descripcion='Octavo A')
        grado4 = Grado(nombre='Octavo B', descripcion='Octavo B')
        grado5 = Grado(nombre='Noveno', descripcion='Noveno')
        grado6 = Grado(nombre='Decimo', descripcion='Decimo')

        # Agregar los grados a la sesión
        db.session.add_all([grado1, grado2, grado3, grado4, grado5, grado6])
        db.session.commit()

        print("Seeding completado: Grados agregados.")

if __name__ == '__main__':
    seed_grados()