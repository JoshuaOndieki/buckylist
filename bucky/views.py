from flask import Blueprint

views = Blueprint('views', __name__)

from flask_login import current_user
from run import app
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user
from .models import User, BucketList, BucketListItem
from .forms import LoginForm, RegistrationForm


@views.route('/', methods = ['GET'])
def index():
    if current_user.is_authenticated:
        return render_template ('index.html')
    return render_template ('login.html')

@views.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form, csrf_token = False)
        if form.validate():
            user = form.username
            if user in app.database.keys() and form.password.data == app.database[user]['password']:
                print("logging")
                login_user(user)
                return redirect('/')
            flash('username or password did not match.')
            return redirect(url_for('views.login'))
        print("login unsuccessful")
    return render_template('login.html')



@views.route('/register', methods=['GET','POST'])
def register():
    """
    Usage: Creates a new user in the app
    :return:
    """
    if request.method == 'POST':
        # client is requesting to post the data to register user
        form = RegistrationForm(request.form, csrf_token = False)
        if True:
            if form.username.data not in app.database:
                print("form valid, creating user")
                user = User(form.username.data,
                            form.password.data)
                #add user to database
                app.database.setdefault(user, {})
                app.database[user].setdefault('buckets' , {})
                app.database[user]['buckets'].setdefault('detail', '')
                app.database[user]['buckets'].setdefault('items', [])
                print("user created")
                flash('Registration successful! You can log in now.')
                return redirect(url_for('views.index'))
            print("user exists")
        print("user creation unsuccessful")
        flash('Registration unsuccessful!')
    return render_template('signup.html') #c+lient is requesting for register page so render it