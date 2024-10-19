import sys
import os

# Agregar la ruta raíz del proyecto a sys.path antes de importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import pytest
from config import TestingConfig
from app import create_app

@pytest.fixture
def client():
    # Crear una aplicación de prueba con el entorno de pruebas
    app = create_app(config_class=TestingConfig)
    app.config['TESTING'] = True  # Activar el modo de pruebas para Flask

    with app.test_client() as client:
        yield client

def test_server_is_running(client):
    # Verificar que el servidor responde en la ruta principal "/"
    response = client.get('/')
    assert response.status_code == 200  # Verifica que la respuesta sea exitosa (200 OK)
    assert b'Bienvenido a Mi Proyecto' in response.data  # Verifica que el contenido esperado esté en la respuesta

def test_session_endpoint(client):
    # Verificar que el servidor responde en la ruta "/session"
    response = client.get('/session')
    assert response.status_code == 200  # Verifica que la respuesta sea exitosa (200 OK)
    assert b'Sesion almacenada en Redis' in response.data  # Verifica que el contenido esperado esté en la respuesta
