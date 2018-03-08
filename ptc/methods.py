from ptc import models, db, mail, ptc






def administrator_authenticate(func):
    @wraps(func)
    def check_user(*args, **kwargs):
        if not 'username' in session or not 'tutor_or_tutee' in session:
            flash("You are not logged in")
            return redirect(url_for('login', prev_url = request.path))
        if not session['tutor_or_tutee'] == 'tutor':
            flash("You must be a tutor to access that page")
            return redirect('index')
        tutor = models.Tutor.query.filter_by(username = session['username']).first()
        if not tutor:
            flash("Authentication did not check out")
            return redirect('index')
        if not tutor.admin:
            flash("You must be an administrator to view this page")
            return redirect('index')
        return func(*args, **kwargs)
return check_userptc


def reset_database():
    #System for pdf creation of database data
    #Clear database
    for parent in models.ParentS.query.filter_by().all():
        db.session.delete(parent)
    db.session.commit()
