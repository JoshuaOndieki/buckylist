from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import Required, username


class LoginForm(Form):
    username = StringField('username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])