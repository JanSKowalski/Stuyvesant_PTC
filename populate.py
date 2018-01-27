from app import models, db
from app.models import PTQueue
import csv

#########################################################
#Database
#########################################################

db.create_all()

with open('app/static/csv/PTC_Room_Assignments.csv') as csvDataFile:
    csv_reader = csv.reader(csvDataFile)
    for row in csv_reader:
        ptqueue = PTQueue(teacher=row[0], department=row[1], room=row[2], description=row[3])
        db.session.add(ptqueue)
        db.session.commit()
