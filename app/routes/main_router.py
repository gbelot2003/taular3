# Archivo: app/routes/main_router.py
from flask import render_template, redirect, url_for, flash, request, session
from app.controllers.home_controller import home_bp

def configure_routes(app):
    
    # Registrar los Blueprints
    app.register_blueprint(home_bp)


    # Ruta de prueba para verificar Redis
    @app.route('/session')
    def session_test():
        if 'counter' in session:
            session['counter'] = session.get('counter') + 1
        else:
            session['counter'] = 1
        return f'Sesion almacenada en Redis. Has visitado esta página {session["counter"]} veces.'