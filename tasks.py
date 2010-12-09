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
import logging
from blog.util import do_ping, twit
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.appstats import recording
from google.appengine.api import namespace_manager


def set_namespace(request):
	url = request.url[7:len(request.url)]
	if (url.find("localhost") == -1):
		namespace = url[0:url.find('/')]
		logging.debug("Namespace set to %s" %namespace)	
		namespace_manager.set_namespace(namespace)
	
class PingWorker(webapp.RequestHandler):
	"""
	Worker to handler ping requests
	"""
	def get(self, service): 
		set_namespace(self.request)
		code = do_ping(service)
		logging.debug("ping sitemap! (status code: %d -  service: %s)", code, service)

class TwitterWorker(webapp.RequestHandler):
	"""
	Worker to handler ping requests
	"""
	def get(self, key): 
		set_namespace(self.request)
		msg = twit(key)
		logging.debug("twitting post! (msg: %s - length: %d)", msg, len(msg))


def main():
	# create app
	app = webapp.WSGIApplication([('/tasks/ping/(.*)', PingWorker),
								('/tasks/twit/(.*)', TwitterWorker)])
	# instrument app for appstats
	app = recording.appstats_wsgi_middleware(app)
	# run the app
	run_wsgi_app(app)

if __name__ == '__main__':
	main()
