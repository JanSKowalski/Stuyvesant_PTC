import os
from flask import Flask, flash, redirect, url_for, render_template, request, session, jsonify
from ptc import ptc, models, db, login_manager

from flask_login import current_user, login_required, login_user, logout_user
#from flask.ext.login import UserMixin
from .forms import LoginForm, RegistrationForm, SearchForm, AddForm

#from ptc.forms import
from ptc.models import User, Parent, PTQueue

@ptc.route('/')
@ptc.route('/index')
def index():
    return render_template('Cover/index.html', title='Stuyvesant PTC')

@ptc.route('/teacher_search', methods=['GET', 'POST'])
@ptc.route('/teacher_search/<teacher_query>', methods=['GET', 'POST'])
def teacher_search():
    form = SearchForm()
    if request.method == 'POST':
        teachers = PTQueue.query.whoosh_search(form.search_field.data).all()
        return render_template('Cover/teacher_search.html', title='Teacher Query', teachers=teachers, form=form)
    else:
        return render_template('Cover/teacher_search.html', title='Teacher Query', teachers=[], form=form)

@ptc.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        username = session['username']
        if (username == 'student'):
            return redirect('/staff')
        if (username == 'admin'):
            return redirect('/administration')

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        login_user(user) #, remember=form.remember_me.data)
        if (form.username.data == 'student'):
            session['username'] = 'student'
            return redirect('/staff')
        if (form.username.data == 'admin'):
            session['username'] = 'admin'
            return redirect('/administration')
        return redirect('/index')
    return render_template('Staff/login.html', title='Login Manager', form=form)


#########################       Parent      #########################
@ptc.route('/parent_home')
def parent_home():
    return render_template('Parent/parent_home.html', title='Parent Portal')
ptc
@ptc.route('/parent_search', methods=['GET', 'POST'])
@ptc.route('/parent_search/<parent_query>', methods=['GET', 'POST'])
def parent_search():
    form = SearchForm()
    if request.method == 'POST':
        parents = Parent.query.whoosh_search(form.search_field.data).all()
        return render_template('Parent/parent_search.html', title='ID Look-Up', parents=parents, form=form)
    else:
        return render_template('Parent/parent_search.html', title='ID Look-Up', parents=[], form=form)

@ptc.route('/parent/<parent_id>', methods=['GET', 'POST'])
def parent(parent_id):
    parent = Parent.query.get(parent_id)
    return render_template('Parent/parent.html', title='Parent', parent=parent)

@ptc.route('/register', methods=['GET', 'POST'])
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


@ptc.route('/parent_schedules', methods=['GET', 'POST'])
@ptc.route('/parent_schedules/<parent_query>', methods=['GET', 'POST'])
def parent_schedules():
    form = SearchForm()
    if request.method == 'POST':
        if form.validate_id():
            parent = models.Parent.query.get(form.search_field.data)
            return render_template('/Parent/parent.html', title='Parent', parent=parent)
        else:
            return render_template('/Parent/parent_schedules.html', title='Parent Schedules', form=form)
    else:
        return render_template('/Parent/parent_schedules.html', title='Parent Schedules', form=form)



#########################       Staff       #########################
@ptc.route('/staff')
@login_required
def staff_home():
    return render_template('Staff/student_home.html', title='Student Portal')


@ptc.route('/logout')
def logout():
    logout_user()
    session['username'] = 'guest'
    return redirect(url_for('index'))


@ptc.route('/teacher/<teacher_id>', methods=['GET', 'POST'])
def teacher(teacher_id):
    add_form = AddForm()
    #rm_form = RemoveForm()

    teacher = PTQueue.query.get(teacher_id)
    if request.method == 'POST':
        if add_form.validate_id():
            parent = models.Parent.query.get(add_form.search_field.data)
            teacher = models.PTQueue.query.get(teacher_id)
            teacher.enqueue(teacher, parent)
            db.session.add(teacher)
            db.session.commit()
            return render_template('Cover/teacher.html', title='Teacher',
                                teacher=teacher, add_form=add_form)

    return render_template('Cover/teacher.html', title='Teacher',
                        teacher=teacher, add_form=add_form)





#########################   Administration  #########################

@ptc.route('/administration')
def admin_home():
    return render_template('Staff/admin_home.html', title='Admin Portal')


@ptc.route('/statistics')
def statistics():
    ptqueue = models.PTQueue.query.all()
    return render_template('Staff/statistics.html', ptqueue=ptqueue, title='Statistics')

@ptc.route('/database')
def database():
    ptqueue = models.PTQueue.query.all()
    return render_template('Staff/database.html', ptqueue=ptqueue, title='Database')

@ptc.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        with open('ptc/static/csv/PTC_Room_Assignments.csv') as csvDataFile:
            csv_reader = csv.reader(csvDataFile)
            for row in csv_reader:
                ptqueue = PTQueue(teacher=row[0], department=row[1], room=row[2], description=row[3])
                db.session.add(ptqueue)
                db.session.commit()
        flash('CSV successfully updated.')
        return redirect(url_for('upload_csv'))
    return render_template('Cover/index.html')
