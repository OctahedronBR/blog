# -*- coding: utf-8 -*-
"""
    Octa Blog - Simple blog engine build to run at Google App Engine
    Copyright (C) 2010  Octahedron

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


    @author Danilo Penna Queiroz [daniloqueiroz@octahehedron.com.br]
    @author Vítor Avelino Dutra Magalhães [vitoravelino@octahedron.com.br]
"""

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

# install event recorder for appstats application
from google.appengine.ext.appstats import recording
fullapp = recording.appstats_wsgi_middleware(app)

import routes

