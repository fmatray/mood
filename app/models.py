from app import db
from flask.ext.security import UserMixin, RoleMixin

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

class User(db.Document, UserMixin):
	name = db.StringField(max_length=80)
	email = db.StringField(max_length=255)
	password = db.StringField(max_length=255)
	active = db.BooleanField(default=True)
	confirmed_at = db.DateTimeField()
	roles = db.ListField(db.ReferenceField(Role), default=[])
	teams = db.ListField(db.ReferenceField(Team), default=[])

	def __str__(self):
		return("%s" % self.name)

class Mood(db.Document):
	name=db.StringField(max_length=32)

	def __str__(self):
		return("%s" % self.name)

