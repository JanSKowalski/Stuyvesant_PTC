from app import models, db

db.create_all()

for i in range(0,5):
    s = str(i)
    u = models.Parent(child_name='child'+s, child_dob = i, email= s+'@email.com')
    db.session.add(u)

db.session.commit()

for i in range(0,5):
    s = str(i)
    u = models.PTQueue(teacher='teacher'+s)
    #print(u)
    '''
    y = models.Parent.query.get(i)
    print(y)
    '''
    db.session.add(u)
    
db.session.commit()

for i in range(0,5):
    z = models.PTQueue().query.get(3)
    print(z.teacher)
    w = z.get_id(z)
    print(z)
    p = models.Parent().query.get(3)
    print(p)
    z.enqueue(z, p)
    print(z)
    #z = z.load_queue(z)
    '''
    parent = models.Parent.query.get(i)
    print(z)
    #Error here
    queue = models.PTQueue.query.get(z)
    print(z)
    queue.enqueue(queue, parent)
    print(q)
    '''
    db.session.add(q)

admin = models.User(username="admin", password="password")
db.session.add(admin)
 
student = models.User(username="student", password="python")
db.session.add(student)
 
 
# commit the record the database
db.session.commit()
