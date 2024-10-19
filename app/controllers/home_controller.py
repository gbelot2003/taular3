# Archivo: app/controllers/home_controller.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.models.user_model import User

# Definimos el Blueprint para el controlador "home"
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('index.html', title="Página de Inicio")

# Ruta de inicio de sesión
@home_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.authenticate(username, password)
        if user:
            login_user(user)
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('hello'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')

    return render_template('login.html')

@home_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('login'))