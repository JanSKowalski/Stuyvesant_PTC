from ptc import ptc, db, login_manager
import datetime
import flask_whooshalchemy as whooshalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, DATETIME
from flask_login import UserMixin #Generic Authentication Functions

# For student and admin user accounts only
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128), index=False, unique=False)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))



# Association table for many-to-many rlationship
queues = db.Table('queues',
    db.Column('parent_id', db.Integer, db.ForeignKey('Parent.id')),
    db.Column('ptqueue_id', db.Integer, db.ForeignKey('PTQueue.id'))
)

#Many-to-Many relationship with PTQueues
class Parent(db.Model):
    __tablename__ = 'Parent'
    __searchable__ = ['id', 'parent_name', 'child_dob', 'child_name']#, 'email']
    id = db.Column(db.Integer, primary_key=True)
    parent_name = db.Column(db.String(32), index=True, unique=False)
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


    __mapper_args__ = {
        'confirm_deleted_rows': False
    }



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
	#-------------------------#
	#	Statistics	  #
	#-------------------------#
	self.parents_seen = 0
	self.avg_time = 3

    @staticmethod
    def get_id(self):
        return unicode(self.id)


    @staticmethod
    def get_time(self):
        return unicode(self.avg_time)


    #Returns Parent object
    @staticmethod
    def get_next(self):
        return self.parents[0]


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
        #self.parents_seen = x + 1

        return self.parents.pop(0)

    @staticmethod
    def size(self):
        return len(self.parents)

    def __repr__(self):
        return '<Id %d, Parents %r, Teacher %r, Room %r>\n\n' % (self.id, self.parents, self.teacher, self.room)


#Allows whoosh to build an indexing database
whooshalchemy.whoosh_index(ptc, Parent)
whooshalchemy.whoosh_index(ptc, PTQueue)
