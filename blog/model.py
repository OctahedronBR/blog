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
from blog.util import render, slugify, strip_html_code, bbcode_to_html, ping_services, twit_post
import tweepy

# Facade
def create_post(form):
	"""
	Creates and saves a new post.
	When a post is created, it's put at cache (by key) and the cache for all posts/drafts
	is cleaned.
	"""
	slug = slugify(form['slug']) if (len(form['slug']) > 0) else slugify(form['title'])
	tags = __strip_tags(form['tags'].split(",")) if (len(form['tags']) > 0) else []
	striped = strip_html_code(form['content'])
	desc = form['desc']
	as_draft = form.has_key('draft')
	html = bbcode_to_html(striped)
	post = Post(title=form['title'], slug=slug, tags=tags, desc=desc, author=users.get_current_user(), coded_content=striped, html_content=html, as_draft=as_draft)
	post.put() 
	memcache.set(str(post.key()), post)
	memcache.delete_multi(['all_posts_10', 'all_drafts_10'])
	update_sitemap()
	twit_post(str(post.key()))
	return post

def __strip_tags(tags):
	tags_stripped = []
	for tag in tags:
		tags_stripped.append(tag.strip())
	return tags_stripped

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
	post.tags = __strip_tags(form['tags'].split(",")) if (len(form['tags']) > 0) else []
	post.slug = slugify(form['slug']) if (len(form['slug']) > 0) else slugify(form['title'])
	post.desc = form['desc']
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
	twit_post(str(draft.key()))

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
	config = get_config()
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

def configure_twitter(form):
	"""
	Configure twitter [improve this!]
	"""
	config = get_config()
	config.consumer_key = form['consumer_key']
	config.consumer_secret = form['consumer_secret']
	config.put()
	memcache.set('config', config)
	## prepare twitter
	callback_url = str(config.url) + "twitter/callback"
	auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret, callback_url)
	#auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
	redirect_url = auth.get_authorization_url()
	memcache.set('request_token', (auth.request_token.key,auth.request_token.secret))
	## return url to redirect user
	return redirect_url
	#return callback_url	

def configure_twitter_access(form):
	verifier = form['oauth_verifier']
	config = get_config()
	auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
	token = memcache.get('request_token')
	auth.set_request_token(token[0], token[1])
	auth.get_access_token(verifier)
	config.access_key = auth.access_token.key
	config.access_secret = auth.access_token.secret
	config.put()
	memcache.set('config', config)

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

def __is_twitter_configured():
	config = get_config()
	return config.access_key != None

# Classes
class Post(db.Model):
	title = db.StringProperty(required = True)
	slug = db.StringProperty(required = True)
	desc = db.StringProperty(required = False)
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
	consumer_key = db.StringProperty()
	consumer_secret = db.StringProperty()
	access_key = db.StringProperty()
	access_secret = db.StringProperty()

class Link(db.Model):
	name = db.StringProperty(required=True)
	url = db.LinkProperty(required=True)
	blog = db.ReferenceProperty(Config, collection_name='links')

class Sitemap(db.Model):
	content = db.TextProperty()

