from flask import render_template, url_for, request, redirect, _request_ctx_stack
from blog import app
from blog.models import Post
from blog.util import render, login_required, slugify
from google.appengine.api import users
from google.appengine.ext.db import Key

@app.route('/')
def index():
	posts = Post.all().fetch(5)
	return render("index.tpl", posts=posts)

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
	params = request.form
	slug = slugify(params['title'])
	post = Post(title=params['title'], content=params['content'], author=users.get_current_user(), slug=slug)
	# todo try, catch
	post.put()
	return redirect(url_for('slug', slug=slug))

@app.route('/post/edit/<key>')
@login_required
def post_edit(key):
	post = Post.all().filter("__key__ =", Key(key)).get()
	if post:
		return render("edit_post.tpl", post=post)
	else:
		return redirect(url_for('index'))

@app.route('/post/update', methods=['POST'])
@login_required
def post_update():
	params = request.form
	post_key = Key(params['key'])
	# todo update post
	return redirect(url_for('slug', post_key=post_key))

@app.route('/<slug>')
def slug(slug):
	post = Post.all().filter("slug =", slug).get()
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

