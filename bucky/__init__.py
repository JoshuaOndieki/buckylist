from flask import Flask
from flask_login import LoginManager
from config import config

database = {}


def create_app(config_name):
    app = Flask(__name__)
    app.database = database
    app.config.from_object(config[config_name])
    login_manager = LoginManager()
    login_manager.init_app(app)
    from . import views
    app.register_blueprint(views.views)
    return app
