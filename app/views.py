# -*- coding:utf-8 -*-

import datetime
from string import strip

from app import blog
from forms import LoginForm, SignUpForm, AboutMeForm, PublishBlogForm, EditForm
from flask import (render_template, flash, redirect, session, url_for, request, g)
from flask.ext.login import (login_user, logout_user, current_user, login_required)
from flask_mail import Message


from markdown import markdown
import bleach


from models import User, ROLE_USER, ROLE_ADMIN, Post

from app import blog, db, lm, mail


from utils import *


@blog.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user_name = request.form.get('nickname')
        pw = request.form.get('password')

        user = User.login_check(user_name, pw)
        if user:
            login_user(user)
            user.last_seen = datetime.datetime.now()

            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash("The DataBase Error")
                return redirect('/login')

            flash('Your Name: ' + request.form.get('nickname'))
            flash('remember me? ' + str(request.form.get('remember_me')))
            return redirect(url_for('index'))
        else:
            flash("Login failed, your name is not exist!")
            return redirect(url_for("login"))

    return render_template('login.html',
                           title='Sign In',
                           form=form)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))  # convert unicode to int


@blog.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@blog.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()

    if form.validate_on_submit():
        nickname = request.form.get("nickname")
        email = request.form.get("email")
        pw = request.form.get("password")
        re_pw = request.form.get("re_password")

        name_email_check = User.query.filter(db.or_(User.nickname == nickname, User.email == email)).first()
        if name_email_check:
            flash("错误: 用户名或者邮件地址已经存在！")
            return redirect(url_for("sign_up"))

        pw_check = (pw != re_pw)

        if pw_check:
            flash("两次输入的密码不相同！")
            return redirect(url_for("sign_up"))

        import helperlib
        if len(nickname) and len(email):
            user = User()
            user.nickname = nickname
            user.email = email
            user.password = helperlib.make_pw_hash(nickname, pw)
            user.role = ROLE_USER

            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash("数据库错误！")
                return redirect(url_for("sign_up"))

            msg = Message("欢迎您来到行博", sender="bjliany@163.com", recipients=[email])
            msg.body = """欢迎您来到行博。
                    我是行博CEO 行云。
                    您注册的账户名称是:{0}
                    祝您开心健康每一天！""".format(nickname)
            import helperlib
            helperlib.send_mail_async(mail, msg)

            flash("注册成功！注册邮件稍后发送至您的邮箱。")
            logout_user()
            return redirect(url_for("login"))
    return render_template(
        "sign_up.html",
        form = form)

# 博客首页
@blog.route("/", defaults={"page": 1}, methods=["GET"])
@blog.route("/index/page/<int:page>", methods=["GET"])
@blog.route('/index', defaults={"page": 1}, methods=["GET"])
def index(page):
    pagination = Post.query.order_by(
        db.desc(Post.timestamp)
        ).paginate(page, INDEX_PER_PAGE, False)
    return render_template('index.html',
                           title='Home',
                           pagination=pagination)

# 用户的个人主页
@blog.route("/user/<int:user_id>", defaults={"page": 1}, methods=["POST", "GET"])
@blog.route("/user/<int:user_id>/page/<int:page>", methods=["GET", "POST"])
@login_required     # must login
def user(user_id, page): # userid is got by url
    form = AboutMeForm()

    user = User.query.filter(User.id == user_id).first()
    # get user from database

    if not user:        # not find the user required
        flash("您访问的用户不存在！")
        return redirect(url_for("/index"))   # convert to index page

    # posts = user.posts.all()
    # posts = user.posts.paginate(page, PER_PAGE, False).items
    pagination = Post.query.filter_by(
        user_id = current_user.id
        ).order_by(
        db.desc(Post.timestamp)
        ).paginate(page, USER_PER_PAGE, False)

    return render_template(
        "user.html",
        form=form,
        pagination=pagination)

# 发表文章页
@blog.route("/publish/<int:user_id>", methods=["POST", "GET"])
@login_required
def publishs(user_id):

    form = PublishBlogForm()

    if form.validate_on_submit():
        post_title = request.form.get("title")
        post_body = request.form.get("body")
        if not len(strip(post_body)) or not len(strip(post_title)):
            flash("不能提交空内容！")
            return redirect(url_for("publish", user_id=user_id))

        post = Post()
        post.body = bleach.linkify(bleach.clean(
            markdown(post_body, out_format='html'), strip = True))
        post.title = post_title
        post.timestamp = datetime.datetime.now()
        post.user_id = user_id


        try:
            db.session.add(post)
            db.session.commit()
        except:
            flash("DataBase error!")
            return redirect(url_for("publish", user_id=user_id))

        return redirect(url_for("user", user_id=user_id))

    return render_template(
        "publish.html",
        form = form)

# 用户编辑个人资料页
@blog.route("/edit/<int:user_id>", methods=["POST", "GET"])
@login_required
def edit(user_id):
    if user_id != current_user.id:
        return redirect(url_for("edit", user_id = current_user.id))
    user = User.query.filter(User.id == user_id).first()
    form = EditForm()

    if form.validate_on_submit():
        new_nickname = request.form.get("nickname")
        new_about = request.form.get("about")

        user.nickname = new_nickname
        user.about = new_about

        try:
            db.session.add(user)
            db.session.commit()
        except:
            flash("The DataBase Error")
            # return redirect(url_for('/edit/'+str(user_id)))

        flash("你的个人信息已经被更新!")
        return redirect(url_for("edit", user_id=user_id))

    else:
        form.nickname.data = user.nickname
        form.about.data = user.about

    return render_template(
        "edit.html",
        form = form)
