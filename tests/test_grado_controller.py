import sys
import os

# Agregar la ruta raíz del proyecto a sys.path antes de importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import pytest
from flask import url_for
from app import create_app, db
from app.models.grado_model import Grado
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

def test_listar_grados(client):
    """Probar que la lista de grados se muestre correctamente"""
    with client.application.app_context():
        response = client.get(url_for('grado.listar_grados'))
    assert response.status_code == 200
    assert b'Lista de Grados' in response.data

def test_crear_grado(client):
    """Probar la creación de un nuevo grado"""
    form_data = {
        'nombre': 'Primero Básico',
        'descripcion': 'Grado inicial'
    }
    with client.application.app_context():
        response = client.post(url_for('grado.crear_grado'), data=form_data, follow_redirects=True)
    assert response.status_code == 200
    #assert b'Grado creado exitosamente.' in response.data

    # Verificar que el grado se haya creado en la base de datos
    # with client.application.app_context():
    #     grado = Grado.query.filter_by(nombre='Primero Básico').first()
    #     assert grado is not None
    #     assert grado.descripcion == 'Grado inicial'

def test_editar_grado(client):
    """Probar la edición de un grado existente"""
    with client.application.app_context():
        # Crear un grado para editar
        grado = Grado(nombre='Segundo Básico', descripcion='Grado intermedio')
        db.session.add(grado)
        db.session.commit()

        # Editar el grado
        form_data = {
            'nombre': 'Segundo Básico Editado',
            'descripcion': 'Grado intermedio actualizado'
        }
        response = client.post(url_for('grado.editar_grado', grado_id=grado.id), data=form_data, follow_redirects=True)
    
    assert response.status_code == 200
    #assert b'Grado actualizado exitosamente.' in response.data  # Verificar mensaje flash

    # with client.application.app_context():
    #     # Verificar los datos actualizados en la base de datos
    #     updated_grado = db.session.get(Grado, grado.id)  # Usar Session.get() en lugar de Query.get()
    #     assert updated_grado.nombre == 'Segundo Básico Editado'
    #     assert updated_grado.descripcion == 'Grado intermedio actualizado'

def test_eliminar_grado(client):
    """Probar la eliminación de un grado existente"""
    # Crear un grado para eliminar
    with client.application.app_context():
        grado = Grado(nombre='Tercer Básico', descripcion='Grado avanzado')
        db.session.add(grado)
        db.session.commit()

        # Eliminar el grado
        response = client.post(url_for('grado.eliminar_grado', grado_id=grado.id), follow_redirects=True)
    assert response.status_code == 200
    assert b'Grado eliminado exitosamente.' in response.data

    # Verificar que el grado se haya eliminado de la base de datos
    with client.application.app_context():
        deleted_grado = db.session.get(Grado, grado.id)  # Usar Session.get() en lugar de Query.get()
        assert deleted_grado is None