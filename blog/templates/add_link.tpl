{% extends "layout.tpl" %}
{% block body %}
	<div class="section">
		<h2>Adicionar Link</h2>
		<div class="margin">
			<p class="warning"></p>
			<form action="/config/add_link" method="post">
				<fieldset>
					<label for="name">Nome</label> <br />
					<input type="text" name="name" class="normal-width"/> <br />
					<label for="url">URL</label> <br />
					<input type="text" name="url" class="normal-width"/><br/>
					<input id="submit" type="submit" value="Criar" />
				</fieldset>
			</form>
		</div>
	</div>
{% endblock %}
{% block scripts %}
	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>
	<script type="text/javascript" src="/js/form.js"></script>
{% endblock %}

