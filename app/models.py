from app import db
from flask.ext.security import UserMixin, RoleMixin
from wtforms import validators
from datetime import datetime

class Role(db.Document, RoleMixin):
	name = db.StringField(max_length=80, unique=True)
	description = db.StringField(max_length=255)
	
	def __str__(self):
		return("%s" % self.name)

class Team(db.Document):
	name = db.StringField(max_length=80, unique=True)
	description = db.StringField(max_length=255)
	
	def __str__(self):
		return("%s" % self.name)

class User(UserMixin, db.Document):
	name = db.StringField(max_length=80)
	email = db.EmailField(max_length=255)
	password = db.StringField(max_length=255)
	active = db.BooleanField(default=True)
	confirmed_at = db.DateTimeField()
	roles = db.ListField(db.ReferenceField(Role), default=[])
	teams = db.ListField(db.ReferenceField(Team), default=[])

	def __str__(self):
		return("%s" % self.name)

class MoodItem(db.Document):
	name=db.StringField(max_length=32)
	def __str__(self):
		return("%s" % self.name)

class MoodGroup(db.Document):
	name=db.StringField(max_length=32)
	mood = db.ListField(db.ReferenceField(MoodItem), default=[], validators=[validators.Required()])
	
	def __str__(self):
		return("%s" % self.name)

class Mood(db.Document):
	mood=db.ListField(db.ReferenceField(MoodItem), default=[], validators=[validators.Required()])
	date=db.DateTimeField(default=datetime.now, required=True)
	user=db.ReferenceField(User, required=True)
	
	def __str__(self):
		return("%s" % self.mood)