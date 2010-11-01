{% extends "layout.tpl" %}
{% block body %}
	<div class="section">
		<h2>Configuração inicial</h2>
		<div class="margin">
			<p class="warning"></p>
			<form action="/config/save" method="post">
				<fieldset>
					<label for="blogname">Nome do blog</label> <br />
					<input type="text" name="blogname" class="normal-width"/> <br />
					<label for="url">URL</label> <br />
					<input type="text" name="url" class="normal-width"/> <br />
					<label for="desc">Descrição</label> <br />
					<textarea name="desc" class="normal-width"></textarea> <br />
					<label for="lang">Língua [use 'en', 'pt_BR', ...]</label> <br />
					<input type="text" name="lang" class="tiny-width"/> <br />
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

