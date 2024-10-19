# Archivo: app/routes/main_router.py
from flask import render_template, redirect, url_for, flash, request, session


def configure_routes(app):
    @app.route('/')
    def hello():
       return render_template('index.html')

    # Ruta de prueba para verificar Redis
    @app.route('/session')
    def session_test():
        if 'counter' in session:
            session['counter'] = session.get('counter') + 1
        else:
            session['counter'] = 1
        return f'Sesion almacenada en Redis. Has visitado esta página {session["counter"]} veces.'