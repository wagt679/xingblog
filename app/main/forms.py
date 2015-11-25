from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, SelectMultipleField,\
    DateTimeField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime


__author__ = "movecloud.me"


class Conference(Form):
    name = StringField("Conference Name", validators = [DataRequired()])
    city = SelectField("City", choices=[("1","AA"), ("2", "BB")])
    description = TextAreaField("Conference description")
    topics = SelectMultipleField("Topics", choices = [("1", "DD"), ("2", "EE"), ("3", "VV")])
    start_time = DateTimeField("Start Time (%Y-%m-%d %H:%M:%S)", format="%Y-%m-%d %H:%M:%S", default=datetime.now())
    end_time = DateTimeField("End Time (%Y-%m-%d %H:%M:%S)", format="%Y-%m-%d %H:%M:%S", default=datetime.now())
    max_attendees = IntegerField("Max Attendees", default=0)
    submit = SubmitField("Publish")
