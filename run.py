#!flask/bin/python
from app import app

if __name__ == "__main__":
    app.debug = True
    app.use_reloader = False
    app.run(debug = True, port = 5016)
