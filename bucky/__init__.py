from flask import Flask

database = {}

def create_app():
    app = Flask(__name__)
    app.database = database
    # register my urls here
    from . import views
    app.register_blueprint(views.views)
    return app