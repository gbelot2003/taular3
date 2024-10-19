# Archivo: app/__init__.py

from flask import Flask, render_template, session
from config import DevelopmentConfig  # Importa la configuración adecuada
from flask_migrate import Migrate
from flask_session import Session
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
    
    # Crea una instancia de SQLAlchemy
    Migrate(app)


    @app.route('/')
    def hello():
       return render_template('index.html')

    # Ruta de prueba para verificar Redis
    @app.route('/session')
    def session_test():
        if 'counter' in session:
            session['counter'] = session.get('counter') + 1
        else:
            session['counter'] = 1
        return f'Sesion almacenada en Redis. Has visitado esta página {session["counter"]} veces.'
        
    return app