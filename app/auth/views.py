
from flask import render_template, redirect, flash, url_for
from . import auth
from ..main import main
from forms import Login, Register

@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        return redirect(url_for("main.index"))
    return render_template("auth/login.html", form=form)

@auth.route("/register", methods=['GET', 'POST'])
def register():
    REGISTER_HTML_PATH = "auth/register.html"
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
            return render_template(REGISTER_HTML_PATH, form=form)


        new_user = User(email=email, nickname=nickname, passwd=passwd)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash("Database Error!")
            return render_template(REGISTER_HTML_PATH, form=form)
        session["nickname"] = nickname
        return redirect(url_for("main.index"))
    return render_template(REGISTER_HTML_PATH, form=form)
