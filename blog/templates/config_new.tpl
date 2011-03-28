{% extends "layout.tpl" %}
{% block header %}
		<title>{{config.blogname}} | Configuração inicial</title>
{% endblock %}
{% block scripts %}
	<script>
		head.js("http://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js", "/js/form.js");
	</script>
{% endblock %}
{% block body %}
	<section class="intern">
		<h2>Configuração inicial</h2>
		<p class="warning"></p>
		<form action="/config/save" method="post">
			<fieldset>
				<label for="blogname">
					Nome do blog: <br />
					<input type="text" name="blogname" class="normal-width"/> <br />
				</label>
				<label for="url">
					URL: <br />
					<input type="text" name="url" class="normal-width"/> <br />
				</label>
				<label for="desc">
					Descrição: <br />
					<textarea name="desc" class="normal-width"></textarea> <br />
				</label>
				<label for="lang">
					Língua: [e.g.: 'en', 'pt_BR', ...] <br />
					<input tyhead.js("http://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js"pe="text" name="lang" class="tiny-width"/> <br />
				</label>
				<input id="submit" type="submit" value="Salvar" />
			</fieldset>
		</form>
	</section>
{% endblock %}
