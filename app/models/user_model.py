# app/models/user_model.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db  # Importar db desde extensions

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Crea un hash de la contraseña"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica la contraseña ingresada"""
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def authenticate(email, password):
        """Autentica al usuario verificando su email y contraseña"""
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None
