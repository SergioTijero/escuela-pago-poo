# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.numeric import FloatField
from wtforms.validators import DataRequired, Length

class PaymentForm(FlaskForm):
    student_name = StringField('Student Name', validators=[DataRequired()])
    guardian_name = StringField('Guardian Name', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    concept = StringField('Concept', validators=[DataRequired()])
    submit = SubmitField('Add Payment')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=150)])
    submit = SubmitField('Login')
