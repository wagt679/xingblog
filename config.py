"""
Flask app config package.
Configration of movecloud.me 's conference
"""

import os

__author__ = "movecloud.me"

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Basic configration of app.
    """
    SECRET_KEY = os.environ.get("SECRET_KEY") or \
        "hard to guess string oidadsaanfdeefd rf ecmemxxrmercrexqwei"

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """
    Extends from Config class.
    Configration for development environment.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
