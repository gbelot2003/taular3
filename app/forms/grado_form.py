from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class GradoForm(FlaskForm):
    nombre = StringField('Nombre del Grado', validators=[DataRequired(), Length(max=100)])
    descripcion = TextAreaField('Descripción', validators=[Length(max=255)])
    submit = SubmitField('Guardar')