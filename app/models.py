# _*_ coding: utf-8 _*_

from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
import datetime

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
    conferences = db.relationship("Conference", backref="organizer", lazy='dynamic')

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
    
    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        
        import forgery_py
        seed()
        for i in xrange(count):
            u = User(
                email = forgery_py.internet.email_address(),
                nickname = forgery_py.internet.user_name(True),
                passwd = forgery_py.lorem_ipsum.word(),
                confirmed = True
            )
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                

    def __str__(self):
        return "<User %s>" % self.nickname
    
        
    __repr__ = __str__

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
        return "<Role %s>" % self.name

    __repr__ = __str__

class City(db.Model):
    __tablename__ = "cities"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(128), unique=True, index=True)
    name = db.Column(db.String(128), unique=True)
    conferences = db.relationship("Conference", backref="city", lazy="dynamic")
    
    @staticmethod
    def insert_cities():
        cities = {
            "xi_an": "Xi An",
            "bei_jing": "Bei Jing",
            "shang_hai": "Shang Hai"
        }
        for (value, name) in cities.items():
            city = City.query.filter_by(value=value).first()
            if city is None:
                city = City(value=value, name=name)
                db.session.add(city)
        db.session.commit()
    
    def __str__(self):
        return "<City %s>" % self.name
    
        
    __repr__ = __str__
            
    
class Topic(db.Model):
    __tablename__ = "topics"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(128), unique=True, index=True)
    name = db.Column(db.String(128), unique=True)
    
    @staticmethod
    def insert_topics():
        topics = {
            "programming": "Programming",
            "web": "Web",
            "movie": "Movie",
            "health": "Health"
        }
        for (value, name) in topics.items():
            topic = Topic.query.filter_by(value=value).first()
            if topic is None:
                topic = Topic(value=value, name=name)
                db.session.add(topic)
        db.session.commit()
    
    def __str__(self):
        return "<Topic %s>" % self.name
        
    __repr__ = __str__


add_topics = db.Table('add_topics', \
                        db.Column("conference_id", db.Integer, db.ForeignKey("conferences.id")),
                        db.Column("topic_id", db.Integer, db.ForeignKey("topics.id")))

class Conference(db.Model):
    __tablename__ = "conferences"
    id = db.Column(db.Integer, primary_key=True)
    organizer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String(128), index=True, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey("cities.id"))
    topics = db.relationship("Topic", secondary=add_topics, backref=db.backref("conferences", lazy="dynamic"), lazy="dynamic")
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    max_attendees = db.Column(db.Integer)
    time_stamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    attendees = db.Column(db.Integer)

    def __str__(self):
        return "<Conference %s>" % self.title
    
    __repr__ = __str__
    
    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        
        seed()
        user_count = User.query.count()
        city_count = City.query.count()
        topic_count = Topic.query.count()
        delta_time = datetime.timedelta(days=1)
        
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            c = City.query.offset(randint(0, city_count - 1)).first()
            t = forgery_py.lorem_ipsum.sentence()
            tps = []
            for ii in xrange(randint(0, 5)):
                tps.append(Topic.query.offset(randint(0, topic_count-1)).first())
            stime = forgery_py.date.date(True)
            etime = stime + delta_time
            des = forgery_py.lorem_ipsum.sentences(randint(1, 3))
            max_attendees = randint(5, 25)
            attendees = max_attendees - randint(0, max_attendees)
            time_stamp = forgery_py.date.date(True)
            
            conference = Conference(
                organizer = u,
                city = c,
                title = t,
                description = des,
                start_time = stime,
                end_time = etime,
                max_attendees = max_attendees,
                attendees = attendees,
                time_stamp = time_stamp
            )
            
            for t in tps:
                conference.topics.append(t)
            db.session.add(conference)
        
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
