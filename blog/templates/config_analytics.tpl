{% extends "layout.tpl" %}
{% block header %}
		<title>{{config.blogname}} | Configurando analytics</title>
{% endblock %}
{% block scripts %}
	<script>
		head.js("http://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js", "/js/form.js");
	</script>
{% endblock %}
{% block body %}
	<section class="intern">
		<h2>Configuração analytics</h2>
		<form action="/config/analytics" method="post">
			<fieldset>
				<label for="key">
					Chave: <input type="text" name="key" value="{% if config.analytics %} {{ config.analytics }} {% endif %}"/> <br />
				</label>
				<input id="submit" type="submit" value="Salvar" />
			</fieldset>
		</form>
	</section>
{% endblock %}
