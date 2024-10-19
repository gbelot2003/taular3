# archivo: app/controllers/grado_controller.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models.grado_model import Grado
from app.forms.grado_form import GradoForm
from app.extensions import db

grado_bp = Blueprint('grado', __name__, url_prefix='/grados')

@grado_bp.route('/')
def listar_grados():
    grados = Grado.query.all()
    return render_template('grado/listar.html', grados=grados)

@grado_bp.route('/crear', methods=['GET', 'POST'])
def crear_grado():
    form = GradoForm()
    if form.validate_on_submit():
        try:
            nuevo_grado = Grado(
                nombre=form.nombre.data,
                descripcion=form.descripcion.data
            )
            db.session.add(nuevo_grado)
            db.session.commit()
            flash('Grado creado exitosamente.', 'success')
            return redirect(url_for('grado.listar_grados'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el grado: {str(e)}', 'danger')

    return render_template('grado/crear.html', form=form)

@grado_bp.route('/editar/<int:grado_id>', methods=['GET', 'POST'])
def editar_grado(grado_id):
    grado = db.session.get(Grado, grado_id)  # Usar Session.get() en lugar de Query.get()
    if grado is None:
        flash('Grado no encontrado.', 'danger')
        return redirect(url_for('grado.listar_grados'))

    form = GradoForm(obj=grado)

    if form.validate_on_submit():
        try:
            grado.nombre = form.nombre.data
            grado.descripcion = form.descripcion.data
            db.session.commit()
            flash('Grado actualizado exitosamente.', 'success')
            return redirect(url_for('grado.listar_grados'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el grado: {str(e)}', 'danger')

    return render_template('grado/editar.html', form=form, grado=grado)

@grado_bp.route('/eliminar/<int:grado_id>', methods=['POST'])
def eliminar_grado(grado_id):
    grado = db.session.get(Grado, grado_id)  # Usar Session.get() en lugar de Query.get()
    if grado is None:
        flash('Grado no encontrado.', 'danger')
        return redirect(url_for('grado.listar_grados'))

    try:
        db.session.delete(grado)
        db.session.commit()
        flash('Grado eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el grado: {str(e)}', 'danger')

    return redirect(url_for('grado.listar_grados'))