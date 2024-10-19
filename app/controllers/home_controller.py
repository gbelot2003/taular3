# Archivo: app/controllers/home_controller.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.forms.login_form import LoginForm
from app.models.user_model import User

# Definimos el Blueprint para el controlador "home"
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('index.html', title="Página de Inicio")

# Ruta de inicio de sesión
@home_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Crear una instancia del formulario
    if form.validate_on_submit():  # Verificar si el formulario es válido
        user = User.authenticate(form.email.data, form.password.data)
        if user:
            login_user(user)
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('home.home'))  # Redirigir a la página principal
        else:
            flash('Email o contraseña incorrectos.', 'danger')

    return render_template('login.html', form=form)

@home_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('home.login'))

@home_bp.route('/protected')
@login_required
def protected():
    return f'¡Hola, {current_user.username}! Esta es una página protegida.'
