from google.appengine.ext import db
from google.appengine.ext.db import Key
from google.appengine.api import users
from blog.util import slugify, strip_html_code, bbcode_to_html
import traceback

# Facade
def create_post(form):
	try:
		slug = (slugify(form['title']), form['slug'])[len(form['slug']) > 0] # ternary operation, python 2.4
		tags = form['tags'].split(",")
		striped = strip_html_code(form['content'])
		html = bbcode_to_html(striped)
		post = Post(title=form['title'], slug=slug, tags=tags, author=users.get_current_user(), coded_content = striped, html_content = html)
		post.put()
		# adicionar ao memcache por slug, key, tag
		# remover memcache allposts
		return post
	except:
		#todo: error message
		traceback.print_exc()

def update_post(form):
	post = Post.all().filter('__key__ =', Key(form['key'])).get()
	if post:
		post.title = form['title']
		post.tags = form['tags'].split(",")
		post.slug = (slugify(form['title']), form['slug'])[len(form['slug']) > 0]
		post.coded_content = strip_html_code(form['content'])
		post.html_content = bbcode_to_html(post.coded_content)
		post.put() #todo: try, catch
		# adicionar ao memcache por slug
		# remover memcache allposts

		return post
	else:
		return False

def get_all_posts(size=5):
	# recuperar posts do memcache se houver (class + size)
	query = Post.all()
	query.order('-when')
	return query.fetch(size)

def get_post_by_key(key):
	# recuperar do memcache
	return Post.all().filter("__key__ =", Key(key)).get()

def get_post_by_slug(slug):
	# recuperar do memcache
	return Post.all().filter("slug =", slug).get()

def get_posts_by_tag(tag, size = 5):
	# recuperar do memcache
	return Post.all().filter("tags =", tag).fetch(size)

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
	# atualizar memcache
	
def get_config(): 
	# recuperar do memcache
	return Config.all().get()

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
