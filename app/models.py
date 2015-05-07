# -*- coding: utf-8 -*-
from hashlib import md5

from app import db

ROLE_USER = 0
ROLE_ADMIN = 1
AVATAR_DEFAULT=["", "mm", "identicon", "monsterid", "wavatar", "retro"]
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(300), index = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = db.relationship('Post', backref = "author", lazy='dynamic')
    about = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    #portrait = db.Column(db.LargeBinary)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def avatar(self, size):
        from random import choice
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + "?d="+ choice(AVATAR_DEFAULT)+"&s=" + str(size)

    @classmethod
    def login_check(cls, user_name, pw):
        """
        验证用户名和密码
        如果成功，返回user
        否则返回None
        """
        user = cls.query.filter(User.nickname==user_name).first()
        name = user.nickname
        h = user.password
        import helperlib
        if helperlib.valid_pw(name, pw, h):
            return user
        else:
            return None


    def __repr__(self):
        return "<User %r>" % (self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(400))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {0}>'.format(self.body)
