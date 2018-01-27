from app import app, models
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email
from flask import flash, session
from datetime import datetime


class RegistrationForm(Form):
    child_name = StringField('child_name', validators=[DataRequired()])
    child_dob = StringField('child_dob', validators=[DataRequired()])
    email = StringField('email', validators=[Email()])
    submit = SubmitField('Register')

    def validate_date(self):
        #Convert to datetime object
        s = self.child_dob.data
        try:
            self.child_dob.data = datetime.strptime(s, '%m/%d/%Y')
        except ValueError:
            self.child_dob.errors.append("Please input a valid date in the correct format")


    def validate_parent(self):
        d_child_name = models.Parent.query.filter_by(child_name = self.child_name.data).first()
        d_child_dob = models.Parent.query.filter_by(child_dob = self.child_dob.data).first()
        if d_child_name and d_child_dob:
            self.child_name.errors.append("A parent has already registered under this child and date of birth")
            self.child_dob.errors.append("A parent has already registered under this child and date of birth")
            return False
        return True

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

    def validate_on_submit(self):
        if not Form.validate_on_submit(self):
            return False
        user = models.Users.query.filter_by(username = self.username.data).first()
        if (not user):
            self.username.errors.append("No user with this username exists")
            return False
        if (user.check_password(self.password.data)):
            self.password.errors.append("Authentication failed")
            return False
        return True

class SearchForm(Form):
    search_field = StringField('search')
    submit = SubmitField()
