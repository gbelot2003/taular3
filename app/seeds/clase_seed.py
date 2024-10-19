# Archivo: app/seeds/clase_seed.py
import sys
import os
from datetime import time

# Asegurarse de que el directorio raíz del proyecto está en sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app import create_app, db
from app.models.grado_model import Grado
from app.models.clase_model import Clase
from app.models.user_model import User

def seed_clases():
    app = create_app()  # Crear la aplicación Flask
    with app.app_context():
        # Obtener los grados
        primero = Grado.query.filter_by(nombre='Septimo A').first()

        # Obtener los maestros (usuarios con rol Maestro)
        maestro1 = User.query.filter_by(username='teacher1').first()
        maestro2 = User.query.filter_by(username='teacher2').first()

        # Crear algunas clases con maestros y horarios
        clase1 = Clase(
            nombre='Matemáticas', 
            grado=primero, 
            maestro=maestro1, 
            horario_inicio=time(8, 0), 
            horario_fin=time(9, 30)
        )
        clase2 = Clase(
            nombre='Historia', 
            grado=primero, 
            maestro=maestro2, 
            horario_inicio=time(10, 0), 
            horario_fin=time(11, 30)
        )
        clase3 = Clase(
            nombre='Ciencias', 
            grado=primero, 
            maestro=maestro1, 
            horario_inicio=time(12, 0), 
            horario_fin=time(13, 30)
        )

        # Agregar las clases a la sesión
        db.session.add_all([clase1, clase2, clase3])
        db.session.commit()

        print("Seeding completado: Clases agregadas con maestros y horarios.")

if __name__ == '__main__':
    seed_clases()