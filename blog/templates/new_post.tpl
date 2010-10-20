{% extends "layout.tpl" %}
{% block body %}
	<p class="warning"></p>
	<form action="/post/create" method="post">
		<fieldset>
			<label for="title">Título</label> <br />
			<input type="text" name="title" /> <br />
			<label for="content">Conteúdo</label> <br />
			<textarea name="content"></textarea> <br />
			<input id="submit" type="submit" value="Criar" />
		</fieldset>
	</form>

	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js"></script>
	<script type="text/javascript" src="/static/js/validation.js"></script>
{% endblock %}

