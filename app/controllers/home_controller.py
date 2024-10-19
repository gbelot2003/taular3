# Archivo: app/controllers/home_controller.py
from flask import Blueprint, render_template

# Definimos el Blueprint para el controlador "home"
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('index.html', title="Página de Inicio")