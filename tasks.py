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
from blog.util import do_ping
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.appstats import recording

class PingWorker(webapp.RequestHandler):
	"""
	Worker to handler ping requests
	"""
	def get(self, service): 
		code = do_ping(service)
		logging.debug("ping sitemap! (status code: %d -  service: %s)", code, service)


def main():
	# create app
	app = webapp.WSGIApplication([('/tasks/ping/(.*)', PingWorker)])
	# instrument app for appstats
	app = recording.appstats_wsgi_middleware(app)
	# run the app
	run_wsgi_app(app)

if __name__ == '__main__':
	main()
