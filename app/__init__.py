from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_mongoengine import MongoEngine

from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
from flask.ext.security import Security, MongoEngineUserDatastore, UserMixin, RoleMixin, login_required

app=Flask(__name__)
app.config.from_object("config")

db=MongoEngine(app)

Bootstrap(app)
nav=Nav()
nav.init_app(app)

admin = Admin(app, name='How do you feel ?', template_mode='bootstrap3')
from .models import *
admin.add_view(ModelView(User))
admin.add_view(ModelView(Team))

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from app import views
