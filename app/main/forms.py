from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


__author__ = "movecloud.me"


class Conference(Form):
    name = StringField("Conference Name", validators = [DataRequired()])
#    city = SelectField()
