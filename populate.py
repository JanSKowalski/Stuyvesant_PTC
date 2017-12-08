from app import models, db

for i in range(0,500):
    s = str(i)
    u = models.Parents(name='parent'+s, child_name='child'+s, email= s+'@email.com')
    db.session.add(u)


user = Users(username="admin", password="password")
db.session.add(user)
 
user = Users(username="student", password="python")
db.session.add(user)
 
 
# commit the record the database
db.session.commit()
