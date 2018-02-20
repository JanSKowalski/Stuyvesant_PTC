from app import app, db, login_manager
import datetime
import flask_whooshalchemy as whooshalchemy
import whoosh
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, DATETIME

# For student and admin user accounts only
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(128), index=True, unique=False)



# Association table for many-to-many rlationship
queues = db.Table('queues',
    db.Column('parent_id', db.Integer, db.ForeignKey('Parent.id')),
    db.Column('ptqueue_id', db.Integer, db.ForeignKey('PTQueue.id'))
)

#Many-to-Many relationship with PTQueues
class Parent(db.Model):
    __tablename__ = 'Parent'
    __searchable__ = ['id', 'child_dob' , 'child_name']#, 'email']
    id = db.Column(db.Integer, primary_key=True)
    child_name = db.Column(db.String(128), index=True, unique=False)
    child_dob = db.Column(db.String(32), index=True, unique=False)
    #email = db.Column(db.String(128), index=True, unique=False)
    ptqueues = db.relationship('PTQueue', secondary=queues,
                            backref=db.backref('queues', lazy='dynamic'))

    def __repr__(self):
        return '<Child Name %s>, <Child DoB %s' % (self.child_name, self.child_dob)

#Many-to-many relationship with Parents
class PTQueue(db.Model):
    __tablename__ = 'PTQueue'
    __searchable__ = ['teacher', 'room', 'department', 'description']
    id = db.Column(db.Integer, primary_key=True)
    teacher = db.Column(db.String(128), index=True, unique=True)
    room = db.Column(db.String(64), index=True, unique=False)
    department = db.Column(db.String(128), index=True, unique=False)
    description = db.Column(db.String(128), index=True, unique=False)
    parents_seen = db.Column(db.Integer, index=True, unique=False)
    avg_time = db.Column(db.Integer, index=True, unique=False)
    parents = db.relationship('Parent', secondary=queues,
                            backref=db.backref('queues', lazy='dynamic'))


    @staticmethod
    def __init__(self, teacher, room, department, description):
        self.parents = []
        self.teacher = teacher
        self.room = room
        self.department = department
        self.description = description

    @staticmethod
    def get_id(self):
        return unicode(self.id)

    @staticmethod
    def isEmpty(self):
        return self.parents == []

    @staticmethod
    def enqueue(self, parent):
        #self.parents.insert(0,parent)
        self.parents.append(parent)

    @staticmethod
    def dequeue(self):
        x = self.parents_seen
        x = x + 1
        return self.parents.pop()

    @staticmethod
    def size(self):
        return len(self.parents)

    def __repr__(self):
        return '<Id %d, Parents %r, Teacher %r, Room %r>\n\n' % (self.id, self.parents, self.teacher, self.room)


#Allows whoosh to build an indexing database
whooshalchemy.whoosh_index(app, Parent)
whooshalchemy.whoosh_index(app, PTQueue)
