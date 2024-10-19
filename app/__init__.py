# Archivo: app/__init__.py

from flask import Flask, render_template, session
from flask_login import LoginManager
from config import DevelopmentConfig  # Importa la configuración adecuada
from flask_migrate import Migrate
from flask_session import Session
from app.routes.main_router import configure_routes
from app.models.user_model import User  # Importar el modelo de usuario
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

    login_manager = LoginManager(app)
    login_manager.login_view = 'login'  # Nombre de la vista para redirigir si no se está autenticado

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)  # Método para cargar usuario por ID

    # Crea una instancia de SQLAlchemy
    Migrate(app)

    # Registra las rutas
    configure_routes(app)

        
    return app