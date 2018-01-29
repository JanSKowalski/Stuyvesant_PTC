import os
import flask.ext.whooshalchemy
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'This-is-a-secret-key'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# set the location for the whoosh index
WHOOSH_BASE = os.path.join(basedir, 'search.db')
