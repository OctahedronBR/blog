from functools import wraps
import model
from google.appengine.api import users
from flask import redirect, request, render_template
import re
from postmarkup import render_bbcode

# Decorators
def login_required(func):
	@wraps(func)
	def decorated_view(*args, **kwargs):
		if not users.get_current_user():
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

