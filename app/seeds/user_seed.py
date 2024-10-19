# Archivo: app/seeds/user_seed.py
import sys
import os

# Asegurarse de que el directorio raíz del proyecto está en sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app import create_app, db
from app.models.user_model import User, ADMINISTRATOR, TEACHER, SUPERVISOR

def seed_data():
    app = create_app()  # Crear la aplicación Flask
    with app.app_context():
        # Crear el usuario administrador
        admin_user = User(username='admin', email='admin@example.com', role=ADMINISTRATOR, is_verified=True)
        admin_user.set_password('adminpassword')  # Establecer la contraseña

        # Crear algunos usuarios maestros
        teacher1 = User(username='teacher1', email='teacher1@example.com', role=TEACHER, is_verified=True)
        teacher1.set_password('teacherpassword1')
        
        teacher2 = User(username='teacher2', email='teacher2@example.com', role=TEACHER, is_verified=True)
        teacher2.set_password('teacherpassword2')
        
        teacher3 = User(username='teacher3', email='teacher3@example.com', role=TEACHER, is_verified=True)
        teacher3.set_password('teacherpassword3')

        # Crear un usuario supervisor
        supervisor1 = User(username='supervisor1', email='supervisor1@example.com', role=SUPERVISOR, is_verified=True)
        supervisor1.set_password('supervisorpassword1')

        # Agregar los usuarios a la sesión
        db.session.add_all([admin_user, teacher1, teacher2, teacher3, supervisor1])
        db.session.commit()

        print("Seeding completado: Usuarios agregados con contraseñas seguras.")

if __name__ == '__main__':
    seed_data()
