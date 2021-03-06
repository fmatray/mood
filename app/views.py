from flask import render_template, flash, request, redirect, session, url_for
from flask_nav.elements import Navbar, View, Subgroup, Text, Separator
from app import app, nav
from flask_security import login_required
from .models import User, MoodItem, MoodGroup, Mood, Team
from .stats import PersoPieChart, PersoHistoChart
from flask_mongoengine.wtf import model_form

from wtforms import SubmitField, FileField
from flask.ext.security import current_user
from .forms import TeamInvite
from datetime import datetime
from PIL import Image


@nav.navigation()
def moodnavbar():
    sg1 = Subgroup("Moods", View("Mood", "mood"), View(
        "Mood List", "moodlist"), Separator(), View("Statistics", "personalstats"))
    sg2 = Subgroup("Teams", View("Team", "team"),
                   View("Team List", "teamlist"))
    sg3 = Subgroup("Auth", View("Login", "security.login"), View("Profile", "profile"), View("Logout", "security.logout"), View("Change password", "security.change_password"),
                   Separator(), View("Register", "security.register"))
    if (current_user.is_authenticated):
        msg = "Welcome "
        if current_user.name:
            msg = msg + current_user.name
        else:
            msg = msg + current_user.email
    else:
        msg = "Please login or register"
    return (Navbar('Mood', View('Home', 'index'), sg1, sg2, sg3, View("Admin", "admin.index"), Text(msg)))


@app.route("/index")
@app.route("/")
def index():
    return (render_template("index.html", title="Welcome"))


""" Mood """


@app.route("/mood",  methods=["GET", "POST"])
@app.route("/mood/edit/<mood_id>",  methods=["GET", "POST"])
@login_required
def mood(mood_id=None):
    if mood_id:
        m = Mood.objects.get_or_404(id=mood_id)
        if not m.iseditable:
            flash("Too old", "error")
            return redirect("/mood/view/" + mood_id)
    else:
        m = Mood()
    Moodform = model_form(Mood, only=["mood", "comment"])
    Moodform.submit = SubmitField('Go')
    form = Moodform(request.form, m)
    if form.validate_on_submit():
        form.populate_obj(m)
        m.user = User.objects.get_or_404(id=current_user.id)
        m.save()
        flash("Thanks a lot", "success")
        return redirect("/mood/list")
    return render_template("form.html", form=form, title="How do you feel today ?")


@app.route("/mood/view/")
@app.route("/mood/view/<mood_id>")
@login_required
def moodview(mood_id=None):
    if mood_id:
        try:
            m = Mood.objects.get_or_404(id=mood_id)
        except:
            flash("Mood not found", "error")
            return redirect("/moodlist")
    else:
        return redirect("/index")
    return render_template("view.html", element=m, title="Mood", long=True)


@app.route("/mood/delete/<mood_id>")
@login_required
def deletemood(mood_id=None):
    if mood_id:
        try:
            m = Mood.objects.get_or_404(id=mood_id)
            m.delete()
            flash("Mood deleted", "success")
        except:
            flash("Mood not found", "error")
    return (redirect("/moodlist"))


@app.route("/mood/list")
@login_required
def moodlist():
    moods = Mood.objects(user=current_user.id).order_by("-date")
    return (render_template("list.html", list=moods,  title="Moods"))

""" User """


@app.route("/profile",  methods=["GET", "POST"])
@login_required
def profile():
    user = User.objects.get_or_404(id=current_user.id)
    Userform = model_form(User, only=["name", "teams", "description"])
    Userform.submit = SubmitField('Go')
    form = Userform(request.form, user)
    if form.validate_on_submit():
        form.populate_obj(user)
        user.save()
        flash("Profile Updated", "success")
        return (redirect("/index"))
    return (render_template("form.html", form=form, title="profile"))

""" Team """


@app.route("/team",  methods=["GET", "POST"])
@app.route("/team/edit/<team_id>",  methods=["GET", "POST"])
@login_required
def team(team_id=None):
    if team_id:
        t = Team.objects.get_or_404(id=team_id)
        fields = ["name", "description"]
    else:
        t = Team()
        fields = ["name", "type", "description"]
    t.admin = User.objects.get_or_404(id=current_user.id)
    Teamform = Team.form(fields)
    form = Teamform(request.form, t)
    if form.validate_on_submit():
        t.photo.replace(request.files[form.photo.name],
                        content_type=request.files["photo"].content_type,
                        filename=request.files["photo"].filename)
        del form.photo
        form.populate_obj(t)
        t.save()
        flash("Thanks a lot", "success")
        return redirect("/index")
    return render_template("form.html", form=form, title="Team")


@app.route("/team/view/")
@app.route("/team/view/<team_id>")
@login_required
def teamview(team_id=None):
    if team_id:
        try:
            t = Team.objects.get_or_404(id=team_id)
        except:
            flash("Team not found", "error")
            return redirect("/teamlist")
    else:
        return redirect("/index")
    return (render_template("viewteam.html", element=t,  title=t.name, long=True))


<<<<<<< HEAD
@app.route("/team/photo/<team_id>")
@app.route("/team/photo/<team_id>/<thumbnail>")
def teamphoto(team_id=None, thumbnail=None):
    t = Team.objects.get_or_404(id=team_id)
    if thumbnail:
        response = make_response(t.photo.thumbnail.read())
    else:
        response = make_response(t.photo.read())
    response.mimetype = t.photo.content_type
    return response

=======
>>>>>>> parent of b1103b0... add image for teams

@app.route("/team/delete/<team_id>")
@login_required
def deleteteam(team_id=None):
    if team_id:
        try:
            t = Team.objects.get_or_404(id=team_id)
            t.delete()
            flash("Team deleted", "success")
        except:
            flash("Team not found", "error")
    return (redirect("/teamlist"))


@app.route("/team/member/invite/<team_id>",  methods=["GET", "POST"])
@login_required
def teammemberinvite(team_id=None):
    if not team_id:
        flash("No team ", "error")
        return (redirect("/index"))
    t = Team.objects.get_or_404(id=team_id)
    form = TeamInvite()
    if form.validate_on_submit():
        t.invite(form.email.data)
        return redirect("/index")
    return render_template("form.html", form=form, title="Invite")

@app.route("/team/member/delete/<team_id>/<user_id>")
@login_required
def teammemberdelete(team_id=None, user_id=None):
	t = Team.objects.get_or_404(id=team_id)
	u = User.objects(id=user_id).first()
	t.removemember(u)
	return redirect("/team/view/" + str(t.id))

@app.route("/team/list")
@login_required
def teamlist():
    teams = Team.objects(admin=current_user.id).order_by("name")
    return (render_template("list.html", list=teams, title="Teams"))


""" Statistics"""


@app.route("/personnal/stats")
@login_required
def personalstats():
    c1 = PersoPieChart()
    c2 = PersoHistoChart()
    user = User.objects.get_or_404(id=current_user.id)
    return (render_template("stats.html", title="Personal statistics",  item=user, charts=[c1, c2]))
