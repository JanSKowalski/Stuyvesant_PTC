from ptc import ptc, models, db
from ptc.models import User


student = User(username='student')
student.set_password('test1')

admin = User(username='admin')
admin.set_password('test2')

station = User(username='station')
station.set_password('test3')

teacher = User(username='teacher')
teacher.set_password('test4')

db.session.add(student)
db.session.add(admin)
db.session.add(station)
db.session.add(teacher)
db.session.commit()
