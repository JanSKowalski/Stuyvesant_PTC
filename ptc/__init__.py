from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from config import basedir, WHOOSH_BASE


ptc = Flask(__name__)
ptc.config.from_object('config')
db = SQLAlchemy(ptc)


login_manager = LoginManager(ptc)
#login_manager.init_app(app)
#login_manager.login_view = 'login'

#Important for this app import to come after app is redefined
from ptc import views, models
