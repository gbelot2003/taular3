# Archivo: app/repositories/user_repository.py
from app.models.user_model import User
from app.extensions import db
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

class UserRepository:
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def update_user(user, **kwargs):
        """Actualiza los atributos de un usuario y guarda los cambios en la base de datos"""
        for key, value in kwargs.items():
            setattr(user, key, value)
        db.session.commit()

    @staticmethod
    def verify_token(token):
        """Verifica el token de verificación de correo electrónico y devuelve el usuario correspondiente"""
        secret_key = current_app.config['SECRET_KEY']
        salt = "your-salt-value"

        if not isinstance(secret_key, (str, bytes)):
            raise TypeError("SECRET_KEY must be una cadena o bytes")
        
        if isinstance(secret_key, str):
            secret_key = secret_key.encode('utf-8')
        
        if not isinstance(salt, (str, bytes)):
            raise TypeError("Salt must be una cadena o bytes")
        
        if isinstance(salt, str):
            salt = salt.encode('utf-8')

        s = Serializer(secret_key)
        signer = s.make_signer(salt=salt)
        
        try:
            data = signer.unsign(token, max_age=1800)
            user_id = eval(data)['user_id']
        except:
            return None
        
        return db.session.get(User, user_id)

