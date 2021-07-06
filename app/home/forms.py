from flask_wtf import FlaskForm
from wtforms.fields import (
    PasswordField,
    SubmitField,
)
from wtforms.fields.core import StringField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import EqualTo, InputRequired


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[InputRequired()])
    new_password = PasswordField(
        'New password',
        validators=[
            InputRequired(),
            EqualTo('new_password2', 'Passwords must match.')
        ])
    new_password2 = PasswordField(
        'Confirm new password', validators=[InputRequired()])
    submit = SubmitField('Changer')
    
class NewThread(FlaskForm):
    title = StringField('Titre', validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired()])
    
class NewReply(FlaskForm):
    message = TextAreaField('Message', validators=[InputRequired()])