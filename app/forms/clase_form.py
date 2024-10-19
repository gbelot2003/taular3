# Archivo: app/forms/clase_form.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TimeField, SubmitField
from wtforms.validators import DataRequired
from app.models.grado_model import Grado
from app.models.user_model import User

class ClaseForm(FlaskForm):
    nombre = StringField('Nombre de la Clase', validators=[DataRequired()])
    grado_id = SelectField('Grado', coerce=int, validators=[DataRequired()])
    maestro_id = SelectField('Maestro', coerce=int, validators=[DataRequired()])
    horario_inicio = TimeField('Horario de Inicio', validators=[DataRequired()])
    horario_fin = TimeField('Horario de Fin', validators=[DataRequired()])
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super(ClaseForm, self).__init__(*args, **kwargs)
        # Rellenar las opciones para Grado y Maestro
        self.grado_id.choices = [(g.id, g.nombre) for g in Grado.query.all()]
        self.maestro_id.choices = [(m.id, m.username) for m in User.query.filter_by(role='Maestro').all()]
