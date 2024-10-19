import sys
import os

# Agregar la ruta raíz del proyecto a sys.path antes de importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import pytest
from flask import url_for
from app import create_app, db
from app.models.user_model import User, ADMINISTRATOR
from config import TestingConfig

@pytest.fixture
def client():
    app = create_app(config_class=TestingConfig)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Deshabilitar CSRF para pruebas
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['SERVER_NAME'] = 'localhost.localdomain'

    with app.app_context():
        db.create_all()

        # Crear un usuario de prueba
        test_user = User(username='admin', email='admin@example.com', role=ADMINISTRATOR)
        test_user.set_password('adminpassword')
        test_user.is_verified = True
        db.session.add(test_user)
        db.session.commit()

        with app.test_client() as client:
            yield client

        db.drop_all()

def test_home_page(client):
    """Probar que la página de inicio es accesible"""
    response = client.get(url_for('home.home'))
    assert response.status_code == 200
    assert 'Bienvenido a Mi Proyecto' in response.data.decode('utf-8')


def test_protected_page_without_login(client):
    """Probar acceso a una página protegida sin iniciar sesión"""
    response = client.get(url_for('home.protected'))
    assert response.status_code == 302  # Redirección a la página de login
    assert url_for('auth.login') in response.headers['Location']


def test_protected_page_with_login(client):
    """Probar acceso a una página protegida con sesión iniciada"""
    # Primero, iniciar sesión
    form_data = {'email': 'admin@example.com', 'password': 'adminpassword'}
    client.post(url_for('auth.login'), data=form_data, follow_redirects=True)

    # Luego, intentar acceder a la página protegida
    response = client.get(url_for('home.protected'))
    assert response.status_code == 200
    assert f'¡Hola, admin!' in response.data.decode('utf-8')
