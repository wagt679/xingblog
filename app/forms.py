# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Required, Email, Length

class LoginForm(Form):
    nickname = TextField('user name', validators = [Required(), Length(max=15)])
    password = PasswordField("password", validators = [Required(), Length(max=20)])
    remember_me = BooleanField('remember_me', default = False)
    submit = SubmitField("登录")

class SignUpForm(Form):
    nickname = TextField('user name', validators = [Required(), Length(max=15)])
    email = TextField('email', validators=[Email(), Required(), Length(max=128)])
    password = PasswordField("password", validators = [Required(), Length(max=20)])
    re_password = PasswordField("re_password", validators = [Required(), Length(max=20)])
    agree = BooleanField('agree', default = False)

    submit = SubmitField('注册')

class PublishBlogForm(Form):
    title = TextField("title", validators = [Required(), Length(max =100)])
    body = TextAreaField("blog content", validators=[Required()])
    submit = SubmitField('发表文章')

class AboutMeForm(Form):
    describe = TextAreaField('about me', validators=[Required(), Length(max=140)])
    submit = SubmitField("yes!")

class EditForm(Form):
    nickname = TextField("nickname", validators = [Required(), Length(max=15)])
    about = TextAreaField("about me", validators=[Length(min=0, max=140)])
    submit = SubmitField("保存")
