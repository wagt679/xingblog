from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy

from config import config


bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
    """
    1. I create app in a function and register it with blueprint, so we can
       create several different app object using different configration.
       This make unit test very easy.
    2. Most of app have different configration in dev environment and online environment.

    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
