
from . import main
from flask import render_template, url_for


@main.route('/')
def index():
    #return "<h1>hello world </h1>"
    return render_template('index.html')

@main.route("/user/<name>")
def user(name):
    return "<h1>hell world {0}</h1>".format(name)
