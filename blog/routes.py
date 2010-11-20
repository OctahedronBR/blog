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

from StringIO import StringIO
from flask import url_for, request, redirect, abort
from simplejson.encoder import JSONEncoder
from blog import app, model
from blog.model import Post, Config
from blog.util import render, render_xml, render_json, login_required, slugify, do_ping
from google.appengine.api import users, namespace_manager, memcache
import feedgenerator, logging

# MISC #
@app.before_request
def before_request():
	if (request.url_root.find("localhost") == -1):
		namespace = request.url_root[7:-1]
		logging.debug("Namespace set to %s" %namespace)	
		namespace_manager.set_namespace(namespace)

@app.route('/')
def index():
	if not model.get_config():
		return redirect(url_for('new_config'))
	else:
		page = render("index.tpl", posts=model.get_all_posts())
		return page

@app.route('/login')
def login():
	return redirect(users.create_login_url(url_for('index')))

@app.route('/logout')
def logout():
	return redirect(users.create_logout_url(url_for('index')))

@app.errorhandler(404)
def page_not_found(error):
	page = memcache.get('error_view')
	if not page:
		page = render('not_found.tpl')
		memcache.set('error_view', page)
	return page, 404

# CONFIG BEGIN #
@app.route('/config/new')
@login_required
def new_config():
	if model.get_config():
		return redirect(url_for('edit_config'))
	else:
		return render("config_new.tpl")

@app.route('/config/edit')
@login_required
def edit_config():
	return render("config_edit.tpl", saved=False)

@app.route('/config/save', methods=['POST'])
@login_required
def configure():
	model.configure(request.form)
	return render("config_edit.tpl", saved=True)

@app.route('/config/add_link')
@login_required
def add_link():
	return render("add_link.tpl")

@app.route('/config/add_link', methods=['POST'])
@login_required
def save_link():
	model.add_link(request.form)
	return redirect(url_for('edit_config'))

@app.route('/config/remove_link/<link_name>')
@login_required
def remove_link(link_name):
	model.remove_link(link_name)
	return redirect(url_for('edit_config'))
# CONFIG END #

# POST BEGIN #
@app.route('/post/new')
@login_required
def new_post():
	page = memcache.get('post_new_view')
	if not page:
		page = render("post_new.tpl")
		memcache.set('post_new_view', page)
	return page

@app.route('/post/create', methods=['POST'])
@login_required
def create_post():
	post = model.create_post(request.form)
	if post:
		if post.as_draft:
			return redirect(url_for('drafts'))
		else:
			return redirect(url_for('slug', slug=post.slug))
	else:
		# todo: error message
		return redirect(url_for('new_post'))

@app.route('/post/edit/<key>')
@login_required
def edit_post(key):
	post = model.get_post_by_key(key)
	if post:
		if post.as_draft:
			return render("post_edit.tpl", post=post, draft=True, tags=",".join(post.tags))
		else:
			return render("post_edit.tpl", post=post,tags=",".join(post.tags))
	else:
		# todo: error message
		return redirect(url_for('index'))

@app.route('/post/update', methods=['POST'])
@login_required
def update_post():
	post = model.update_post(request.form)
	if post:
		if post.as_draft:
			return redirect(url_for('drafts'))
		else:
			return redirect(url_for('slug', slug=post.slug))
	else:
		# todo: error message
		return redirect(url_for('edit_post', key=post.key()))


@app.route('/drafts')
@login_required
def drafts():
	page = render("drafts.tpl", posts=model.get_all_drafts())
	return page

@app.route('/remove/<key>')
@login_required
def remove(key):
	model.delete_post(key)
	return redirect(url_for('index'))

@app.route('/publish/<key>')
@login_required
def publish(key):
	model.publish_draft(key)
	return redirect(url_for('index'))

@app.route('/<slug>')
def slug(slug):
	post = model.get_post_by_slug(slug)
	if not post:
		return abort(404)
	page = render("post_view.tpl", post=post)
	return page

@app.route('/tag/<tag>')
def tag(tag):
	# TODO check tpl page
	return render("index.tpl", posts=model.get_posts_by_tag(tag))
# POST END #

# API BEGIN #
@app.route('/sitemap.xml')
def sitemap():
	sitemap = memcache.get('sitemap_view')
	if not sitemap:
		sitemap = model.get_sitemap().content
		memcache.set('sitemap_view', sitemap)
	return render_xml(sitemap)

@app.route('/json')
@app.route('/json/<int:limit>')
def json(limit=10):
	posts = model.get_all_posts(limit)
	to_json = []
	for post in posts:
		entry = {}
		entry['title'] = post.title
		entry['slug'] = request.url_root + post.slug
		entry['author'] = post.author.nickname()
		entry['when'] = post.when.strftime("%d %b %Y %I:%M:%S %p")
		entry['content'] = post.html_content
		entry['tags'] = post.tags
		to_json.append(entry)
	return render_json(JSONEncoder().encode(to_json))

@app.route('/rss')
@app.route('/rss/<int:limit>')
def rss(limit=10):
	config = model.get_config()
	#TODO load info from properties
	# we can create and property for each blog
	feed = feedgenerator.Rss201rev2Feed(title=config.blogname,
									link=config.url,
									feed_url=config.url + "rss",
									description=config.desc,
									language=config.lang)

	posts = model.get_all_posts(limit)
	for post in posts:
		feed.add_item(title=post.title,
					link=request.url_root + post.slug,
					author_name = post.author.nickname(),
					description=post.html_content,
					pubdate = post.when)
	out = StringIO()
	feed.write(out, 'utf-8')
	try:
		return out.getvalue()
	finally:
		out.close()
# API END #

