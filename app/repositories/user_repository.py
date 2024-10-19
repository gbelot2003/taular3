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
        salt = current_app.config.get('SECURITY_SALT', 'your-salt-value')

        s = Serializer(secret_key)
        
        try:
            data = s.loads(token, salt=salt, max_age=1800)
            user_id = data['user_id']
        except:
            return None
        
        return db.session.get(User, user_id)

