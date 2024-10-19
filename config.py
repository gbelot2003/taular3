import os
from dotenv import load_dotenv

load_dotenv(override=True)

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Configuración común a todos los entornos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')  # Ensure this is a string
    SECRET_API_TOKEN = os.getenv('SECRET_API_TOKEN') or 'default-api-token'
    MAIL_SERVER = 'localhost'   # El servidor de Mailpit
    MAIL_PORT = 1025            # El puerto SMTP de Mailpit
    MAIL_USE_TLS = False        # Sin encriptación
    MAIL_USE_SSL = False        # Sin SSL
    MAIL_USERNAME = None        # Sin autenticación
    MAIL_PASSWORD = None        # Sin autenticación
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@yourapp.com')
    
    # Configuración de Redis
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')


class DevelopmentConfig(Config):
    # Configuración específica para el entorno de desarrollo
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance/dev.db')
    DEBUG = True

class TestingConfig(Config):
    # Configuración para el entorno de pruebas
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Base de datos en memoria
    SESSION_REDIS_URL = 'redis://localhost:6379/0'
    TESTING = True
    DEBUG = False

class ProductionConfig(Config):
    # Configuración para el entorno de producción
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'instance/prod.db')
    DEBUG = False