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
    response = client.get(url_for('clase.listar_clases'))
    assert response.status_code == 200
    assert b'Lista de Clases' in response.data

def test_crear_clase(client, setup_data):
    """Probar la creación de una nueva clase"""
    form_data = {
        'nombre': 'Matemáticas',
        'grado_id': setup_data["grado"].id,
        'maestro_id': setup_data["maestro"].id,
        'horario_inicio': datetime.strptime('08:00', '%H:%M').time(),
        'horario_fin': datetime.strptime('10:00', '%H:%M').time()
    }
    with client.application.app_context():
        response = client.post(url_for('clase.crear_clase'), data=form_data, follow_redirects=True)
        assert response.status_code == 200
        assert b'Clase creada exitosamente.' in response.data

def test_editar_clase(client, setup_data):
    """Probar la edición de una clase existente"""
    # Crear una clase para editar
    with client.application.app_context():
        clase = Clase(
            nombre="Ciencias",
            grado_id=setup_data["grado"].id,
            maestro_id=setup_data["maestro"].id,
            horario_inicio="09:00",
            horario_fin="11:00"
        )
        db.session.add(clase)
        db.session.commit()

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

def test_eliminar_clase(client, setup_data):
    """Probar la eliminación de una clase existente"""
    # Crear una clase para eliminar
    with client.application.app_context():
        clase = Clase(
            nombre="Educación Física",
            grado_id=setup_data["grado"].id,
            maestro_id=setup_data["maestro"].id,
            horario_inicio=datetime.strptime('09:00', '%H:%M').time(),
            horario_fin=datetime.strptime('11:00', '%H:%M').time()
        )
        db.session.add(clase)
        db.session.commit()

        # Eliminar la clase
        response = client.post(url_for('clase.eliminar_clase', clase_id=clase.id), follow_redirects=True)
        assert response.status_code == 200
        assert b'Clase eliminada exitosamente.' in response.data