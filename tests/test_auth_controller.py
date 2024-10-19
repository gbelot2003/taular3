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

        # Crear un usuario de prueba
        test_user = User(username='admin', email='admin@example.com', role=ADMINISTRATOR)
        test_user.set_password('adminpassword')
        test_user.is_verified = False
        db.session.add(test_user)
        db.session.commit()

        with app.test_client() as client:
            yield client

        db.drop_all()

def test_login_success(client):
    """Probar un inicio de sesión exitoso"""
    form_data = {'email': 'admin@example.com', 'password': 'adminpassword'}
    response = client.post(url_for('auth.login'), data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'Inicio de sesión exitoso.' in response.data.decode('utf-8')

def test_login_failure(client):
    """Probar un intento de inicio de sesión fallido"""
    form_data = {'email': 'wrong@example.com', 'password': 'wrongpassword'}
    response = client.post(url_for('auth.login'), data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'Email o contraseña incorrectos.' in response.data.decode('utf-8')

def test_logout(client):
    """Probar que el cierre de sesión funcione correctamente"""
    form_data = {'email': 'admin@example.com', 'password': 'adminpassword'}
    client.post(url_for('auth.login'), data=form_data, follow_redirects=True)
    response = client.get(url_for('auth.logout'), follow_redirects=True)
    assert response.status_code == 200
    #assert 'Has cerrado sesión correctamente.' in response.data.decode('utf-8')

    # Luego, cerrar sesión
    # response = client.get(url_for('auth.logout'), follow_redirects=True)
    # assert response.status_code == 200
    # assert 'Has cerrado sesión correctamente.' in response.data.decode('utf-8')

def test_send_verification_email(client):
    """Probar el envío de correo de verificación"""
    # Primero, iniciar sesión
    form_data = {'email': 'admin@example.com', 'password': 'adminpassword'}
    client.post(url_for('auth.login'), data=form_data, follow_redirects=True)

    # Enviar correo de verificación
    response = client.get(url_for('auth.send_verification'), follow_redirects=True)
    assert response.status_code == 200
    #assert 'Se ha enviado un enlace de verificación a tu correo electrónico.' in response.data.decode('utf-8')

def test_verify_email(client):
    """Probar la verificación del enlace de correo electrónico"""
    # Primero, iniciar sesión
    form_data = {'email': 'admin@example.com', 'password': 'adminpassword'}
    client.post(url_for('auth.login'), data=form_data, follow_redirects=True)

    # Obtener el token de verificación del usuario de prueba
    with client.application.app_context():
        user = User.query.filter_by(email='admin@example.com').first()
        token = user.generate_verification_token()

    # Verificar el token
    response = client.get(url_for('auth.verify_email', token=token), follow_redirects=True)
    assert response.status_code == 200
    assert 'Tu cuenta ha sido verificada con éxito.' in response.data.decode('utf-8')

    # Verificar que el usuario esté marcado como verificado en la base de datos
    with client.application.app_context():
        user = User.query.filter_by(email='admin@example.com').first()
        assert user.is_verified
