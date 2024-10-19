# Archivo: app/controllers/auth_controller.py
# uff-8
from flask import Blueprint, current_app, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from app.forms.login_form import LoginForm
from app.models.user_model import User
from flask_mail import Message
from app.extensions import mail, db
from smtplib import SMTPException

auth_bp = Blueprint('auth', __name__)

# Ruta de inicio de sesión
@auth_bp.route('/login', methods=['GET', 'POST'])
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

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/send_verification')
@login_required
def send_verification():
    """Envía un correo de verificación al usuario"""
    try:
        # Generar el token de verificación
        token = current_user.generate_verification_token()
        # Crear el enlace de verificación
        verification_link = url_for('auth.verify_email', token=token, _external=True)

        # Configurar el mensaje de correo
        msg = Message(
            subject='Verifica tu correo electrónico',
            sender=current_app.config['MAIL_DEFAULT_SENDER'] or 'noreply@yourapp.com',
            recipients=[current_user.email]
        )
        msg.body = f'Para verificar tu cuenta, haz clic en el siguiente enlace: {verification_link}'
        # Enviar el correo
        mail.send(msg)

        # Informar al usuario del envío exitoso
        flash('Se ha enviado un enlace de verificación a tu correo electrónico.', 'info')
    except SMTPException as e:
        # Manejar errores en el envío de correo
        flash('No se pudo enviar el correo de verificación. Por favor, intenta de nuevo más tarde.', 'danger')
        current_app.logger.error(f'Error al enviar correo de verificación: {str(e)}')

    return redirect(url_for('home.home'))

@auth_bp.route('/verify_email/<token>')
def verify_email(token):
    """Ruta para verificar el token del correo"""
    user = User.verify_token(token)
    if user is None:
        flash('El enlace de verificación es inválido o ha expirado.', 'danger')
        return redirect(url_for('auth.login'))
    
    print(f"User before verification: {user.is_verified}")  # Debugging
    user.is_verified = True
    db.session.commit()
    print(f"User after verification: {user.is_verified}")  # Debugging
    flash('Tu cuenta ha sido verificada con éxito.', 'success')
    return redirect(url_for('home.home'))