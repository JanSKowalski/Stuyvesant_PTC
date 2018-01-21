from app import models, db
from flask import request


db.create_all()

for i in range(0,5):
    s = str(i)
    u = models.Parent(child_name='child'+s,  email= s+'@email.com')
    db.session.add(u)

db.session.commit()


for i in range(0,3):
    s = str(i)
    u = models.PTQueue(teacher='teacher'+s, room=s, department=s, description=s)
    db.session.add(u)
db.session.commit()    
'''
z = models.PTQueue().query.get(1)
print("queue: " + str(z))
p = models.Parent().query.get(3)
print("parent: " + str(p))
z.enqueue(z, p)
print(z)
db.session.add(z)
db.session.commit()

'''
'''
for i in range(0,8):
    z = models.PTQueue().query.get(i + 1)
    print(z)
'''
#########################################################
#Database
#########################################################
'''
def ptqueue_init_func(row):
        q = PTQueue()
        q.teacher = row['Teacher']
        q.department = row['Department']
        q.room = row['Room']
        q.description = row['Description']
        return q

request.save_book_to_database(
    field_name='app.db', session=db.session,
    tables=[PTQueue],
    initializers=[ptqueue_init_func])
            
admin = models.User(username="admin", password="password")
db.session.add(admin)
 
student = models.User(username="student", password="python")
db.session.add(student)
 
 
# commit the record the database
db.session.commit()
'''
