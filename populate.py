from app import models, db

for i in range(0,500):
    s = str(i)
    u = models.Parents(name='parent'+s, child_name='child'+s, email= s+'@email.com')
    db.session.add(u)



db.session.commit()
