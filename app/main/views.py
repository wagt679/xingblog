

from . import main
from forms import *
from flask import render_template, url_for, redirect, flash, session
from flask.ext.login import login_required

from ..models import User
from .. import db


@main.route('/', methods=['GET', 'POST'])
def index():
    nickname = session.get("nickname", None)
    if nickname:
        flash("Hello %s" % nickname)
    return render_template('index.html')

@main.route('/show_conf', methods=['GET', 'POST'])
@login_required
def show_conf():
    form = Conference()
    if form.validate_on_submit():
        s1 = form.city.data     # the value "1"
        s2 = form.topics.data   # the value list = [u"1", u"2"]
        flash("date: {0}, {1}".format(s1 , s2))
        return redirect(url_for("main.index"))

    return render_template('show_conference.html', form=form)

@main.route("/create_conf")
def create_conf():
    return "<h1>hell world </h1>"

@main.route("/profile")
def profile():
    return "<h1>hell world</h1>"
