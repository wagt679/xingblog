from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email


__author__ = "movecloud.me"


class NavLogin(Form):
    email = StringField("Email", validators = [DataRequired(), Email()])
    passwd = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField("Sign In")

class Conference(Form):
    name = StringField("Conference Name", validators = [DataRequired()])
    city = SelectField()
