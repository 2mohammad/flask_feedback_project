from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, ValidationError, Length, Email


class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1,max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Length(1,50), Email()])
    first_name = StringField("First Name", validators=[InputRequired(), Length(1,30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(1,30)])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1,max=20)])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content", validators=[InputRequired()])
