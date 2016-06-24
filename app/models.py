from app import db
from flask_security import UserMixin, RoleMixin, current_user
from wtforms import validators
from datetime import datetime
from flask import flash, url_for
from collections import OrderedDict


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

    def __str__(self):
        return("%s" % self.name)


class User(UserMixin, db.Document):
    name = db.StringField(max_length=80, 
                          verbose_name="Name", help_text="Basically, who are you?")
    email = db.EmailField(max_length=255, unique=True, 
                          verbose_name="Email contact", help_text="Please, check your email")
    description = db.StringField(max_length=1024, 
                          verbose_name="Description", help_text="Tell us more about you")
    password = db.StringField(max_length=255, 
                          verbose_name="Password", help_text="Secret password")
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

    renderfields = ("name", "email", "description", "teams")
    renderfieldsaslist = ("teams")
    badge = "teams"

    def __str__(self):
        if (self.name):
            return("%s" % self.name)
        else:
            return("%s" % self.email)

    @property
    def teams(self):
        return Team.objects.filter(members__user=self)


class Member(db.EmbeddedDocument):
    user = db.ReferenceField(User, required=True)
    start = db.DateTimeField(default=datetime.now, required=True)
    end = db.DateTimeField(default=datetime.now)
    active = db.BooleanField(default=True)

    def __str__(self):
        return self.user.__str__()


TEAM_TYPE=(("Company", "Compagny"),
						("NGO", "Non-governmental organization"), 
						("Simple", "Simple"))
class Team(db.Document):
    name = db.StringField(max_length=80, unique=True, 
                          verbose_name="Team name", help_text="Basically, who are you?")
    type = db.StringField(choices=TEAM_TYPE, required=True,
    			  verbose_name="Type of team", help_text="This will give you differents options after.")
    description = db.StringField(max_length=255, 
                                verbose_name="Description", help_text="What is the purpose of your team?")
    admin = db.ReferenceField(User, required=True, 
                              verbose_name="Administrator", help_text="Who is the boss?")
    date = db.DateTimeField(default=datetime.now, required=True,
                            verbose_name="Creation date", help_text="Automatic field", )
    members = db.EmbeddedDocumentListField('Member',verbose_name="Team's Members", help_text="Who is in?")
    photo = db.ImageField(thumbnail_size=(100, 100, True))

    renderfields = ("name", "type", "description", "admin", "members")
    renderfieldsaslist = ("members")
    actions = OrderedDict((("view", "View"), ("edit", "Edit"),
                           ("invite", "Invite"), ("delete", "Delete")))
    badge = "members"

    @property
    def editurl(self):
        return url_for("team")

    def addmember(self, usertoadd):
        if usertoadd:
            m = Member(user=usertoadd)
            self.members.append(m)
            self.save()
	

    def invite(self, email):
        u = User.objects(email=email).first()
        if u:
            if self.members.filter(user=u).count() == 0:
                self.addmember(u)
                flash("User added", "success")
            else:
                flash("User allready in the team", "error")
        else:
            u = User(email=email).save()
            self.addmember(u)
            flash("Email sent", "success")
    
    @classmethod
    def form(cls, fields=None):
    	if fields:
            Teamform = model_form(cls, only=fields)
        else:
            Teamform = model_form(cls)
        Teamform.photo = FileField()
        Teamform.submit = SubmitField('Go')

    def __str__(self):
        return("%s" % self.name)


class MoodItem(db.Document):
    name = db.StringField(max_length=32)
    color = db.StringField(max_length=10)
    order = db.IntField()

    def __str__(self):
        return("%s" % self.name)

    def __repr__(self):
        return(self.__str__())


class MoodGroup(db.Document):
    name = db.StringField(max_length=32)
    mood = db.ListField(db.ReferenceField(MoodItem),
                        default=[], validators=[validators.Required()])

    def __str__(self):
        return("%s" % self.name)


class Mood(db.Document):
    mood = db.ReferenceField(MoodItem, default=[], validators=[validators.Required()], 
                          verbose_name="How do you feel now?", help_text="This is a feeling")
    date = db.DateTimeField(default=datetime.now, required=True)
    user = db.ReferenceField(User, required=True)
    comment = db.StringField(max_length=255, 
                          verbose_name="Comment", help_text="Feel free to add some comments")

    renderfields = ("mood", "date", "comment")
    actions = OrderedDict(
        (("view", "View"), ("edit", "Edit"), ("delete", "Delete")))

    @property
    def editurl(self):
        return url_for("mood")

    def __str__(self):
        return("%s" % self.mood.name)
