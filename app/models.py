
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

from . import login_manager

from . import db

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    nickname = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def passwd(self):
        raise AttributeError("Password is not a readable attribute")

    @passwd.setter
    def passwd(self, passwd):
        self.password_hash = generate_password_hash(passwd)

    def verify_passwd(self, passwd):
        return check_password_hash(self.password_hash, passwd)


    def __str__(self):
        return "<User %s>" % self.nickname

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
