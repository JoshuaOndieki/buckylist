from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegistrationForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
