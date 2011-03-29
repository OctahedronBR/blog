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
					<input type="text" id="blogname" name="blogname" /> <br />
				</label>
				<label for="url">
					URL: <br />
					<input type="text" id="url" name="url" /> <br />
				</label>
				<label for="desc">
					Descrição: <br />
					<textarea id="desc" name="desc" ></textarea> <br />
				</label>
				<label for="lang">
					Língua: [e.g.: 'en', 'pt_BR', ...] <br />
					<input type="text" id="lang" name="lang" /> <br />
				</label>
				<input id="submit" type="submit" value="Salvar" />
			</fieldset>
		</form>
	</section>
{% endblock %}
