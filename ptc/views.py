import os
from flask import Flask, flash, redirect, url_for, render_template, request, session, jsonify
from ptc import ptc, models, db, login_manager

from flask_login import current_user, login_required, login_user, logout_user
from .forms import LoginForm, RegistrationForm, SearchForm, AddForm, RemoveForm

from ptc.models import User, Parent, PTQueue
import time, datetime

@ptc.route('/')
@ptc.route('/index')
def index():
    session['username'] = 'Guest'

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
        if (username == 'Student'):
            return redirect('/staff')
        if (username == 'Admin'):
            return redirect('/administration')

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        login_user(user)
        if (form.username.data == 'student'):
            session['username'] = 'Student'
            return redirect('/staff')
        if (form.username.data == 'station'):
            session['username'] = 'Station'
            return redirect('/station')
        if (form.username.data == 'teacher'):
            session['username'] = 'Teacher'
            return redirect('/teacher_home')
        if (form.username.data == 'admin'):
            session['username'] = 'Admin'
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


@ptc.route('/id_response/<parent_id>', methods=['GET', 'POST'])
def id_response(parent_id):
	return render_template('Parent/id_response.html', title='ID Response', parent_id=parent_id)


@ptc.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if  form.validate_on_submit():
        parent = Parent(parent_name=form.parent_name.data, child_name=form.child_name.data, child_dob=form.child_dob.data) #, email=form.email.data)
        db.session.add(parent)
        db.session.commit()
        #flash('Congratulations, you are now a registered parent!')
        parent_id = parent.id
        return redirect('id_response/' + str(parent_id))
    else:
        return render_template('Parent/register.html', title='Register', form=form)

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

@ptc.route('/station')
@login_required
def station_home():
    return render_template('Staff/station_home.html', title='Station Portal')

@ptc.route('/teacher_home')
@login_required
def teacher_home():
    return render_template('Staff/teacher_home.html', title='Teacher Portal')


@ptc.route('/logout')
def logout():
    logout_user()
    session['username'] = 'Guest'
    return redirect(url_for('index'))


@ptc.route('/teacher/<teacher_id>', methods=['GET', 'POST'])
def teacher(teacher_id):
    add_form = AddForm()
    rm_form = RemoveForm()


    teacher = PTQueue.query.get(teacher_id)
    #for p in teacher.parents:

    if request.method == 'POST':
        if add_form.validate_id():
            parent = models.Parent.query.get(add_form.add_field.data)
            teacher = models.PTQueue.query.get(teacher_id)
    	    db.session.add(teacher)		#Adding before and after is very necessary,
    	    teacher.enqueue(teacher, parent)	#as this allows sqlalchemy to match the orm
    	    db.session.add(teacher) 		#to the regular database. (Google 'sqlalchemy orm')
    	    db.session.commit()
            return render_template('Cover/teacher.html', title='Teacher',
                                teacher=teacher, add_form=add_form, rm_form=rm_form)

        elif rm_form.validate_id(teacher_id):
            teacher = models.PTQueue.query.get(teacher_id)
            db.session.add(teacher) 	#Adding before and after is very necessary,
    	    teacher.dequeue(teacher)	#as this allows sqlalchemy to match the orm
    	    db.session.add(teacher) 	#to the regular database. (Google 'sqlalchemy orm')
    	    db.session.commit()
            return render_template('Cover/teacher.html', title='Teacher',
                                teacher=teacher, add_form=add_form, rm_form=rm_form)


    return render_template('Cover/teacher.html', title='Teacher',
                        teacher=teacher, add_form=add_form, rm_form=rm_form)





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
