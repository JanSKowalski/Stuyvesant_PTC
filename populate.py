import os
from ptc import ptc, models, db
from ptc.models import PTQueue, Parent, User
import csv, datetime
import whoosh
from whoosh.fields import Schema, DATETIME
import flask_sqlalchemy as flask_sqlalchemy
import flask_whooshalchemy as whooshalchemy


#########################################################
#Database
#########################################################

#flask_sqlalchemy.models_committed.connect(_after_flush)
'''
schema, primary_key = whooshalchemy._get_whoosh_schema_and_primary_key(Parent)
print "_____________________________\n"
print schema
print "_____________________________\n"
schema.add('child_dob', whoosh.fields.TEXT(stored=True, sortable=True))

#schema.remove('child_dob')
print schema
print "_____________________________\n"

'''

os.system("sudo rm ptc.db")
os.system("sudo rm error.log")
os.system("sudo rm -rf search.db")



#db.drop_all()
db.create_all()


for i in range(3, 25):
    parent = Parent(parent_name="parent"+str(i), child_name="child"+str(i), child_dob="2/19/20"+str(i))
    db.session.add(parent)
    db.session.commit()



with open('ptc/static/csv/PTC_Room_Assignments.csv') as csvDataFile:
    csv_reader = csv.reader(csvDataFile)
    for row in csv_reader:
        ptqueue = PTQueue(teacher=row[0], opt_in=int(row[1]), department=row[2], room=row[3], description=row[4])
        db.session.add(ptqueue)
        db.session.commit()


#os.system("sudo python accounts.py")
#os.system("sudo chown -R www-data .")
