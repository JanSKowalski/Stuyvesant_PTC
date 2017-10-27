from app import app, models
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import flash, session

class RegisterForm(Form):
    name = StringField('name', validators=[DataRequired()])
    child_name = StringField('name', validators=[DataRequired()])
    email = StringField('name', validators=[DataRequired()])
    
    def validate_on_submit(self):
        if not Form.validate_on_submit(self):
            return False
        parent = models.Parents.query.filter_by(name = self.name.data).first()
        if parent:
            self.name.errors.append("A parent has already registered under this name")
            return False
        return True
    
class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField()

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
