#!flask/bin/python

import os
from flask import Flask, flash, redirect, render_template, request, session, abort
from app import app, models, db, login_manager

'''
from flask import render_template, flash, redirect, session, url_for, request
#from flask_login import login_user, logout_user, current_user, login_required

#from .forms import LoginForm, RegisterForm
#from .models import Parents, Users
'''


@app.route('/')
def index():
    session['logged_in'] = False
    
    parents = models.Parent.query.all()
    ptqueue = models.PTQueue.query.all()
    return render_template('Parent/parents.html', title = 'Parent Number Look-Up', parents = parents, ptqueue = ptqueue)

 
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'passwords' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()


@app.route('/parents')
def parents():
    parents = models.Parents.query.all()
    return render_template('Parent/parents.html', title = 'Parent Number Look-Up', parents = parents)
    
'''
@app.route("/import", methods=['GET', 'POST'])
def doimport():
    if request.method == 'POST':


        return redirect('/')
'''
'''
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = 'Home')


@app.route('/search')
def search():
    return render_template('Parent/search.html', title = 'Search Options')

@app.route('/parents')
def parents():
    parents = models.Parents.query.all()
    return render_template('Parent/parents.html', title = 'Parent Number Look-Up',
                         parents = parents)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    session['username'] = login_form.username.data
    if login_form.validate_on_submit():
        flash('Welcome %s!' % (login_form.username.data))
        return redirect('/index')
    return render_template('login.html', title = 'Login', form = login_form)
    
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        new_parent = models.Parents(name = register_form.name.data,
                                child_name = register_form.child_name.data,
                                email = register_form.email.data
                                )
        db.session.add(new_parent)
        db.session.commit()
        #flash('Welcome %s!' % (register_form.name.data))
        flash('Welcome!')
        #return redirect('number.html?id=3')
        return redirect('index')
    return render_template('Parent/register.html', title = 'Register', form = register_form)    
    
    
@app.route('/number')
def number():
    return render_template('Parent/number.html', title = 'Number')
    
    '''
