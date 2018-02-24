#!flask/bin/python
from app import app, db

if __name__ == "__main__":
    #db.create_all()
    app.debug = False
    app.use_reloader = False
    app.run(debug = False)
