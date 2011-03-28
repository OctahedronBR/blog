{% extends "layout.tpl" %}
{% block header %}
	<link rel="stylesheet" type="text/css" href="/js/markitup/skins/markitup/style.css" />
	<link rel="stylesheet" type="text/css" href="/js/markitup/sets/bbcode/style.css" />
	<title>{{config.blogname}} | Novo post</title>
{% endblock %}
{% block scripts %}
	<script>
		head.js("http://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js", "/js/form.js", "/js/markitup/jquery.markitup.js", "/js/markitup/sets/bbcode/set.js");
	</script>
{% endblock %}
{% block body %}
	<section class="intern">
		<h2>Novo post</h2>
		<p class="warning"></p>
		<form action="/post/create" method="post">
			<fieldset>
				<label for="title">
					Título: <br />
					<input type="text" name="title" class="normal-width"/> <br />
				</label>
				<input type="text" name="slug" class="normal-width"/>

				<button id="slugify">Slugify!</button> <br />

				<label for="desc">
					Descrição do conteúdo: (~160 caracteres / <a href="http://en.wikipedia.org/wiki/Search_engine_optimization" target="_blank">SEO</a>) <br />
					<textarea id="desc" name="desc" class="large-width"></textarea> <br />
				</label>

				<label for="content">
					Conteúdo: <a href="/help/bbcode" target="_blank">(BBCode?)</a> <br />
					<textarea id="content" name="content" class="large-width"></textarea> <br />
				</label>

				<label for="tags">
					Tags: (e.g.: cloud computing, appengine, python) <br />
					<input type="text" id="tags" name="tags" class="normal-width"/> <br />
				</label>

				<label for="draft">
					<input type="checkbox" id="draft" name="draft" value="True" /> Rascunho <br />
				</label>

				<input id="submit" type="submit" value="Criar" />
			</fieldset>
		</form>
	</section>
{% endblock %}
