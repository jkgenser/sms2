import os

class DefaultConfig(object):
    SECRET_KEY = 'secret_key'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]


class DevelopmentConfig(DefaultConfig):
    Debug = True
