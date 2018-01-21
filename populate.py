from app import models, db
from flask import request
from pandas import DataFrame, read_csv
from sqlalchemy import create_engine
import pandas as pd

print pd.__version__

#db.create_all()
'''
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
Location = 'PTC_Room_Assignments.csv'
df = pd.read_csv(Location, names=['teacher','department','room','description'])
engine = create_engine('sqlite:///app.db')
df.to_sql(engine, models.PTQueue)
'''
