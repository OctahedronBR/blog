from StringIO import StringIO
from flask import render_template, url_for, request, redirect
from simplejson.encoder import JSONEncoder
from blog import app, model
from blog.model import Post, Config
from blog.util import render, login_required, slugify
from google.appengine.api import users, namespace_manager
import feedgenerator


@app.before_request
def before_request():
	if (request.url_root.find("localhost") == -1):
		namespace_manager.set_namespace(request.url_root[8:-1])


@app.route('/config')
#@login_required
def create_config():
	if model.get_config():
		return redirect(url_for('edit_config'))
	else:
		return render("create_config.tpl")

@app.route('/config/edit')
#@login_required
def edit_config():
	return render("config.tpl")


@app.route('/config/save', methods=['POST'])
#@login_required
def configure():
	model.configure(request.form)
	return redirect(url_for('edit_config'))

@app.route('/')
def index():
	if not model.get_config():
		return redirect(url_for('create_config'))
	else:
		return render("index.tpl", posts=model.get_all_posts())

@app.route('/login')
def login():
	return redirect(users.create_login_url(url_for('index')))

@app.route('/post/new')
@login_required
def post_new():
	return render("new_post.tpl")

@app.route('/post/create', methods=['POST'])
@login_required
def post_create():
	post = model.create_post(request.form)
	if post:
		return redirect(url_for('slug', slug=post.slug))
	else:
		# todo: error message
		return redirect(url_for('post_new'))

@app.route('/post/edit/<key>')
@login_required
def post_edit(key):
	post = model.get_post_by_key(key)
	if post:
		return render("edit_post.tpl", post=post)
	else:
		# todo: error message
		return redirect(url_for('index'))

@app.route('/post/update', methods=['POST'])
@login_required
def post_update():
	post = model.update_post(request.form)
	if post:
		return redirect(url_for('slug', slug=post.slug))
	else:
		# todo: error message
		return redirect(url_for('index'))

@app.route('/<slug>')
def slug(slug):
	post = model.get_post_by_slug(slug)
	if post:
		return render("post.tpl", post=post)
	else:
		return redirect(url_for('index'))

@app.route('/tag/<tag>')
def tag(tag):
	# TODO check tpl page
	return render("index.tpl", posts=model.get_posts_by_tag(tag))

@app.errorhandler(404)
def page_not_found(error):
	# todo
	return error, 404

# API

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
		entry['content'] = post.content
		entry['tags'] = post.tags
		to_json.append(entry)
	return JSONEncoder().encode(entry)

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
					description=post.content,
					pubdate = post.when)
	out = StringIO()
	feed.write(out, 'utf-8')
	try:
		return out.getvalue()
	finally:
		out.close()
