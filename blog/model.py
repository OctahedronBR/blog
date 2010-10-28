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
	html = bbcode_to_html(striped)
	post = Post(title=form['title'], slug=slug, tags=tags, author=users.get_current_user(), coded_content=striped, html_content=html)
	post.put() #todo: try, catch
	memcache.set_multi({str(post.key()): post, post.slug: post})
	memcache.delete_multi(['index_view', 'all_posts_5'])
	update_sitemap()
	# remover memcache tag

	return post

def update_post(form):
	post = memcache.get(form['key'], namespace=namespace_manager.get_namespace())
	if not post:
		post = Post.all().filter('__key__ =', Key(form['key'])).get()
	if post.slug != slugify(form['slug']):
		memcache.delete_multi([post.slug, post.slug+'_view'], namespace=namespace_manager.get_namespace())
	post.title = form['title']
	post.tags = form['tags'].split(",") if (len(form['tags']) > 0) else []
	post.slug = slugify(form['slug']) if (len(form['slug']) > 0) else slugify(form['title'])
	post.coded_content = strip_html_code(form['content'])
	post.html_content = bbcode_to_html(post.coded_content)
	post.put() #todo: try, catch
	memcache.set_multi({str(post.key()): post, post.slug: post}, namespace=namespace_manager.get_namespace())
	memcache.delete_multi(['index_view', 'all_posts_5', post.slug+'_view'], namespace=namespace_manager.get_namespace())
	update_sitemap()
	# remover memcache tag

	return post

def get_all_posts(size=5):
	posts = memcache.get('all_posts_'+str(size))
	if not posts:
		posts = Post.all().order('-when').fetch(size)
		memcache.set('all_posts_'+str(size), posts)
	return posts

def get_post_by_key(key):
	post = memcache.get(key)
	if not post:
		post = Post.all().filter('__key__ =', Key(key)).get()
		memcache.set(key, post)
	return post

def get_post_by_slug(slug):
	post = memcache.get(slug)
	if not post:
		post = Post.all().filter('slug =', slug).get()
		memcache.set(slug, post)
	return post

def get_posts_by_tag(tag, size=5):
	# recuperar do memcache
	return Post.all().filter('tags =', tag).fetch(size)

def configure(form):
	config = Config.all().get()
	if not config:
		config = Config()
	config.blogname = form['url']
	config.url = form['url']
	config.desc = form['desc']
	config.lang = form['lang']

	#adjust url
	config.url = config.url.strip()
	if not config.url.endswith('/'):
		config.url += '/'

	config.put()
	memcache.set('config', config)

def get_config():
	config = memcache.get('config')
	if not config:
		config = Config.all().get()
		memcache.set('config', config)
	return config

def get_sitemap():
	sitemap = memcache.get('sitemap')
	if not sitemap:
		sitemap = Sitemap.all().get()
		if not sitemap:
			sitemap = Sitemap()
			sitemap.content = render('sitemap.tpl', posts=get_all_posts())
			sitemap.put()
		memcache.set('sitemap', sitemap)
	return sitemap

def update_sitemap():
	sitemap = get_sitemap()
	if not sitemap:
		sitemap = Sitemap()
	sitemap.content = render('sitemap.tpl', posts=get_all_posts())
	sitemap.put()
	memcache.set('sitemap', sitemap)
	memcache.delete('sitemap_view')
	# submit to Google Webmaster Tools

# Classes
class Post(db.Model):
	title = db.StringProperty(required = True)
	slug = db.StringProperty(required = True)
	coded_content = db.TextProperty(required = True)
	html_content = db.TextProperty(required = True)
	when = db.DateTimeProperty(auto_now_add = True)
	tags = db.StringListProperty()
	author = db.UserProperty(required = True)

class Config(db.Model):
	blogname = db.StringProperty()
	url = db.StringProperty()
	desc = db.StringProperty()
	lang = db.StringProperty()

class Sitemap(db.Model):
	content = db.TextProperty()

