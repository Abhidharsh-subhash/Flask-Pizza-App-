import os
from decouple import config
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')


class DevConfig(Config):
    DEBUG = config('DEBUG', cast=bool)
    SQLALCHEMY_TRACK_MODIFICATION = False
    SQLALCHEMY_ECHO = True
    # for testing we uses an in memory database
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATION = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(BASE_DIR, 'db.sqlite1')


class ProdConfig(Config):
    pass


config_dict = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}
