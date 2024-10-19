# Archivo: app/controllers/dashboard_controller.py

from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard_home():
    """
    Muestra el panel de control principal del usuario autenticado.
    """
    # Aquí se pueden obtener estadísticas u opciones de navegación desde la base de datos o realizar cálculos
    user_data = {
        'username': current_user.username,
        'email': current_user.email,
        'role': current_user.role,
        # Otros datos que desees mostrar
    }
    return render_template('dashboard.html', user_data=user_data)

@dashboard_bp.route('/dashboard/settings')
@login_required
def dashboard_settings():
    """
    Muestra la configuración del usuario autenticado.
    """
    return render_template('dashboard_settings.html')

@dashboard_bp.route('/dashboard/profile')
@login_required
def dashboard_profile():
    """
    Muestra el perfil del usuario autenticado.
    """
    return render_template('dashboard_profile.html', user=current_user)

