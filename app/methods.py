from app import models, db, mail, app

    
def reset_database():
    #System for pdf creation of database data
    #Clear database
    for parent in models.ParentS.query.filter_by().all():
        db.session.delete(parent)
    db.session.commit()
