import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'secret'



class DevelopmentConfig(Config):
    WTF_CSRF_ENABLED = False
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    WTF_CSRF_ENABLED = False
    DEBUG = True


config = {
'development': DevelopmentConfig,
'testing': TestingConfig,
'production': ProductionConfig,
}
