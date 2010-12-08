{% extends "layout.tpl" %}
{% block body %}
	<div class="section">
		<h2>Configuração twitter</h2>
		<div class="margin">
			<p class="warning">Antes você deve registrar sua aplicação no twitter!</p>
			<form action="/config/twitter" method="post">
				<fieldset>
					<label for="consumer_key">Consumer Key</label> <br />
					<input type="text" name="consumer_key" class="normal-width"/> <br />
					<label for="consumer_secret">Consumer Secret</label> <br />
					<input type="text" name="consumer_secret" class="normal-width"/> <br />
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
