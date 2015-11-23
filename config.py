"""
Flask app config package.
Configration of xing conference
"""

import os
import random
import string

__author__ = "movecloud.me"

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Basic configration of app.
    """
    SECRET_KEY = os.environ.get("SECRET_KEY") or \
        "".join(random.choice(string.letters) for x in xrange(100))
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 994
    MAIL_USE_SSL = True
    MAIL_USERNAME = "lianyun08"        # os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = "movecloud1234"
    FLASKY_MAIL_SUBJECT_PREFIX = '[Xing]'
    FLASKY_MAIL_SENDER = 'Xing Admin <lianyun08@126.com>'

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
