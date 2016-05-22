from flask import render_template, flash, request, redirect, session
from flask_nav.elements import Navbar, View, Subgroup
from app import app, nav
from .forms import MoodForm, LoginForm, SignUpForm
from .models import User

@nav.navigation()
def moodnavbar():
	return (Navbar('Mood', View('Home', 'index'), 
										Subgroup("Log", View('Login', "login"), View("Logout", "logout"), View("Sign up", "signup")), 
										Subgroup("Mood view", View("Mood", "mood"), View("Switch team", "team"),View("Statistics", "stats"))))

@app.route("/index")
@app.route("/")
def index():
	return (render_template("index.html", title="Welcome"))

@app.route("/mood",  methods=["GET", "POST"])
def mood():
	form=MoodForm()
	if  form.validate_on_submit():
		flash("Thanks a lot", "success")
		return (redirect("/index"))
	return (render_template("form.html", form=form, title="How do you feel today ?"))

@app.route("/team",  methods=["GET", "POST"])
def team():
	return (render_template("form.html", title="team"))
	
@app.route("/stats",  methods=["GET", "POST"])
def stats():
	return (render_template("form.html", title="team"))
	
	
	
@app.route("/login",  methods=["GET", "POST"])
def login():
	form=LoginForm()
	if  form.validate_on_submit():
		session["login"]=request.form["login"] 
		flash("Thanks a lot", "success")
		return (redirect("/index"))
	return (render_template("form.html", form=form, title="Please Login"))

@app.route("/logout")
def logout():
	flash("See you soon", "success")
	if session["login"]:
		session.pop("login")
	return (redirect("/index"))
	
@app.route("/signup", methods=["GET", "POST"])
def signup():
	form=SignUpForm()
	if  form.validate_on_submit():
		session["login"]=request.form["login"]
		U=User(login=request.form["login"], password=request.form["password1"], 
						email=request.form ["email"])
		U.save()
		flash("Thanks for joining us", "success")
		return (redirect("/index"))
	return(render_template("form.html", form=form))