from flask import Flask
from flask_login import LoginManager
from config import config


database = {} # multi dimentional dict storing application data in form of objects
current_user = None # use current_user to check logged in user
login_manager = LoginManager()

def create_app(config_name):
    """
    Usage: Factory function used to setup the application instance
    :return: application instance
    """
    app = Flask(__name__)
    app.database = database
    app.current_user = current_user
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


"""
``````````````````````````DATA structure
{
    user_object:
                {
                    BucketList_object:
                                        [
                                            item_object, item_object,..
                                        ]
                }

}
"""
