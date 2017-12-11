from app import app, models
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import flash, session

class RegisterForm(Form):
    child_name = StringField('child_name', validators=[DataRequired()])
    child_dob = StringField('child_dob', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    
    def validate_on_submit(self):
        if not Form.validate_on_submit(self):
            return False
        d_child_name = models.Parent.query.filter_by(name = self.name.data).first()
        d_child_dob = models.Parent.query.filter_by(name = self.name.data).first()
        if d_child_name and d_child_dob:
            self.name.errors.append("A parent has already registered under this child and date of birth")
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
