from flask import render_template, url_for, request, redirect
from blog import app, model
from blog.model import Post
from blog.util import render, login_required, slugify
from google.appengine.api import users, namespace_manager

@app.before_request
def before_request():
	if (request.url_root.find("localhost") == -1):
		namespace_manager.set_namespace(request.url_root[8:-1])

@app.route('/')
def index():
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

@app.errorhandler(404)
def page_not_found(error):
	# todo
	return error, 404

# API
@app.route('/json/<int:limit>')
def json(limit):
	#todo
	return "todo"

@app.route('/rss/<int:limit>')
def rss(limit):
	#todo
	return "todo"

