{% block stylesheet %}
	<link rel="stylesheet" type="text/css" href="/js/markitup/skins/markitup/style.css" />
	<link rel="stylesheet" type="text/css" href="/js/markitup/sets/bbcode/style.css" />
{% endblock %}
{% extends "layout.tpl" %}
{% block body %}
	<div class="section">
		<h2>Novo post</h2>
		<div class="margin">
			<p class="warning"></p>
			<form action="/post/create" method="post">
				<fieldset>
					<label for="title">
						Título: <br />
						<input type="text" name="title" class="normal-width"/> <br />
					</label>
					<input type="text" name="slug" class="normal-width"/>
					<button id="slugify">Slugify!</button> <br />
					<label for="content">
						Conteúdo: <a href="/help/bbcode" target="_blank">(BBCode?)</a> <br />
						<textarea name="content" class="large-width"></textarea> <br />
					</label>
					<label for="tags">
						Tags: (e.g.: cloud computing, appengine, python) <br />
						<input type="text" name="tags" class="normal-width"/> <br />
					</label>
					<label for="draft">
						<input type="checkbox" name="draft" value="True" />Rascunho <br />
					</label>
					<input id="submit" type="submit" value="Criar" />
				</fieldset>
			</form>
		</div>
	</div>
{% endblock %}
{% block scripts %}
	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js"></script>
	<script type="text/javascript" src="/js/form.js"></script>
	<script type="text/javascript" src="/js/markitup/jquery.markitup.js"></script>
	<script type="text/javascript" src="/js/markitup/sets/bbcode/set.js"></script>
{% endblock %}

