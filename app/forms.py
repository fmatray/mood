from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, RadioField, SubmitField, validators

class MoodForm(Form):
	title="mood"
	choice_switcher=RadioField("How do you feel today ?", [validators.DataRequired()], 
		choices=[("Bad", "Bad"), ("Ok","Ok"), ("Good", "Good")])
	submit = SubmitField(u'Go')

class LoginForm(Form):
	title="login"
	login=StringField("Login", [validators.DataRequired()])
	password=PasswordField("Password", [validators.DataRequired()])
	submit = SubmitField(u'Go')

	def validate_login(self, field):
		user = self.get_user()
		if user is None:
			raise validators.ValidationError('Invalid user')

		if user.password != self.password.data:
			raise validators.ValidationError('Invalid password')

	def get_user(self):
		return User.objects(login=self.login.data).first()
	
	
class SignUpForm(Form):
	title="signup"
	login=StringField("Login", [validators.DataRequired()])
	email=StringField("Email", [validators.DataRequired(), validators.Email()])
	password1=PasswordField("Password", [validators.DataRequired(), validators.Length(min=6, message="Password too short"), validators.EqualTo('password2', message='password mismatch')])
	password2=PasswordField("Confirmation", [validators.DataRequired()])
	submit = SubmitField(u'Go')
