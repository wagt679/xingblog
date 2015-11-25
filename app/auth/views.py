
from flask import render_template, redirect, flash, url_for, request, session
from flask.ext.login import login_user, logout_user, login_required, \
    current_user


from . import auth
from ..main import main
from ..models import User
from ..email import send_async_email
from .. import db
from forms import Login, Register

@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u and u.verify_passwd(form.passwd.data):
            login_user(u, form.remember_me.data)
            flash("Logged in successfully.")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("main.index"))
        flash("Invalid username or password.")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for("main.index"))


@auth.route("/register", methods=['GET', 'POST'])
def register():
    REGISTER_HTML_PATH = "auth/register.html"
    form = Register()
    if form.validate_on_submit():
        email = form.email.data
        nickname = form.nickname.data
        passwd = form.passwd.data
        confirm = form.confirm.data

        new_user = User(email=email, nickname=nickname, passwd=passwd)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash("Database Error!")
            return render_template(REGISTER_HTML_PATH, form=form)
        token = new_user.generate_confirmation_token()
        send_async_email(new_user.email, "Confirm Your Account", "auth/email/confirm",\
            user=new_user, token=token)  # to,  subject, template, **kwargs
        flash('A confirmation email has been sent to you by email.')
        session["nickname"] = nickname
        return redirect(url_for("main.index"))
    return render_template(REGISTER_HTML_PATH, form=form)

@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if not current_user.confirmed:
        if current_user.confirm(token):
            flash("You have confirmed your account!")
        else:
            flash("The confirmation link is invalid or has expired.")
    return redirect(url_for("main.index"))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.endpoint[:5] != "auth."\
        and request.endpoint != 'static':
        return redirect(url_for("auth.unconfirmed"))

@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("main.index"))
    return render_template("auth/unconfirmed.html")

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_async_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))
