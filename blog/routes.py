from StringIO import StringIO
from flask import url_for, request, redirect, make_response, abort
from simplejson.encoder import JSONEncoder
from blog import app, model
from blog.model import Post, Config
from blog.util import render, login_required, slugify
from google.appengine.api import users, namespace_manager, memcache
import feedgenerator

# MISC #
@app.before_request
def before_request():
	if (request.url_root.find("localhost") == -1):
		namespace_manager.set_namespace(request.url_root[8:-1])

@app.route('/')
def index():
	if not model.get_config():
		return redirect(url_for('new_config'))
	else:
		page = memcache.get('index_view')
		if not page:
			page = render("index.tpl", posts=model.get_all_posts())
			memcache.set('index_view', page)
		return page

@app.route('/login')
def login():
	memcache.delete('index_view')
	return redirect(users.create_login_url(url_for('index')))

@app.route('/logout')
def logout():
	memcache.delete('index_view')
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
	return render("config_edit.tpl")

@app.route('/config/save', methods=['POST'])
@login_required
def configure():
	model.configure(request.form)
	return redirect(url_for('index'))
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
		return redirect(url_for('slug', slug=post.slug))
	else:
		# todo: error message
		return redirect(url_for('new_post'))

@app.route('/post/edit/<key>')
@login_required
def edit_post(key):
	post = model.get_post_by_key(key)
	if post:
		return render("post_edit.tpl", post=post, tags=",".join(post.tags))
	else:
		# todo: error message
		return redirect(url_for('index'))

@app.route('/post/update', methods=['POST'])
@login_required
def update_post():
	post = model.update_post(request.form)
	if post:
		return redirect(url_for('slug', slug=post.slug))
	else:
		# todo: error message
		return redirect(url_for('edit_post', key=post.key()))

@app.route('/<slug>')
def slug(slug):
	page = memcache.get(slug+'_view')
	if not page:
		post = model.get_post_by_slug(slug)
		if not post:
			return abort(404)
		page = render("post_view.tpl", post=post)
		memcache.set(slug+'_view', page)
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
	response = make_response(sitemap)
	response.headers['Content-Type'] = 'text/xml'
	return response

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
# API END #

