import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True

    # not a real secret, for dev use only
    SECRET_KEY = "He3NhGf7r2wq6zfrmRWPeCXBXrXJvRNF0fDudJv+x0k="

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class TestConfig(BaseConfig):
    DEBUG = False
    Testing = True
