from flask import Blueprint

views = Blueprint('views', __name__)

from run import app
from flask import render_template, redirect, request, url_for, flash
from .models import User, BucketList, BucketListItem
from .forms import LoginForm, RegistrationForm
from .helpers import get_user

@views.route('/', methods = ['GET'])
def index():
    """
    Usage: Redirects unauthorised users to login and authorised users to index
    :return:
    """
    if app.current_user is None:
        return redirect(url_for('views.login'))
    return render_template('index.html', data={'user': app.current_user})

@views.route('/login', methods=['GET','POST'])
def login():
    """
    Usage: logs a user in the app with correct credentials
    :return:
    """
    errors = []
    if request.method == 'POST':
        form = LoginForm()
        if True:  # N/B:!!! use form.validate_on_submit() !!!
            for user in app.database:
                if form.username.data == user.username and form.password.data == user.password:
                    app.current_user = user
                    return redirect('/')
            errors = ['username or password did not match.']
            print(errors)
            return render_template('login.html', data={'errors': errors })
    if app.current_user: # always send logged in users to panel with index view
        return redirect('/')
    return render_template('login.html', data={'errors': errors})



@views.route('/register', methods=['GET','POST'])
def register():
    """
    Usage: Creates a new user in the app
    :return:
    """
    errors = []
    success = None
    if request.method == 'POST':
        form = RegistrationForm()
        if True:  # N/B:!!! use form.validate_on_submit() !!!
            user_exists = get_user(form.username.data, app.database)
            if user_exists:
                errors = ['username taken']
                return render_template('signup.html', data={'errors': errors})
            else:
                user = User(form.username.data,
                            form.password.data)
                #add user to database
                app.database[user] = {}
                success = 'Registration successful! You can log in now.'
                return redirect(url_for('views.index'))
    return render_template('signup.html', data={'errors': errors, 'success': success})


@views.route('/logout', methods = ['GET', 'POST'])
def logout():
    app.current_user = None
    return redirect(url_for('views.index'))
