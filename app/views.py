import os
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from app import app, models, db, login_manager


@app.route('/')
def index():
    return render_template('Cover/index.html', title='Stuyvesant PTC')

@app.route('/search')
def teacher_search():
    return render_template('Cover/teacher_search.html', title='Teacher Query')

@app.route('/login')
def login():
    return render_template('Staff/login.html', title='Login Manager')


#Create a specific page for statistics

#########################       Parent      #########################
@app.route('/parent')
def parent_home():
    return render_template('Parent/parent_home.html', title='Parent Portal')

@app.route('/parent_search')
def parent_search():
    return render_template('Parent/parent_search.html', title='ID Look-Up')

@app.route('/register')
def register():
    return render_template('Parent/register.html', title='Register')

@app.route('/parent_schedules')
def parent_schedules():
    return render_template('Parent/parent_schedules.html', title='Parent Schedules')



#########################       Staff       #########################

@app.route('/staff')
def staff_home():
    return render_template('Staff/student_home.html', title='Student Portal')




#########################   Administration  #########################

#@app.route('')








@app.route('/database')
def database():
    ptqueue = models.PTQueue.query.all()
    return render_template('Cover/database.html', ptqueue=ptqueue, title='database')

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
