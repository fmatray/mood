from flask_wtf import Form
from wtforms import StringField, SubmitField, validators


class TeamInvite(Form):
    """ Form to send and invitation for a team to a user """
    email = StringField('Email to invite', [
        validators.Length(min=6, max=35), validators.Email()])
    submit = SubmitField('Go')

    def __init__(self):
        Form.__init__(self, csrf_enabled=True)
