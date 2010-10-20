{% extends "layout.tpl" %}
{% block body %}
	<p class="warning"></p>
	<form action="/post/update" method="post">
		<fieldset>
			<input type="hidden" name="key" value="{{ post.key() }}" />
			<label for="title">Título</label> <br />
			<input id="title" type="text" name="title" value="{{ post.title }}" /> <br />
			<label for="content">Conteúdo</label> <br />
			<textarea id="content" type="text" name="content">{{ post.content }}</textarea> <br />
			<input id="submit" type="submit" value="Atualizar" />
		</fieldset>
	</form>

	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js"></script>
	<script type="text/javascript" src="/static/js/validation.js"></script>
{% endblock %}

