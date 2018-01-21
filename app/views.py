import os
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from app import app, models, db, login_manager


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/database')
def database():
    ptqueue = models.PTQueue.query.all()
    return render_template('database.html', ptqueue=ptqueue)

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
    return render_template('index.html')
