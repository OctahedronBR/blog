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
from google.appengine.api.labs import taskqueue
from flask import redirect, request, make_response, render_template
from postmarkup import render_bbcode
import model, re, urllib
import tweepy

services = {
		'bing': ("http://www.bing.com/webmaster/ping.aspx","siteMap"),
		'google': ("http://www.google.com/webmasters/sitemaps/ping","sitemap")
		}

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

def render_json(output, callback=''):
	callback = request.args.get('callback', '')
	output = "%s(%s)" % (callback, output)
	response = make_response(output)
	response.headers['Content-Type'] = 'application/json'
	return response

def render_xml(output):
	response = make_response(output)
	response.headers['Content-Type'] = 'text/xml'
	return response

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

def ping_services():
	# enqueue a task for each service to ping
	for service in services.keys():
		taskqueue.add(url='/tasks/ping/%s'%service, method = 'GET')
		
def do_ping(service):
	# get service data (url and param_name)
	url,param_name = services[service]
	# Prepare input date
	sitemap_url = model.get_config().url + 'sitemap.xml'
	form_fields = {param_name: sitemap_url}
	form_data = urllib.urlencode(form_fields)
	# invoke the url fetch
	result = urlfetch.fetch(url,payload=form_data,follow_redirects=True)
	# return status code
	return result.status_code 	

def twit_post(key):
	if model.__is_twitter_configured():
		taskqueue.add(url='/tasks/twit/%s'%key, method = 'GET')


def twit(key):
	config = model.get_config()
	post = model.get_post_by_key(key)
	if not post.as_draft:
		
		auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
		auth.set_access_token(config.access_key, config.access_secret)
		api = tweepy.API(auth)
		
		post_url = config.url + post.slug
		msg = post.title + " " + post_url
		api.update_status(msg)
		return msg
	else:
		return "draft!"