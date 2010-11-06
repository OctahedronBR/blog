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

from google.appengine.ext import db
from google.appengine.ext.db import Key
from google.appengine.api import users, memcache
from blog.util import render, slugify, strip_html_code, bbcode_to_html, ping_services

# Facade
def create_post(form):
	"""
	Creates and saves a new post.
	When a post is created, it's put at cache (by key) and the cache for all posts/drafts
	is cleaned.
	"""
	slug = slugify(form['slug']) if (len(form['slug']) > 0) else slugify(form['title'])
	tags = form['tags'].split(",") if (len(form['tags']) > 0) else []
	striped = strip_html_code(form['content'])
	as_draft = form.has_key('draft')
	html = bbcode_to_html(striped)
	post = Post(title=form['title'], slug=slug, tags=tags, author=users.get_current_user(), coded_content=striped, html_content=html, as_draft=as_draft)
	post.put() 
	memcache.set(str(post.key()), post)
	memcache.delete_multi(['all_posts_10', 'all_drafts_10'])
	update_sitemap()
	return post

def update_post(form):
	"""
	Updates an existent post. Post is identified by it unique key
	When a post is updated, it's put at cache (by key) and the cache for all posts/drafts
	is cleaned.
	"""
	post = memcache.get(form['key'])
	if not post:
		post = Post.all().filter('__key__ =', Key(form['key'])).get()
	if post.slug != slugify(form['slug']):
		memcache.delete(post.slug)
	post.title = form['title']
	post.tags = form['tags'].split(",") if (len(form['tags']) > 0) else []
	post.slug = slugify(form['slug']) if (len(form['slug']) > 0) else slugify(form['title'])
	post.coded_content = strip_html_code(form['content'])
	post.html_content = bbcode_to_html(post.coded_content)
	post.as_draft = form.has_key('draft')	
	post.put() #todo: try, catch
	memcache.set(str(post.key()), post)
	memcache.delete_multi(['all_posts_10','all_drafts_10', post.slug])
	update_sitemap()
	# remover memcache tag
	return post

def delete_post(key):
	"""
	Deletes the post with the given key.
	The post is also removed from cache
	"""
	post = get_post_by_key(key)
	db.delete(post)
	memcache.delete_multi(['all_posts_10','all_drafts_10',str(post.key()), post.slug])
	update_sitemap()

def publish_draft(key):
	"""
	Removes 'as_draft' mark from the post with the given key
	Cache adjusted
	"""
	draft = get_post_by_key(key)
	draft.as_draft = False
	draft.put()
	memcache.delete_multi(['all_posts_10','all_drafts_10',str(draft.key())])

def get_all_posts(size=10):
	"""
	Gets all published posts.
	""" 
	posts = memcache.get('all_posts_'+str(size))
	if not posts:
		posts = Post.all().filter("as_draft =", False).order('as_draft').order('-when').fetch(size)
		memcache.set('all_posts_'+str(size), posts)
	return posts

def get_all_drafts(size=10):
	"""
	Gets all draft posts
	"""
	drafts = memcache.get('all_drafts_'+str(size))
	if not drafts:
		drafts = Post.all().filter("as_draft =", True).order('-when').fetch(size)
		memcache.set('all_drafts_'+str(size), drafts)
	return drafts

def get_posts_by_tag(tag, size=10):
	"""
	Gets all published post with a given tag
	"""
	# recuperar do memcache
	return Post.all().filter('tags =', tag).filter("as_draft =", False).fetch(size)


def get_post_by_key(key):
	"""
	Gets a post by key
	"""
	post = memcache.get(key)
	if not post:
		post = Post.all().filter('__key__ =', Key(key)).get()
		memcache.set(key, post)
	return post

def get_post_by_slug(slug):
	"""
	Gets a post by slug
	"""
	post = memcache.get(slug)
	if not post:
		post = Post.all().filter('slug =', slug).filter("as_draft =", False).get()
		memcache.set(slug, post)
	return post

def configure(form):
	"""
	Configures the blog
	"""
	config = Config.all().get()
	if not config:
		config = Config()
	config.blogname = form['blogname']
	config.url = db.Link(form['url'])
	config.desc = form['desc']
	config.lang = form['lang']

	#adjust url
	config.url = config.url.strip()
	if not config.url.endswith('/'):
		config.url += '/'

	config.put()
	memcache.set('config', config)

def add_link(form):
	"""
	Adds a link to the blog configuration
	"""
	name = form['name']
	url = db.Link(form['url'])
	link = Link(name=name, url=url, blog=get_config())
	link.put()

def remove_link(name):
	"""
	Removes a link from blog congiguration
	"""
	links = Link.all().filter('name =', name).fetch(100)
	db.delete(links)

def get_config():
	"""
	Gets the blog configuration. Returns None if there isn't a configuration for blog yet.
	"""
	config = memcache.get('config')
	if not config:
		config = Config.all().get()
		memcache.set('config', config)
	return config

def __update_sitemap(sitemap):
	"""
	Updates the given sitemap. Updates the content, save it to DS and to cache.
	"""
	sitemap.content = render('sitemap.tpl', posts=get_all_posts())
	sitemap.put()
	memcache.set('sitemap', sitemap)
	memcache.delete('sitemap_view')
	ping_services()

def get_sitemap():
	"""
	Gets the blog site map. If it doesn't exists yet, it will be created
	"""
	sitemap = memcache.get('sitemap')
	if not sitemap:
		sitemap = Sitemap.all().get()
		if not sitemap:
			sitemap = Sitemap()
			__update_sitemap(sitemap)
		else:
			memcache.set('sitemap', sitemap)
	return sitemap

def update_sitemap():
	"""
	Updates the blog sitemap
	"""
	__update_sitemap(get_sitemap())

# Classes
class Post(db.Model):
	title = db.StringProperty(required = True)
	slug = db.StringProperty(required = True)
	coded_content = db.TextProperty(required = True)
	html_content = db.TextProperty(required = True)
	when = db.DateTimeProperty(auto_now_add = True)
	tags = db.StringListProperty()
	as_draft = db.BooleanProperty(required = True, default = False)
	author = db.UserProperty(required = True)

class Config(db.Model):
	blogname = db.StringProperty()
	url = db.LinkProperty()
	desc = db.StringProperty()
	lang = db.StringProperty()

class Link(db.Model):
	name = db.StringProperty(required=True)
	url = db.LinkProperty(required=True)
	blog = db.ReferenceProperty(Config, collection_name='links')

class Sitemap(db.Model):
	content = db.TextProperty()

