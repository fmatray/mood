from app import db

class Role(db.Document, RoleMixin):
	name = db.StringField(max_length=80, unique=True)
	description = db.StringField(max_length=255)
	
class User(db.Document):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])



		
class Team(db.Document):
	name=db.StringField(required=True)
	
	def __str__(self):
		return("%s" % self.name)
