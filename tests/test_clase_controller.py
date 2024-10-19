# Archivo: tests/test_clase_controller.py
import datetime
import sys
import os

# Agregar la ruta raíz del proyecto a sys.path antes de importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import pytest
from flask import url_for
from app.models.grado_model import Grado
from app.models.user_model import User, TEACHER
from app.models.clase_model import Clase
from app import create_app, db
from app.extensions import mail
from config import TestingConfig
from datetime import datetime

@pytest.fixture
def client():
    """Fixture para proporcionar un cliente de pruebas de Flask"""
    app = create_app(config_class=TestingConfig)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Deshabilitar CSRF para pruebas
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['SERVER_NAME'] = 'localhost.localdomain'
    app.config['MAIL_SUPPRESS_SEND'] = True  # Evitar enviar correos en pruebas

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

@pytest.fixture
def setup_data(client):
    """Fixture para configurar los datos iniciales para las pruebas"""
    with client.application.app_context():
        # Crear un grado de prueba
        grado = Grado(nombre="Primero Básico", descripcion="Grado inicial")
        db.session.add(grado)
        db.session.commit()

        # Crear un maestro de prueba
        maestro = User(username="profesor1", email="profesor1@example.com", role=TEACHER)
        maestro.set_password("password")
        db.session.add(maestro)
        db.session.commit()

        yield {"grado": grado, "maestro": maestro}

        # Limpiar los datos después de la prueba
        db.session.delete(grado)
        db.session.delete(maestro)
        db.session.commit()

def test_listar_clases(client, setup_data):
    """Probar que la lista de clases se muestre correctamente"""
    # Autenticar al usuario
    client.post(url_for('auth.login'), data={'username': 'profesor1', 'password': 'password'}, follow_redirects=True)

    response = client.get(url_for('clase.listar_clases'))
    assert response.status_code == 200

def test_crear_clase(client, setup_data):
    """Probar la creación de una nueva clase"""
    # Autenticar al usuario
    client.post(url_for('auth.login'), data={'username': 'profesor1', 'password': 'password'}, follow_redirects=True)

    form_data = {
        'nombre': 'Matemáticas',
        'grado_id': setup_data["grado"].id,
        'maestro_id': setup_data["maestro"].id,
        'horario_inicio': datetime.strptime('08:00', '%H:%M').time(),
        'horario_fin': datetime.strptime('10:00', '%H:%M').time()
    }
    response = client.post(url_for('clase.crear_clase'), data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Clase creada exitosamente.' in response.data

    # Verificar que la clase se haya creado en la base de datos
    with client.application.app_context():
        clase = Clase.query.filter_by(nombre='Matemáticas').first()
        assert clase is not None
        assert clase.grado_id == setup_data["grado"].id
        assert clase.maestro_id == setup_data["maestro"].id
        assert clase.horario_inicio == datetime.strptime('08:00', '%H:%M').time()
        assert clase.horario_fin == datetime.strptime('10:00', '%H:%M').time()

def test_editar_clase(client, setup_data):
    """Probar la edición de una clase existente"""
    with client.application.app_context():
        # Crear una clase para editar
        horario_inicio = datetime.strptime('09:00', '%H:%M').time()
        horario_fin = datetime.strptime('11:00', '%H:%M').time()
        clase = Clase(
            nombre="Ciencias",
            grado_id=setup_data["grado"].id,
            maestro_id=setup_data["maestro"].id,
            horario_inicio=horario_inicio,
            horario_fin=horario_fin
        )
        db.session.add(clase)
        db.session.commit()

    # Autenticar al usuario
    client.post(url_for('auth.login'), data={'username': 'profesor1', 'password': 'password'}, follow_redirects=True)

    # Editar la clase
    form_data = {
        'nombre': 'Ciencias Naturales',
        'grado_id': setup_data["grado"].id,
        'maestro_id': setup_data["maestro"].id,
        'horario_inicio': datetime.strptime('08:00', '%H:%M').time(),
        'horario_fin': datetime.strptime('10:00', '%H:%M').time()
    }
    response = client.post(url_for('clase.editar_clase', clase_id=clase.id), data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Clase actualizada exitosamente.' in response.data

    # Verificar que la clase se haya actualizado en la base de datos
    with client.application.app_context():
        updated_clase = Clase.query.get(clase.id)
        assert updated_clase.nombre == 'Ciencias Naturales'
        assert updated_clase.grado_id == setup_data["grado"].id
        assert updated_clase.maestro_id == setup_data["maestro"].id
        assert updated_clase.horario_inicio == datetime.strptime('08:00', '%H:%M').time()
        assert updated_clase.horario_fin == datetime.strptime('10:00', '%H:%M').time()

def test_eliminar_clase(client, setup_data):
    """Probar la eliminación de una clase existente"""
    with client.application.app_context():
        # Crear una clase para eliminar
        horario_inicio = datetime.strptime('09:00', '%H:%M').time()
        horario_fin = datetime.strptime('11:00', '%H:%M').time()
        clase = Clase(
            nombre="Educación Física",
            grado_id=setup_data["grado"].id,
            maestro_id=setup_data["maestro"].id,
            horario_inicio=horario_inicio,
            horario_fin=horario_fin
        )
        db.session.add(clase)
        db.session.commit()

    # Autenticar al usuario
    client.post(url_for('auth.login'), data={'username': 'profesor1', 'password': 'password'}, follow_redirects=True)

    # Eliminar la clase
    response = client.post(url_for('clase.eliminar_clase', clase_id=clase.id), follow_redirects=True)
    assert response.status_code == 200
    assert b'Clase eliminada exitosamente.' in response.data

    # Verificar que la clase se haya eliminado de la base de datos
    with client.application.app_context():
        deleted_clase = Clase.query.get(clase.id)
        assert deleted_clase is None