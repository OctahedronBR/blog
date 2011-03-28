{% extends "layout.tpl" %}
{% block header %}
		<title>{{config.blogname}} | Add link</title>
{% endblock %}
{% block scripts %}
	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>
	<script type="text/javascript" src="/js/form.js"></script>
{% endblock %}
{% block body %}
	<section class="intern">
		<h2>Adicionar Link</h2>
		<p class="warning"></p>
		<form action="/config/add_link" method="post">
			<fieldset>
				<label for="name">
					Nome <br />
					<input type="text" id="name" name="name" class="normal-width"/> <br />
				</label>
				<label for="url">
					URL <br />
					<input type="text" id="url" name="url" class="normal-width"/><br/ >
				</label>
				<input id="submit" type="submit" value="Criar" />
			</fieldset>
		</form>
	</section>
{% endblock %}
