from flask import render_template, flash, request, redirect, session
from flask_nav.elements import Navbar, View, Subgroup
from app import app, nav
from flask.ext.security import login_required
from .models import User, MoodItem, MoodGroup, Mood
from flask_mongoengine.wtf import model_form

from wtforms import SubmitField
from flask.ext.security import current_user


@nav.navigation()
def moodnavbar():
	return (Navbar('Mood', View('Home', 'index'), 
										Subgroup("Mood view", View("Mood", "mood"), View("View Moods", "moodview"), View("Switch team", "team"),View("Statistics", "stats")),
										Subgroup("Auth", View("Login", "security.login"), View("Logout", "security.logout"),View("Change password", "security.change_password"), View("Register", "security.register"))))


@app.route("/index")
@app.route("/")
def index():
	return (render_template("index.html", title="Welcome"))


@app.route("/mood",  methods=["GET", "POST"])
@login_required
def mood():
	Moodform=model_form(Mood, only=["mood", "user"])
	Moodform.submit=SubmitField('Go')
	form=Moodform(request.form)
	if  form.validate_on_submit():
		m=Mood()
		form.populate_obj(m)
		m.save()
		flash("Thanks a lot", "success")
		return (redirect("/index"))
	return (render_template("form.html", form=form, title="How do you feel today ?"))

@app.route("/moodview")
@login_required
def moodview():
	moods=Mood.objects.all()
	return (render_template("list.html", list=moods, title="Moods"))
	
@app.route("/team",  methods=["GET", "POST"])
def team():
	return (render_template("form.html", title="team"))
	
@app.route("/stats",  methods=["GET", "POST"])
def stats():
	return (render_template("form.html", title="team"))
	