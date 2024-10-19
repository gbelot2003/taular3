# app/models/user_model.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db  # Importar db desde extensions

class User(UserMixin, db.Model):  # Hereda de UserMixin
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def set_password(self, password):
        """Hashea la contraseña y la almacena"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con la hasheada"""
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def authenticate(email, password):
        """Autentica al usuario verificando su email y contraseña"""
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None

    def get_id(self):
        """Devuelve el ID del usuario para Flask-Login"""
        return str(self.id)

    @property
    def is_active(self):
        """Devuelve True si el usuario está activo"""
        return True

    def __repr__(self):
        return f'<User {self.username} - Role: {self.role}>'

# Opcionales: Define constantes para los roles
ADMINISTRATOR = 'Administrador'
TEACHER = 'Maestro'
SUPERVISOR = 'Supervisor'
