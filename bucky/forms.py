from wtforms import Form, StringField, PasswordField
from wtforms.validators import Required
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    """
    A FlaskForm used to validate login form
    """
    username = StringField('username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])


class RegistrationForm(FlaskForm):
    """
    A FlaskForm used to validate the registration form
    """
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
