# Archivo: app/controllers/clase_controller.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms.clase_form import ClaseForm
from app.repositories.clase_repository import ClaseRepository
from flask_login import login_required
from app.extensions import db

clase_bp = Blueprint('clase', __name__, url_prefix='/clases')

@clase_bp.route('/listar')
@login_required
def listar_clases():
    """Listado de todas las clases"""
    clases = ClaseRepository.get_all()
    return render_template('clase/listar_clases.html', clases=clases)

@clase_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear_clase():
    """Crear una nueva clase"""
    form = ClaseForm()
    if form.validate_on_submit():
        ClaseRepository.create(
            nombre=form.nombre.data,
            grado_id=form.grado_id.data,
            maestro_id=form.maestro_id.data,
            horario_inicio=form.horario_inicio.data,
            horario_fin=form.horario_fin.data
        )
        flash('Clase creada exitosamente.', 'success')
        return redirect(url_for('clase.listar_clases'))
    
    return render_template('clase/crear_clase.html', form=form)

@clase_bp.route('/editar/<int:clase_id>', methods=['GET', 'POST'])
@login_required
def editar_clase(clase_id):
    """Editar una clase existente"""
    clase = ClaseRepository.get_by_id(clase_id)
    if not clase:
        flash('Clase no encontrada.', 'danger')
        return redirect(url_for('clase.listar_clases'))
    
    form = ClaseForm(obj=clase)
    if form.validate_on_submit():
        ClaseRepository.update(
            clase_id=clase_id,
            nombre=form.nombre.data,
            grado_id=form.grado_id.data,
            maestro_id=form.maestro_id.data,
            horario_inicio=form.horario_inicio.data,
            horario_fin=form.horario_fin.data
        )
        flash('Clase actualizada exitosamente.', 'success')
        return redirect(url_for('clase.listar_clases'))
    
    return render_template('clase/editar_clase.html', form=form, clase=clase)

@clase_bp.route('/eliminar/<int:clase_id>', methods=['POST'])
@login_required
def eliminar_clase(clase_id):
    """Eliminar una clase"""
    success = ClaseRepository.delete(clase_id)
    if success:
        flash('Clase eliminada exitosamente.', 'success')
    else:
        flash('Clase no encontrada.', 'danger')
    return redirect(url_for('clase.listar_clases'))
