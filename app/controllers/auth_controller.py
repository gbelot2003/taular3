from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app.models.user_model import User
from flask_mail import Message
from app.extensions import mail

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/send_verification')
@login_required
def send_verification():
    """Envía un correo de verificación al usuario"""
    token = current_user.generate_verification_token()
    verification_link = url_for('auth.verify_email', token=token, _external=True)
    msg = Message('Verifica tu correo electrónico',
                  sender='noreply@yourapp.com',
                  recipients=[current_user.email])
    msg.body = f'Para verificar tu cuenta, haz clic en el siguiente enlace: {verification_link}'
    mail.send(msg)
    flash('Se ha enviado un enlace de verificación a tu correo electrónico.', 'info')
    return redirect(url_for('home.home'))

@auth_bp.route('/verify_email/<token>')
def verify_email(token):
    """Ruta para verificar el token del correo"""
    user = User.verify_token(token)
    if user is None:
        flash('El enlace de verificación es inválido o ha expirado.', 'danger')
        return redirect(url_for('auth.login'))
    user.is_verified = True
    db.session.commit()
    flash('Tu cuenta ha sido verificada con éxito.', 'success')
    return redirect(url_for('home.home'))
