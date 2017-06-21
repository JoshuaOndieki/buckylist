from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, username


class LoginForm(Form):
    username = StringField('username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])