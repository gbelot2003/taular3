# Archivo: app/controllers/alumno_controller.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms.alumno_form import AlumnoForm
from app.repositories.alumno_repository import AlumnoRepository
from flask_login import login_required

alumno_bp = Blueprint('alumno', __name__, url_prefix='/alumnos')

@alumno_bp.route('/listar')
@login_required
def listar_alumnos():
    """Listado de todos los alumnos"""
    alumnos = AlumnoRepository.get_all()
    return render_template('alumno/listar_alumnos.html', alumnos=alumnos)

@alumno_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear_alumno():
    """Crear un nuevo alumno"""
    form = AlumnoForm()
    if form.validate_on_submit():
        AlumnoRepository.create(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            email=form.email.data,
            grado_id=form.grado_id.data
        )
        flash('Alumno creado exitosamente.', 'success')
        return redirect(url_for('alumno.listar_alumnos'))
    
    return render_template('alumno/crear_alumno.html', form=form)

@alumno_bp.route('/editar/<int:alumno_id>', methods=['GET', 'POST'])
@login_required
def editar_alumno(alumno_id):
    """Editar un alumno existente"""
    alumno = AlumnoRepository.get_by_id(alumno_id)
    if not alumno:
        flash('Alumno no encontrado.', 'danger')
        return redirect(url_for('alumno.listar_alumnos'))
    
    form = AlumnoForm(obj=alumno)
    if form.validate_on_submit():
        AlumnoRepository.update(
            alumno_id=alumno_id,
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            email=form.email.data,
            grado_id=form.grado_id.data
        )
        flash('Alumno actualizado exitosamente.', 'success')
        return redirect(url_for('alumno.listar_alumnos'))
    
    return render_template('alumno/editar_alumno.html', form=form, alumno=alumno)

@alumno_bp.route('/eliminar/<int:alumno_id>', methods=['POST'])
@login_required
def eliminar_alumno(alumno_id):
    """Eliminar un alumno"""
    success = AlumnoRepository.delete(alumno_id)
    if success:
        flash('Alumno eliminado exitosamente.', 'success')
    else:
        flash('Alumno no encontrado.', 'danger')
    return redirect(url_for('alumno.listar_alumnos'))
