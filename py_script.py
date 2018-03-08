from ptc import models, db
from ptc.models import PTQueue, Parent
oli = PTQueue.query.get(11)
parent = Parent.query.get(18)
parent2 = Parent.query.get(15)


oli.get_parent_time(oli, parent)
