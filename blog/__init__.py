import sys, os

LOCAL = os.environ["SERVER_SOFTWARE"].startswith("Development")
if LOCAL:
    from google.appengine.tools.dev_appserver import FakeFile
    FakeFile.SetAllowedPaths('/', [])
    sys.meta_path = [] # disables python sandbox in local version

if 'werkzeug.zip' not in sys.path: sys.path.insert(0, 'werkzeug.zip');
if 'flask.zip' not in sys.path: sys.path.insert(0, 'flask.zip');
if 'simplejson.zip' not in sys.path: sys.path.insert(0, 'simplejson.zip');
if 'jinja2.zip' not in sys.path: sys.path.insert(0, 'jinja2.zip');

import werkzeug 
from flask import Flask
import settings

app = Flask('blog')
app.config.from_object('blog.settings')
import routes

