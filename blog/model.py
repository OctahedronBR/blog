from google.appengine.ext import db
from google.appengine.ext.db import Key
from google.appengine.api import users, memcache, namespace_manager
from blog.util import render, slugify, strip_html_code, bbcode_to_html
import traceback

# Facade
def create_post(form):
	slug = slugify(form['slug']) if (len(form['slug']) > 0) else slugify(form['title'])
	tags = form['tags'].split(",") if (len(form['tags']) > 0) else []
	striped = strip_html_code(form['content'])
	as_draft = form.has_key('draft')
	html = bbcode_to_html(striped)
	post = Post(title=form['title'], slug=slug, tags=tags, author=users.get_current_user(), coded_content=striped, html_content=html, as_draft=as_draft)
	post.put() 
	memcache.set_multi({str(post.key()): post})
	memcache.delete_multi(['all_posts_5', 'all_drafts_5'])
	update_sitemap()
	return post

def update_post(form):
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
	memcache.delete_multi(['all_posts_5','all_drafts_5'])
	update_sitemap()
	# remover memcache tag
	return post

def delete_post(key):
	post = get_post_by_key(key)
	db.delete(post)
	memcache.delete_multi(['all_posts_5','all_drafts_5',str(post.key())])

def publish_draft(key):
	draft = get_post_by_key(key)
	draft.as_draft = False
	draft.put()
	memcache.delete_multi(['all_posts_5','all_drafts_5',str(draft.key())])

def get_all_posts(size=5):
	posts = memcache.get('all_posts_'+str(size))
	if not posts:
		posts = Post.all().filter("as_draft !=", True).order('as_draft').order('as_draft').order('-when').fetch(size)
		memcache.set('all_posts_'+str(size), posts)
	return posts

def get_all_drafts(size=5):
	drafts = memcache.get('all_drafts_'+str(size))
	if not drafts:
		drafts = Post.all().filter("as_draft =", True).order('-when').fetch(size)
		memcache.set('all_drafts_'+str(size), drafts)
	return drafts

def get_post_by_key(key):
	post = memcache.get(key)
	if not post:
		post = Post.all().filter('__key__ =', Key(key)).get()
		memcache.set(key, post)
	return post

def get_post_by_slug(slug):
	post = memcache.get(slug)
	if not post:
		post = Post.all().filter('slug =', slug).filter("as_draft !=", True).order('as_draft').get()
		memcache.set(slug, post)
	return post

def get_posts_by_tag(tag, size=5):
	# recuperar do memcache
	return Post.all().filter('tags =', tag).filter("as_draft !=", True).order('as_draft').fetch(size)

def configure(form):
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
	name = form['name']
	url = db.Link(form['url'])
	link = Link(name=name, url=url, blog=get_config())
	link.put()

def remove_link(name):
	links = Link.all().filter('name =', name).fetch(100)
	db.delete(links)

def get_config():
	config = memcache.get('config')
	if not config:
		config = Config.all().get()
		memcache.set('config', config)
	return config

def __update_sitemap(sitemap):
	sitemap.content = render('sitemap.tpl', posts=get_all_posts())
	sitemap.put()
	memcache.set('sitemap', sitemap)
	memcache.delete('sitemap_view')
	# submit to Google Webmaster Tools

def get_sitemap():
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

