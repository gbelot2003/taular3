# Archivo: app/models/user_model.py

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from app.extensions import db
from flask import current_app

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
        # Asegurarse de que el SECRET_KEY sea una cadena o bytes
        secret_key = "secrettest"  # current_app.config['SECRET_KEY']
        print(secret_key)
        
        if not isinstance(secret_key, (str, bytes)):
            raise TypeError("SECRET_KEY must be a string or bytes")
        
        if isinstance(secret_key, str):
            secret_key = secret_key.encode('utf-8')
        
        # Asegurarse de que el salt sea una cadena o bytes
        salt = "your-salt-value"  # Replace with your actual salt value
        if not isinstance(salt, (str, bytes)):
            raise TypeError("Salt must be a string or bytes")
        
        if isinstance(salt, str):
            salt = salt.encode('utf-8')
        
        # Generar el token utilizando el secret_key y salt convertidos a bytes
        s = Serializer(secret_key, expires_sec)
        signer = s.make_signer(salt=salt)
        return signer.sign(str({'user_id': self.id})).decode('utf-8')

    @staticmethod
    def verify_token(token):
        """Verifica el token de verificación de correo electrónico"""
        secret_key = "secrettest"  # current_app.config['SECRET_KEY']
        salt = "your-salt-value"  # Replace with your actual salt value
        
        if not isinstance(secret_key, (str, bytes)):
            raise TypeError("SECRET_KEY must be a string or bytes")
        
        if isinstance(secret_key, str):
            secret_key = secret_key.encode('utf-8')
        
        if not isinstance(salt, (str, bytes)):
            raise TypeError("Salt must be a string or bytes")
        
        if isinstance(salt, str):
            salt = salt.encode('utf-8')
        
        s = Serializer(secret_key)
        signer = s.make_signer(salt=salt)
        
        try:
            data = signer.unsign(token, max_age=1800)
            user_id = eval(data)['user_id']
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