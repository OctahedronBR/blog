{% extends "layout.tpl" %}
{% block body %}
	<div class="section">
		<h2>Configuração</h2>
		<div class="margin">
			<p class="warning"></p>
			<form action="/config/save" method="post">
				<fieldset>
					<label for="blogname">Nome do Blog</label> <br />
					<input type="text" name="blogname" value="{{ config.blogname }}" class="normal-width"/> <br />
					<label for="url">URL</label> <br />
					<input type="text" name="url" value="{{ config.url }}" class="normal-width"/> <br />
					<label for="desc">Descrição</label> <br />
					<textarea name="desc" class="normal-width">{{ config.desc }}</textarea> <br />
					<label for="lang">Lingua</label> <br />
					<input type="text" name="lang" value="{{ config.lang }}" class="tiny-width"/> <br />
					<input id="submit" type="submit" value="Salvar" />
				</fieldset>
			</form>
		</div>
	</div>
{% endblock %}
{% block scripts %}
	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js"></script>
	<script type="text/javascript" src="/static/js/form.js"></script>
{% endblock %}

