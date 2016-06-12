from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_mongoengine import MongoEngine

from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_admin.contrib.mongoengine import ModelView
from flask_security import Security, MongoEngineUserDatastore, UserMixin, RoleMixin, login_required, current_user
from flask_login import LoginManager
from flask_mail import Mail

from flask_humanize import Humanize

app=Flask(__name__)
app.config.from_object("config")

humanize = Humanize(app)


mail = Mail(app)

db=MongoEngine(app)

Bootstrap(app)
nav=Nav()
nav.init_app(app)

class SecuredModelView(ModelView):
	def is_accessible(self):
		if not current_user.is_active or not current_user.is_authenticated:
			return False

		if current_user.has_role('superuser'):
			return True

		return False

	def _handle_view(self, name, **kwargs):
		"""
			Override builtin _handle_view in order to redirect users when a view is not accessible.
		"""
		if not self.is_accessible():
			if current_user.is_authenticated:
				# permission denied
				abort(403)
			else:
				# login
				return redirect(url_for('security.login', next=request.url))

admin = Admin(app, name='How do you feel ?', template_mode='bootstrap3')
from .models import *
admin.add_view(SecuredModelView(User))
admin.add_view(SecuredModelView(Role))
admin.add_view(SecuredModelView(Team))
admin.add_view(SecuredModelView(Mood))
admin.add_view(SecuredModelView(MoodItem))
admin.add_view(SecuredModelView(MoodGroup))

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
	u=User.objects.get(id=user_id)
	return u
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
    )
from app import views
