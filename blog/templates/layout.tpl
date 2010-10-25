<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
		<link rel="shortcut icon" type="image/x-icon" href="/static/images/icon48px.png" />
		<link rel="stylesheet" type="text/css" href="/static/css/stylesheet.css">

		<title>Octahedron - Blog</title>
	</head>
	<body>
		<div id="all">
			<div id="content">
				<div id="posts">
					{% block body %}{% endblock %}
				</div>
				<div id="sidebar">
					<div id="side-header">
						<a href="/"><img src="/static/images/logo.png" /></a><br />
						{% if user %}
							Olá {{ user.nickname() }}, toolbar aqui!
						{% endif %}
					</div>
				</div>
			</div>
		</div>
	</body>
</html>

