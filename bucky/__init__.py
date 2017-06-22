from flask import Flask
from flask_login import LoginManager
from config import config

database = {}
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    app.database = database
    app.config.from_object(config[config_name])
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(username):
        for user in app.database:
            if user.username == username:
                return user

    from . import views
    app.register_blueprint(views.views)
    return app
