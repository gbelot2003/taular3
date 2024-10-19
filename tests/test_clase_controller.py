# Archivo: tests/test_clase_controller.py
import sys
import os

# Agregar la ruta raíz del proyecto a sys.path antes de importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import pytest
from flask import url_for
from app import create_app, db
from config import TestingConfig

@pytest.fixture
def app():
    app = create_app(config_class=TestingConfig)
    app.config['SERVER_NAME'] = 'localhost.localdomain'  # Configuración necesaria para generar URLs
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_listar_clases(client):
    """Probar que la lista de clases se muestre correctamente"""
    with client.application.app_context():
        response = client.get(url_for('clase.listar_clases'))
    assert response.status_code == 200
    assert b'Lista de Clases' in response.data
