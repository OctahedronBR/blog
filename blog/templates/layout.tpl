<!DOCTYPE HTML>
<html lang="pt-br">
	<head>
		<meta charset="utf-8">

		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
		<meta name="author" content="Octahedron Desenvolvimento de Software LTDA" />
		<meta name="keywords" content="cloud computing, octahedron, soluções, clientes, empresa, blog, alta disponibilidade, realidade, ideias" />

		{%block header %}{% endblock %}

		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
		<meta name="google-site-verification" content="J3vK68sDvX45SktALH9Siv-sUP5Wcd6PFMhv-3sWR3o" />
		<meta name="msvalidate.01" content="8F837D913B4245B0480258530194829E" />

		<link rel="shortcut icon" type="image/x-icon" href="/images/favicon.png" />
		<link rel="stylesheet" type="text/css" href="/css/boilerplate.css" />
		<link rel="stylesheet" type="text/css" href="/css/style.css" />
		<link rel="alternate" type="application/rss+xml" title="{{config.blogname}} Feeds" href="{{config.url}}rss" />

		<!--[if lt IE 9]>
			<script type="text/javascript" src="/js/selectivizr.js"></script>
		<![endif]-->
		<script type="text/javascript" src="/js/libs/modernizr-1.7.min.js"></script>
		<script type="text/javascript" src="/js/libs/head.load.min.js"></script>
		{% block scripts %}{% endblock %}
	</head>
	<body>
		<section id="container">
			<section id="content" class="left">
				{% block body %}{% endblock %}
			</section>
			<aside class="right">
				<hr />
				<header>
					<a href="{{config.url}}">
						<img alt="Octahedron" src="/images/logo-light-normal.png" width="132" height="109" />
					</a><br />
				</header>
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
					<h2>Links</h2>
					{% if config.links %}
					<nav>
						<ul>
						{% for link in config.links %}
							<li><a href="{{link.url}}" target="_blank">{{link.name}}</a></li>
						{% endfor %}
						</ul>
					</nav>
					{% endif %}
				</div>
				<hr />
				<div id="access">
					<h2>Admin</h2>
					<nav>
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
					</nav>
				</div>
			</aside>  <!-- sidebar -->
			<footer>
				<p>Posts mais antigos</p>
			</footer>
		</section> <!-- container -->
		<!--[if lt IE 7 ]>
			<script>head.js("/js/libs/dd_belatedpng.js", function() {DD_belatedPNG.fix("img, .png_bg")}</script>
		<![endif]-->
		{% block scripts_bottom %}{% endblock %}
	</body>
</html>

