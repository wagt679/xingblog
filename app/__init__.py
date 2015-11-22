from flask import Flask

from config import config

from flask.ext.bootstrap import Bootstrap
bootstrap = Bootstrap()

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"


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
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app
