<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
		<link rel="shortcut icon" type="image/x-icon" href="/static/images/icon48px.png" />
		<link rel="stylesheet" type="text/css" href="/static/css/reset.css">
		<link rel="stylesheet" type="text/css" href="/static/css/stylesheet.css">

		<title>Octahedron - Blog</title>
	</head>
	<body>
		<div id="content">
			<div id="main" class="left">
				{% block body %}{% endblock %}
			</div>
			<div id="sidebar" class="right">
				<div id="header">
					<a href="/"><img alt="Octahedron" src="/static/images/logo.png" /></a><br />
				</div>
				<hr />
				<div class="search">
					<form action="/search" method="get">
						<fieldset>
							<input type="text" name="q" />
						</fieldset>
					</form>
				</div>
				<hr />
				<div id="links">
					<h2>_Links</h2>
					<ul>
						<li><a href="">link1</a></li>
						<li><a href="">link1</a></li>
						<li><a href="">link1</a></li>
						<li><a href="">link1</a></li>
						<li><a>link1</a></li>
						<li><a>link1</a></li>
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

