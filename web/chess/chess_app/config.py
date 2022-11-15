class Config(object):
    SECRET_KEY = '736670cb10a600b695a55839ca3a5aa54a7d7356cdef815d2ad6e19a2031182b'

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://../database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    DEBUG = True
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
