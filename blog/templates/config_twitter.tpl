{% extends "layout.tpl" %}
{% block header %}
		<title>{{config.blogname}} | Configurando Twitter API</title>
{% endblock %}
{% block scripts %}
	<script>
		head.js("http://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js", "/js/form.js");
	</script>
{% endblock %}
{% block body %}
	<section class="intern">
		<h2>Configuração twitter</h2>
		<p class="warning">Antes, você deve <a href="http://dev.twitter.com/apps/new">registrar sua aplicação</a> no Twitter!</p>
		<form action="/config/twitter" method="post">
			<fieldset>
				<label for="consumer_key">
					Consumer Key <br />
					<input type="text" id="consumer_key" name="consumer_key" value="{% if config.consumer_key %} {{ config.consumer_key }} {% endif %}"/> <br />
				</label>
				<label for="consumer_secret">
					Consumer Secret <br />
					<input type="text" id="consumer_secret" name="consumer_secret" value="{% if config.consumer_secret %}{{ config.consumer_secret }} {% endif %}"/> <br />
				</label>
				<input id="submit" type="submit" value="Salvar" />
			</fieldset>
		</form>
	</section>
{% endblock %}
