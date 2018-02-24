import os
from flask import Flask, flash, redirect, url_for, render_template, request, session, jsonify
from app import app, models, db, login_manager

from flask_login import current_user, login_required, login_user, logout_user
from flask.ext.login import UserMixin
from .forms import LoginForm, RegistrationForm, SearchForm

#from app.forms import
from app.models import User, Parent, PTQueue

@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:
      username = session['username']
      return 'Logged in as ' + username + '<br>'
    #current_user.is_authenticated = False
    return render_template('Cover/index.html', title='Stuyvesant PTC')

@app.route('/teacher_search', methods=['GET', 'POST'])
@app.route('/teacher_search/<teacher_query>', methods=['GET', 'POST'])
def teacher_search():
    form = SearchForm()
    if request.method == 'POST':
        teachers = PTQueue.query.whoosh_search(form.search_field.data).all()
        return render_template('Cover/teacher_search.html', title='Teacher Query', teachers=teachers, form=form)
    else:
        return render_template('Cover/teacher_search.html', title='Teacher Query', teachers=[], form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #If a user is already logged in, send them to the right place
    '''
    if current_user.is_authenticated:
        if (current_user == 'student'):
            return redirect(url_for('staff'))
        if (current_user == 'admin'):
            return redirect(url_for('administration'))
        return redirect(url_for('index'))
'''
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        print(form.username.data)


        login_user(user, remember=form.remember_me.data)
        if (form.username.data == 'student'):
            session['username'] = 'student'
            return redirect(url_for('staff'))
        if (form.username.data == 'admin'):
            session['username'] = 'admin'
            return redirect(url_for('administration'))
        return redirect(url_for('index'))
    return render_template('Staff/login.html', title='Login Manager', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/teacher/<teacher_id>', methods=['GET', 'POST'])
def teacher(teacher_id):
    teacher = PTQueue.query.get(teacher_id)
    return render_template('Cover/teacher.html', title='Teacher', teacher=teacher)






#########################       Parent      #########################
@app.route('/parent_home')
def parent_home():
    return render_template('Parent/parent_home.html', title='Parent Portal')

@app.route('/parent_search', methods=['GET', 'POST'])
@app.route('/parent_search/<parent_query>', methods=['GET', 'POST'])
def parent_search():
    form = SearchForm()
    if request.method == 'POST':
        parents = Parent.query.whoosh_search(form.search_field.data).all()
        return render_template('Parent/parent_search.html', title='ID Look-Up', parents=parents, form=form)
    else:
        return render_template('Parent/parent_search.html', title='ID Look-Up', parents=[], form=form)

@app.route('/parent/<parent_id>', methods=['GET', 'POST'])
def parent(parent_id):
    parent = Parent.query.get(parent_id)
    return render_template('Parent/parent.html', title='Parent', parent=parent)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if  form.validate_on_submit():
        if (not form.validate_date() or not form.validate_parent()):
            for error in form.errors:
                flash(error)
        parent = Parent(child_name=form.child_name.data, child_dob=form.child_dob.data) #, email=form.email.data)
        db.session.add(parent)
        db.session.commit()
        #flash('Congratulations, you are now a registered parent!')
        parent_id = parent.id
        return render_template('Parent/id_response.html', title='ID Response', parent_id=parent_id)
    else:
        for error in form.errors:
            flash(error)
    return render_template('Parent/register.html', title='Register', form=form)

@app.route('/parent_schedules')
def parent_schedules():
    return render_template('Parent/parent_schedules.html', title='Parent Schedules')



#########################       Staff       #########################
@app.route('/staff')
@login_required
def staff_home():
    return render_template('Staff/student_home.html', title='Student Portal')



#########################   Administration  #########################

@app.route('/administration')
def admin_home():
    return render_template('Staff/admin_home.html', title='Admin Portal')


@app.route('/statistics')
def statistics():
    ptqueue = models.PTQueue.query.all()
    return render_template('Staff/statistics.html', ptqueue=ptqueue, title='Statistics')

@app.route('/database')
def database():
    ptqueue = models.PTQueue.query.all()
    return render_template('Staff/database.html', ptqueue=ptqueue, title='Database')

@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        with open('app/static/csv/PTC_Room_Assignments.csv') as csvDataFile:
            csv_reader = csv.reader(csvDataFile)
            for row in csv_reader:
                ptqueue = PTQueue(teacher=row[0], department=row[1], room=row[2], description=row[3])
                db.session.add(ptqueue)
                db.session.commit()
        flash('CSV successfully updated.')
        return redirect(url_for('upload_csv'))
    return render_template('Cover/index.html')
