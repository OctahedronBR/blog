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

from functools import wraps
from google.appengine.api import users, urlfetch
from flask import redirect, request, render_template
from postmarkup import render_bbcode
import model
import re

# Decorators
def login_required(func):
	@wraps(func)
	def decorated_view(*args, **kwargs):
		if not users.get_current_user():
			return redirect(users.create_login_url(request.url))
		return func(*args, **kwargs)
	return decorated_view
	
def admin_required(func):
	@wraps(func)
	def decorated_view(*args, **kwargs):
		if not users.is_current_user_admin():
			return redirect(users.create_login_url(request.url))
		return func(*args, **kwargs)
	return decorated_view

# Other
def render(template_name, **kwargs):
	user = users.get_current_user()
	config = model.get_config()
	return render_template(template_name, config=config, user=user, **kwargs)

_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')

_html_code_re = re.compile(r'<[\w ="/]+>')
_html_accent_re = re.compile(r'&[a-zA-Z]+')

def slugify(value):
	value = _slugify_strip_re.sub('', value).strip().lower()
	return _slugify_hyphenate_re.sub('-', value)

def strip_html_code(value):
	return _html_accent_re.sub('', _html_code_re.sub('', value))

def bbcode_to_html(value):
	return render_bbcode(value)

def do_ping(url):
	result = urlfetch.fetch(url)
	return result.status_code 

