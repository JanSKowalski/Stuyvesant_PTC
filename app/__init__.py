from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from config import basedir, WHOOSH_BASE


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Important for this app import to come after app is redefined
from app import views, models
