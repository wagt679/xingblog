from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo


__author__ = "movecloud.me"


class Conference(Form):
    name = StringField("Conference Name", validators = [DataRequired()])
#    city = SelectField()


class Login(Form):
    email = StringField("Email Address", validators = [DataRequired(), Email()])
    passwd = PasswordField("Pass Word", validators = [DataRequired()])
    submit = SubmitField("Sign In")

class Register(Form):
    email = StringField("Email Address", validators = [DataRequired(), Email()])
    nickname = StringField("Nick Name", validators = [DataRequired()])
    passwd = PasswordField('New Password', validators = [DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password',  validators = [DataRequired()])
    submit = SubmitField("Register")
