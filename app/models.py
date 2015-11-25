# _*_ coding: utf-8 _*_

from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime

from . import db, login_manager

class Permission:
    """
    0b00000001: 关注
    0b00000010: 评论
    0b00000100: 写文章
    0b00001000: 管理他人的评论
    0b00010000: 管理员权限
    """
    FOLLOW = 0x01
    COMMIT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMITS = 0x08
    ADMINISTER = 0x08

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    nickname = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    conferences = db.relationship("Conference", backref="sponsor", lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config["XING_ADMIN"]:
                self.role = Role.query.filter_by(permissions = 0xff).first()
            else:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, permission):
        """
        Verify this user's role.
        If this user has permission required, return true, vise vese.
        """
        return (self.role is not None) and \
            ((self.role.permissions & permission) == permission)

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    @property
    def passwd(self):
        raise AttributeError("Password is not a readable attribute")

    @passwd.setter
    def passwd(self, passwd):
        self.password_hash = generate_password_hash(passwd)

    def verify_passwd(self, passwd):
        return check_password_hash(self.password_hash, passwd)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):

        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get("confirm") == self.id:
            self.confirmed = True
            db.session.add(self)
            return True
        return False

    def __str__(self):
        return "<User %s>" % self.nickname

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return True

login_manager.anonymous_user = AnonymousUser

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", backref="role", lazy="dynamic")

    @staticmethod
    def insert_roles():
        roles = {
            "User" : (Permission.FOLLOW |
                      Permission.COMMIT |
                      Permission.WRITE_ARTICLES, True),
            "Moderator" : ( Permission.FOLLOW |
                            Permission.COMMIT |
                            Permission.WRITE_ARTICLES |
                            Permission.MODERATE_COMMITS, False),
            "Administrator" : (0xff, False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()
    def __str__(self):
        return self.name

    __repr__ = __str__


class Conference(db.Model):
    __tablename__ = "conferences"
    id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.String(128), index=True, nullable=False)
    city = db.Column(db.String(128))
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    max_attendees = db.Column(db.Integer)
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return "<Conference %s>" % name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
