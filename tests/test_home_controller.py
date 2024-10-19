# -*- coding: utf-8 -*-
# Archivo: test_home_controller.py
import sys
import os

# Agregar la ruta raíz del proyecto a sys.path antes de importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))



import pytest
from flask import url_for
from app import create_app
from app.models.user_model import User
from app.forms.login_form import LoginForm
from config import TestingConfig
from app import create_app

@pytest.fixture
def client():
    app = create_app(config_class=TestingConfig)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Deshabilitar CSRF para pruebas
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['SERVER_NAME'] = 'localhost.localdomain'

    with app.test_client() as client:
        with app.app_context():
            yield client



def test_home_page(client):
    """Probar que la página de inicio es accesible"""
    response = client.get(url_for('home.home'))
    assert response.status_code == 200
    assert 'Bienvenido a Mi Proyecto' in response.data.decode('utf-8')

def test_login_success(client):
    """Probar un inicio de sesión exitoso"""
    form_data = {'email': 'admin@example.com', 'password': 'admin'}

    response = client.post(url_for('home.login'), data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'Inicio de sesión exitoso.' in response.data.decode('utf-8')

def test_login_failure(client):
    """Probar un intento de inicio de sesión fallido"""
    form_data = {'email': 'wrong@example.com', 'password': 'wrong'}

    response = client.post(url_for('home.login'), data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'Email o contraseña incorrectos.' in response.data.decode('utf-8')

def test_protected_page_without_login(client):
    """Probar acceso a una página protegida sin iniciar sesión"""
    response = client.get(url_for('home.protected'))
    assert response.status_code == 302  # Redirección a la página de login
    assert url_for('home.login') in response.headers['Location']

def test_logout(client):
    """Probar que el cierre de sesión funcione correctamente"""
    # Primero, iniciar sesión
    form_data = {'email': 'admin@example.com', 'password': 'admin'}
    client.post(url_for('home.login'), data=form_data, follow_redirects=True)

    # Luego, cerrar sesión
    response = client.get(url_for('home.logout'), follow_redirects=True)
    assert response.status_code == 200
    assert 'Has cerrado sesión correctamente.' in response.data.decode('utf-8')