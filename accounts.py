from ptc import ptc, models, db
from ptc.models import User


student = User(username='student')
student.set_password('Honor')

admin = User(username='admin')
admin.set_password('Authority')

station = User(username='station')
station.set_password('Train')

teacher = User(username='teacher')
teacher.set_password('AnotherBrick')

db.session.add(student)
db.session.add(admin)
db.session.add(station)
db.session.add(teacher)
db.session.commit()
