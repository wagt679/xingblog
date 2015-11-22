

from . import main
from forms import *
from flask import render_template, url_for, redirect, flash, session

from ..models import User
from .. import db


@main.route('/', methods=['GET', 'POST'])
def index():
    nickname = session.get("nickname", None)
    if nickname:
        flash("Hello %s" % nickname)
    return render_template('index.html')

@main.route('/show_conf')
def show_conf():
    #return "<h1>hello world </h1>"
    return render_template('base.html')

@main.route("/create_conf")
def create_conf():
    return "<h1>hell world </h1>"

@main.route("/profile")
def profile():
    return "<h1>hell world</h1>"

@main.route("/login", methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        return redirect(url_for(".index"))
    return render_template("login.html", form=form)

@main.route("/register", methods=['GET', 'POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        email = form.email.data
        nickname = form.nickname.data
        passwd = form.passwd.data
        confirm = form.confirm.data
        #if passwd != confirm:
        #    flash("password is not equal")
        #    return render_template("register.html", form=form)


        u1s = User.query.filter_by(email=email).first()
        u2s = User.query.filter_by(nickname=nickname).first()
        if u1s:
            flash("Your email have been registed!")
        if u2s:
            flash("Your nickname have been registed!")
        if u1s or u2s:
            return render_template("register.html", form=form)


        new_user = User(email=email, nickname=nickname, passwd=passwd)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash("Database Error!")
            return render_template("register.html", form=form)
        session["nickname"] = nickname
        return redirect(url_for(".index"))
    return render_template("register.html", form=form)
