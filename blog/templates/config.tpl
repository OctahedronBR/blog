{% extends "layout.tpl" %}
{% block body %}
	<p class="warning"></p>
	<form action="/config/save" method="post">
		<fieldset>
			<label for="blogname">Nome do Blog</label> <br />
			<input type="text" name="blogname" value="{{config.blogname}}"/> <br />
			<label for="url">URL</label> <br />
			<input type="text" name="url" value="{{config.url}}"/> <br />
			<label for="desc">Descrição</label> <br />
			<textarea name="desc">{{config.desc}}</textarea> <br />
			<label for="lang">Lingua</label> <br />
			<input type="lang" name="lang" value="{{config.blogname}}"/> <br />
			<input id="submit" type="submit" value="Salvar" />
		</fieldset>
	</form>

	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js"></script>
	<script type="text/javascript" src="/static/js/form.js"></script>
{% endblock %}