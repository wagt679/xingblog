

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
