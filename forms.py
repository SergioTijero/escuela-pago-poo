from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class FormularioPago(FlaskForm):
    nombre_alumno = StringField('Nombre del Alumno', validators=[DataRequired()])
    nombre_apoderado = StringField('Nombre del Apoderado', validators=[DataRequired()])
    monto = FloatField('Monto', validators=[DataRequired()])
    concepto = StringField('Concepto', validators=[DataRequired()])
    submit = SubmitField('Registrar Pago')

class FormularioBusqueda(FlaskForm):
    busqueda = StringField('Buscar alumno por nombre o nombre del apoderado', validators=[DataRequired()])
    submit = SubmitField('Buscar')

class FormularioLogin(FlaskForm):
    nombre_usuario = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=4, max=150)])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(), Length(min=4, max=150)])
    submit = SubmitField('Iniciar Sesión')
