
from . import main
from forms import *
from flask import render_template, url_for, redirect, flash


@main.route('/', methods=['GET', 'POST'])
def index():
    #return "<h1>hello world </h1>"
    form = NavLogin()
    if form.validate_on_submit():
        email = form.email.data
        passwd = form.passwd.data
        flash("you email is: " + email)
        return redirect(url_for(".index"))

    return render_template('index.html', form=form)

@main.route("/user/<name>")
def user(name):
    return "<h1>hell world {0}</h1>".format(name)

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
