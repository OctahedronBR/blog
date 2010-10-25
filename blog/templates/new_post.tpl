{% extends "layout.tpl" %}
{% block body %}
	<p class="warning"></p>
	<form action="/post/create" method="post">
		<fieldset>
			<label for="title">Título</label> <br />
			<input type="text" name="title" /> <br />
			<input type="text" name="slug" />
			<button id="slugify">Slugify!</button> <br />
			<label for="content">Conteúdo</label> <br />
			<textarea name="content"></textarea> <br />
			<label for="tags">Tags</label> <br />
			<input type="text" name="tags" /> <br />
			<input id="submit" type="submit" value="Criar" />
		</fieldset>
	</form>

	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js"></script>
	<script type="text/javascript" src="/static/js/form.js"></script>
{% endblock %}

