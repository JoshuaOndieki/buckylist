from wtforms import Form, StringField, PasswordField
from wtforms.validators import Required
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    """
    A FlaskForm used to validate login form
    """
    username = StringField('username', validators=[Required()])
    password = PasswordField('password', validators=[Required()])


class RegistrationForm(FlaskForm):
    """
    A FlaskForm used to validate the registration form
    """
    username = StringField('username', validators=[Required()])
    password = PasswordField('password', validators=[Required()])


class BucketForm(FlaskForm):
    """
    A FlaskForm used to validate the bucket form
    """
    name = StringField('name', validators=[Required()])
    description = StringField('description', validators=[Required()])
