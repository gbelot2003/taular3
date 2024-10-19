# Archivo: app/models/user_model.py

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from app.extensions import db
from flask import current_app
import json

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        """Hashea la contraseña y la almacena"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con la hasheada"""
        return check_password_hash(self.password_hash, password)

    @classmethod
    def authenticate(cls, email, password):
        """Autentica al usuario según el correo y la contraseña"""
        user = cls.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None

    def generate_verification_token(self, expires_sec=1800):
        """Genera un token de verificación de correo electrónico"""
        secret_key = current_app.config['SECRET_KEY']
        salt = current_app.config.get('SECURITY_SALT', 'your-salt-value')

        s = Serializer(secret_key, expires_sec)
        return s.dumps({'user_id': self.id}, salt=salt)

    @staticmethod
    def verify_token(token):
        """Verifica el token de verificación de correo electrónico"""
        secret_key = current_app.config['SECRET_KEY']
        salt = current_app.config.get('SECURITY_SALT', 'your-salt-value')
        s = Serializer(secret_key)
        
        try:
            data = s.loads(token, salt=salt, max_age=1800)
            user_id = data['user_id']
        except:
            return None
        
        return User.query.get(user_id)

    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        """Devuelve True si el usuario está activo y verificado"""
        return self.is_verified

    def __repr__(self):
        return f'<User {self.username} - Role: {self.role}>'

# Define constantes para los roles
ADMINISTRATOR = 'Administrador'
TEACHER = 'Maestro'
SUPERVISOR = 'Supervisor'
