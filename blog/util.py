from functools import wraps
from google.appengine.api import users
from flask import redirect, request, render_template
import re

# Decorators
def login_required(func):
	@wraps(func)
	def decorated_view(*args, **kwargs):
		if not users.get_current_user():
			return redirect(users.create_login_url(request.url))
		return func(*args, **kwargs)
	return decorated_view

# Other
def render(template_name, **args):
	user = users.get_current_user()
	return render_template(template_name, user=user, **args)

_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')

def slugify(value):
	value = _slugify_strip_re.sub('', value).strip().lower()
	return _slugify_hyphenate_re.sub('-', value)
