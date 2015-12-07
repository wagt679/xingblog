
from datetime import datetime

from forms import *
import forms
from flask import render_template, url_for, redirect, flash, session, request, current_app
from flask.ext.login import login_required, current_user

from . import main
from ..models import User, Topic, City, Conference
from .. import db


@main.route('/', methods=['GET', 'POST'])
def index():
    nickname = session.get("nickname", None)
    if nickname:
        flash("Hello %s" % nickname)
    return render_template('index.html')

@main.route("/show_conference", methods=['GET', 'POST'])
def show_conference():
    page = request.args.get("page", 1, type=int)
    pagination = Conference.query.order_by(Conference.time_stamp.desc()) \
                    .paginate(page, per_page=current_app.config["FLASKY_POSTS_PER_PAGE"], error_out=False)
    conferences = pagination.items
    return render_template('show_conference.html', conferences=conferences, pagination=pagination)

@main.route("/create_conference", methods=["GET", "POST"])
def create_conference():
    if (not current_user.is_authenticated):
        flash("Login to create a conference!")
        return redirect(url_for("auth.login"))
    
    form = forms.Conference()
    if form.validate_on_submit():

        title = form.title.data
        description = form.description.data
        city_id = form.city.data
        topic_ids = form.topics.data
        stime = form.start_time.data
        etime = form.end_time.data
        max_attendees = form.max_attendees.data
        time_stamp = datetime.utcnow()
        
        new_conf = Conference(
            organizer = current_user,
            title = title,
            city = City.query.filter_by(id = city_id).first(),
            description = description,
            start_time = stime,
            end_time = etime,
            max_attendees = max_attendees,
            time_stamp = time_stamp
        )
        for topic_id in topic_ids:
            new_conf.topics.append(Topic.query.filter_by(id=topic_id).first())
        
        db.session.add(new_conf)
        db.session.commit()
        
        flash("New conference is created!")
        
        return redirect(url_for("main.index"))

    allowable_topics = [(topic.id, topic.name) for topic in Topic.query.all()]
    allowable_cities = [(city.id, city.name) for city in City.query.all()] 
    form.city.choices = allowable_cities
    form.topics.choices = allowable_topics
    
    return render_template('create_conference.html', form=form)

@main.route("/conference/<int:id>", methods=["GET", "POST"])
def conference(id):
    conference = Conference.query.filter_by(id=id).first()
    return render_template("conference_context.html", conference=conference)

@main.route("/profile")
def profile():
    return "<h1>hell world</h1>"
