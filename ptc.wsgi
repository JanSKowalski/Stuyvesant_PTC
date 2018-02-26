#!/var/www/ptc/ptc/venv/bin/python
activate_this = '/var/www/ptc/ptc/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0,"/var/www/ptc/")

import site

site.addsitedir('/var/www/ptc/ptc/venv/lib/python2.7/site-packages')


from ptc import ptc as application

