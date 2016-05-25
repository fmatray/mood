from flask import render_template, flash, request, redirect, session, url_for
from flask_nav.elements import Navbar, View, Subgroup, Text, Separator
from app import app, nav
from flask.ext.security import login_required
from .models import User, MoodItem, MoodGroup, Mood, Team
from flask_mongoengine.wtf import model_form

from wtforms import SubmitField
from flask.ext.security import current_user


@nav.navigation()
def moodnavbar():
	sg1=Subgroup("Mood view", View("Mood", "mood"), View("Mood List", "moodlist"), Separator(),View("Team", "team"), View("Team List", "teamlist"),Separator(),View("Statistics", "stats"))
	sg2=Subgroup("Auth", View("Login", "security.login"), View("Profile", "profile"),View("Logout", "security.logout"), View("Change password", "security.change_password"), 
									Separator(),View("Register", "security.register"))
	if (current_user.is_authenticated):
		msg="Welcome "
		if current_user.name:
			msg=msg + current_user.name
		else:
			msg=msg + current_user.email
	else:
		msg="Please login or register"
	return (Navbar('Mood', View('Home', 'index'), sg1, sg2, View("Admin", "admin.index"), Text(msg)))


@app.route("/index")
@app.route("/")
def index():
	return (render_template("index.html", title="Welcome"))


@app.route("/mood",  methods=["GET", "POST"])
@app.route("/mood/<mood_id>",  methods=["GET", "POST"])
@login_required
def mood(mood_id=None):
	if mood_id:
		m=Mood.objects.get(id=mood_id)
	else:
		m=Mood()
	Moodform=model_form(Mood, only=["mood"])
	Moodform.submit=SubmitField('Go')
	form=Moodform(request.form, m)
	if  form.validate_on_submit():
		form.populate_obj(m)
		m.user=User.objects.get(id=current_user.id)
		m.save()
		flash("Thanks a lot", "success")
		return (redirect("/index"))
	return (render_template("form.html", form=form, title="How do you feel today ?"))

@app.route("/moodlist")
@login_required
def moodlist():
	moods=Mood.objects(user=current_user.id)
	fields=("mood", "date")
	return (render_template("list.html", list=moods, fields=fields,  editurl=url_for("mood"), title="Moods"))

@app.route("/profile",  methods=["GET", "POST"])
@login_required
def profile():
	user=User.objects.get(id=current_user.id)
	Userform=model_form(User, only=["name", "teams"])
	Userform.submit=SubmitField('Go')
	form=Userform(request.form, user)
	if  form.validate_on_submit():
		form.populate_obj(user)
		user.save()
		flash("Profile Updated", "success")
		return (redirect("/index"))
	return (render_template("form.html", form=form, title="profile"))


@app.route("/team",  methods=["GET", "POST"])
@app.route("/team/<team_id>",  methods=["GET", "POST"])
@login_required
def team(team_id=None):
	if team_id:
		t=Team.objects.get(id=team_id)
	else:
		t=Team()
	t.admin=User.objects.get(id=current_user.id)
	Teamform=model_form(Team)
	Teamform.submit=SubmitField('Go')
	form=Teamform(request.form, t)
	if  form.validate_on_submit():
		form.populate_obj(t)
		t.save()
		flash("Thanks a lot", "success")
		return (redirect("/index"))
	return (render_template("form.html", form=form, title="Team"))

@app.route("/teamlist")
@login_required
def teamlist():
	teams=Team.objects(admin=current_user.id)
	fields=("name", "description", "admin", "members")
	return (render_template("list.html", list=teams, fields=fields, 
					editurl=url_for("team"), badge="members", title="Teams"))

@app.route("/stats",  methods=["GET", "POST"])
def stats():
	return (render_template("form.html", title="team"))
	