activate_this = '/var/www/score/project/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
import sys
import logging
print(sys.path)
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/score/project")

from score import app as application
