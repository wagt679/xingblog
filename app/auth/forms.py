
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length
from ..models import User
from .. import db

__author__ = "movecloud.me"

class Login(Form):
    email = StringField("Email Address", validators = [DataRequired(), Length(1, 64), Email()])
    passwd = PasswordField("Pass Word", validators = [DataRequired()])
    remember_me = BooleanField("keep me logged in?")
    submit = SubmitField("Log In")

class Register(Form):
    email = StringField("Email Address", validators = [DataRequired(), Email()])
    nickname = StringField("Nick Name", validators = [DataRequired()])
    passwd = PasswordField('New Password', validators = [DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password',  validators = [DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already in using!")

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError("Nickname already in using!")
