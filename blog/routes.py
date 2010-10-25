from StringIO import StringIO

from flask import render_template, url_for, request, redirect
from simplejson.encoder import JSONEncoder
from blog import app, model
from blog.model import Post
from blog.util import render, login_required, slugify, get_slug_link
from google.appengine.api import users, namespace_manager
import feedgenerator


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
	#TODO load info from properties
	# we can create and property for each blog
	feed = feedgenerator.Rss201rev2Feed(title=u"Poynter E-Media Tidbits",
									link=request.url_root,
									feed_url=urequest.url_root + "rss",
									description=u"A group weblog by the sharpest minds in online media/journalism/publishing.",
									language=u"en")
	
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
