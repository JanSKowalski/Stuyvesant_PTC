#!flask/bin/python

import os
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from app import app, models, db, login_manager


@app.route('/')
def index():
    #ptqueue = models.PTQueue.query.all()
    
    return render_template('index.html')

@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        csv_file = request.files['PTC_Room_Assignments.csv']
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            ptqueue = PTQueue(teacher=row[0], department=row[1], room=row[2], description=row[3])
            db.session.add(ptqueue)
            db.session.commit()
        return redirect(url_for('upload_csv'))
    return render_template('index.html')
