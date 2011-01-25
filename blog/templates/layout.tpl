<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
		<meta name="author" content="Octahedron Desenvolvimento de Software LTDA" />
		<meta name="msvalidate.01" content="8F837D913B4245B0480258530194829E" />

		<link rel="shortcut icon" type="image/x-icon" href="/images/icon48px.png" />
		<link rel="stylesheet" type="text/css" href="/css/reset.css" />
		<link rel="stylesheet" type="text/css" href="/css/stylesheet.css" />
		<link rel="alternate" type="application/rss+xml" title="{{config.blogname}} Feeds" href="{{config.url}}rss" />
		{%block header %}
		{% endblock %}
	</head>
	<body>
		<div id="content">
			<div id="main" class="left">
				{% block body %}{% endblock %}
			</div>
			<div id="sidebar" class="right">
				<hr />
				<div id="header">
					<a href="{{config.url}}"><img alt="Octahedron" src="/images/logo.png" /></a><br />
				</div>
				<hr />
				<div class="search">
					<form action="http://www.google.com/search" method="get">
						<fieldset>
							<input type="hidden" name="sitesearch" value="{{ config.url }}" />
							<input type="text" name="q" />
						</fieldset>
					</form>
				</div>
				<hr />
				<div id="links">
					<h2>_Links</h2>
					{% if config.links.count() > 0 %}
					<ul>
					{% for link in config.links %}
						<li><a href="{{link.url}}" target="_blank">{{link.name}}</a></li>
					{% endfor %}
					</ul>
					{% endif %}
				</div>
				<hr />
				<div id="access">
					<h2>_Admin</h2>
					<ul>
						{% if user %}
						<li><a href="/logout">Logout</a></li>
						<li><a href="/post/new">Criar post</a></li>
						<li><a href="/drafts">Rascunhos</a></li>
						<li><a href="/config/edit">Editar configurações</a></li>
						{% else %}
						<li><a href="/login">Login</a></li>
						{% endif %}
					</ul>
				</div>
			</div>  <!-- sidebar -->
			<div id="footer">
				<p>Posts mais antigos</p>
			</div>
		</div> <!-- content -->
		{% block scripts %}{% endblock %}
	</body>
</html>

