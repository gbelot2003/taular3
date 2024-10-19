from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.forms.login_form import LoginForm
from app.models.user_model import User

# Definimos el Blueprint para el controlador "home"
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('index.html', title="Página de Inicio")

@home_bp.route('/protected')
@login_required
def protected():
    return f'¡Hola, {current_user.username}! Esta es una página protegida.'
