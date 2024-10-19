# Archivo: tests/test_dashboard_controller.py
import sys
import os

# Agregar la ruta raíz del proyecto a sys.path antes de importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import pytest
from flask import url_for
from app import create_app, db
from app.models.user_model import User, ADMINISTRATOR
from config import TestingConfig
from flask_mail import Mail

@pytest.fixture
def client():
    app = create_app(config_class=TestingConfig)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Deshabilitar CSRF para pruebas
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['SERVER_NAME'] = 'localhost.localdomain'
    app.config['MAIL_SUPPRESS_SEND'] = True  # Evitar enviar correos en pruebas

    mail = Mail(app)

    with app.app_context():
        db.create_all()

        yield app.test_client()

        db.drop_all()

@pytest.fixture
def authenticated_client(client):
    # Crear un usuario de prueba
    test_user = User(username='admin', email='admin@example.com', role=ADMINISTRATOR)
    test_user.set_password('adminpassword')
    test_user.is_verified = True
    with client.application.app_context():
        db.session.add(test_user)
        db.session.commit()

    # Iniciar sesión como el usuario de prueba
    form_data = {'email': 'admin@example.com', 'password': 'adminpassword'}
    client.post(url_for('auth.login'), data=form_data, follow_redirects=True)

    return client

def test_dashboard_access(authenticated_client):
    """Probar acceso al dashboard con usuario autenticado"""
    response = authenticated_client.get(url_for('dashboard.dashboard_home'))
    assert response.status_code == 200
    assert 'Bienvenido al Panel de Control' in response.data.decode('utf-8')

def test_dashboard_settings_access(authenticated_client):
    """Probar acceso a las configuraciones del dashboard con usuario autenticado"""
    response = authenticated_client.get(url_for('dashboard.dashboard_settings'))
    assert response.status_code == 200
    assert 'Configuraciones de Usuario' in response.data.decode('utf-8')

def test_dashboard_profile_access(authenticated_client):
    """Probar acceso al perfil del dashboard con usuario autenticado"""
    response = authenticated_client.get(url_for('dashboard.dashboard_profile'))
    assert response.status_code == 200
    assert 'Perfil de Usuario' in response.data.decode('utf-8')
