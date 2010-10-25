from google.appengine.ext import db
from google.appengine.ext.db import Key
from google.appengine.api import users
from blog import app
from blog.util import slugify
import traceback

# Facade
def create_post(form):
	try:
		slug = (slugify(form['title']), form['slug'])[len(form['slug']) > 0] # ternary operation, python 2.4
		tags = form['tags'].split(",")
		post = Post(title=form['title'], slug=slug, content=form['content'], tags=tags, author=users.get_current_user())
		post.put()
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
		post.content = form['content']
		post.put() #todo: try, catch

		return post
	else:
		return false

def get_all_posts():
	return Post.all().fetch(5)

def get_post_by_key(key):
	return Post.all().filter("__key__ =", Key(key)).get()

def get_post_by_slug(slug):
	return Post.all().filter("slug =", slug).get()

# Classes
class Post(db.Model):
    title = db.StringProperty(required = True)
    slug = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    when = db.DateTimeProperty(auto_now_add = True)
    tags = db.StringListProperty()
    author = db.UserProperty(required = True)

