from ptc import ptc, db, login_manager
import datetime
import flask_whooshalchemy as whooshalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, DATETIME
from flask_login import UserMixin #Generic Authentication Functions


#class Statistics(db.Model):





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
        return '<ID %d>\n' % (self.id)



#Many-to-many relationship with Parents
class PTQueue(db.Model):
    __tablename__ = 'PTQueue'
    __searchable__ = ['teacher', 'room', 'department', 'description'] #, 'opt_in']


    id = db.Column(db.Integer, primary_key=True)
    teacher = db.Column(db.String(128), index=True, unique=False)
    room = db.Column(db.String(64), index=True, unique=False)
    department = db.Column(db.String(128), index=True, unique=False)
    description = db.Column(db.String(128), index=True, unique=False)
    parents_seen = db.Column(db.Integer, index=True, unique=False)
    avg_time = db.Column(db.Float, index=True, unique=False)
    previous_time = db.Column(db.DateTime, index=True, unique=False)
    opt_in = db.Column(db.Boolean, index=True, unique=False)
    parents = db.relationship('Parent', secondary=queues,
                            backref=db.backref('queues', lazy='dynamic'))
    parent_times = db.Column(db.DateTime, index=False, unique=False)


    @staticmethod
    def __init__(self, teacher, room, department, description, opt_in):
        self.parents = []
        self.teacher = teacher
        self.room = room
        self.department = department
        self.description = description
        self.opt_in = opt_in
        self.parents_seen = 0
        self.avg_time = 3.0
        self.previous_time = None

    @staticmethod
    def get_id(self):
        return unicode(self.id)


    @staticmethod
    def get_avg_time(self):
        return self.avg_time


    @staticmethod
    def get_parent_position(self, parent):
        try:
            position = self.parents.index(parent)
        except ValueError:
            position = -1
        return position


    @staticmethod
    def get_parent_time(self, parent):
    	avg_time = self.avg_time
        position = self.get_parent_position(self, parent)
        current_time = datetime.datetime.now()
        time_change = datetime.timedelta(0, (int(avg_time)*position*60)) #Converting to seconds
        estimated_time = current_time + time_change
        return estimated_time.strftime('%I : %M')


    #Returns Parent object
    @staticmethod
    def get_next(self):
        return self.parents[0]


    @staticmethod
    def isEmpty(self):
        return self.parents == []


    def enqueue(self, parent):
        self.parents.append(parent)


    def dequeue(self):
        x = self.parents_seen
        parents_seen = x + 1
        current_time = datetime.datetime.now()
        #This setup updates the avg time of teachers
        if (self.previous_time is not None):
            time_change = current_time - self.previous_time
            self.avg_time = (avg_time*parents_seen + time_change)/parents_seen
        previous_time = current_time
        return self.parents.pop(0)

    @staticmethod
    def size(self):
        return len(self.parents)

    def __repr__(self):
        return '<Id %d>\n' % (self.id)


#Allows whoosh to build an indexing database
whooshalchemy.whoosh_index(ptc, Parent)
whooshalchemy.whoosh_index(ptc, PTQueue)
