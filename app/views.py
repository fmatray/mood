from flask import render_template, flash, request, redirect, session
from flask_nav.elements import Navbar, View, Subgroup
from app import app, nav
from flask.ext.security import login_required
from .models import User, Mood
from flask_mongoengine.wtf import model_form

@nav.navigation()
def moodnavbar():
	return (Navbar('Mood', View('Home', 'index'), 
										Subgroup("Mood view", View("Mood", "mood"), View("Switch team", "team"),View("Statistics", "stats")),
										Subgroup("Auth", View("Login", "security.login"), View("Logout", "security.logout"),View("Change password", "security.change_password"), View("Register", "security.register"))))

@app.route("/index")
@app.route("/")
def index():
	return (render_template("index.html", title="Welcome"))

@app.route("/mood",  methods=["GET", "POST"])
@login_required
def mood():
	form=model_form(Mood)
	if  request.method == 'POST' and form.validate():
		flash("Thanks a lot", "success")
		return (redirect("/index"))
	return (render_template("form.html", form=form, title="How do you feel today ?"))

@app.route("/team",  methods=["GET", "POST"])
def team():
	return (render_template("form.html", title="team"))
	
@app.route("/stats",  methods=["GET", "POST"])
def stats():
	return (render_template("form.html", title="team"))
	