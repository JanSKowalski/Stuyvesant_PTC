from ptc import ptc, models
from flask_wtf import Form
from flask.ext.login import UserMixin
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, NumberRange, Email, Optional
from flask import flash, session
from datetime import datetime

class NumberForm(Form):
    number = StringField('number', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegistrationForm(Form):
    parent_name = StringField('parent_name', validators=[DataRequired()])
    child_name = StringField('child_name', validators=[DataRequired()])
    child_dob = StringField('child_dob', validators=[DataRequired()])
    #email = StringField('email', validators=[Email(), Optional()])
    submit = SubmitField('Register')

    def validate_date(self):
        #Convert to datetime object
        s = self.child_dob.data
        try:
            self.child_dob.data = datetime.strptime(s, '%m/%d/%Y')
        except ValueError:
            self.child_dob.errors.append("Please input a valid date in the correct format")


    def validate_parent(self):
        d_parent_name = models.Parent.query.filter_by(parent_name = self.parent_name.data).first()
        d_child_name = models.Parent.query.filter_by(child_name = self.child_name.data).first()
        d_child_dob = models.Parent.query.filter_by(child_dob = self.child_dob.data).first()
        if d_paret_name and d_child_name and d_child_dob:
            self.parent_name.errors.append("A parent has already registered with these credentials")
            self.child_name.errors.append("A parent has already registered with these credentials")
            self.child_dob.errors.append("A parent has already registered with these credentials")
            return False
        return True

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

    def validate_on_submit(self):
        if not Form.validate_on_submit(self):
            return False
        user = models.User.query.filter_by(username = self.username.data).first()
        if (not user):
            self.username.errors.append("No user with this username exists")
            return False
        if (not user.check_password(self.password.data)):
            self.password.errors.append("Authentication failed")
            return False
        return True

class SearchForm(Form):
    search_field = StringField('search', validators=[DataRequired()])
    submit = SubmitField()

    def validate_id(self):
        parent_id = self.search_field.data
        parent = models.Parent.query.get(parent_id)
        if parent is None:
            tmp = list(self.search_field.errors)
            tmp.append("This ID is not recognized.")
            self = tuple(tmp)
            return False
        else:
            return True

#Add Parent to a teacher queue, validate ID exists
class AddForm(Form):
    add_field = StringField('add_field', validators=[NumberRange()])
    submit = SubmitField()

    def validate_id(self, teacher_id):
        teacher = models.PTQueue.query.get(teacher_id)
        parent_list = teacher.parents
        parent_id = self.add_field.data
        if parent_id is None:
            return False
        parent = models.Parent.query.get(parent_id)
        if parent is None:
            tmp = list(self.add_field.errors)
            tmp.append("This ID is not recognized.")
            self = tuple(tmp)
            return False
        if parent in parent_list:
            return False
        else:
            return True

#Add Parent to a teacher queue, validate ID exists
class RemoveForm(Form):
    rm_field = StringField('rm_field', validators=[NumberRange()])
    submit = SubmitField()

    def validate_id(self, teacher_id):
    	teacher = models.PTQueue.query.get(teacher_id)
        size = teacher.size(teacher)
        position = self.rm_field.data
        if position == '':
            return False
    	if size == 0:
    	    return False
        try:
            position = int(position)
        except:
            return False
        if position < 0 or position > teacher.size(teacher):
            return False
        else:
            return True
