from flask import Flask
from flask-login import LoginManger

database = {}

def create_app():
    app = Flask(__name__)
    app.database = database
    login_manager = LoginManager()
    login_manager.init_app(app)
    from . import views
    app.register_blueprint(views.views)
    return app