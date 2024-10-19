# Archivo: app/__init__.py

from flask import Flask, render_template, session
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_session import Session
from config import DevelopmentConfig  # Importa la configuración adecuada
from app.routes.main_router import configure_routes
from app.extensions import db, mail  # Importar db desde extensions
import redis

def create_app(config_class=DevelopmentConfig):
    # Crea una instancia de Flask
    app = Flask(__name__)

    # Configura la aplicación con la configuración proporcionada
    app.config.from_object(config_class)

    # Configurar Redis como backend para sesiones
    app.config['SESSION_REDIS'] = redis.StrictRedis.from_url(app.config['SESSION_REDIS_URL'])

    # Inicializar la extensión de sesiones
    Session(app)

    # Inicializar la base de datos y migraciones
    db.init_app(app)
    mail.init_app(app)
    migrate = Migrate(app, db)

    # Inicializar LoginManager
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'  # Nombre de la vista para redirigir si no se está autenticado

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user_model import User
        return User.query.get(int(user_id))

    # Registra las rutas
    configure_routes(app)

    return app
