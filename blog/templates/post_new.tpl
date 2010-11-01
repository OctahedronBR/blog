{% extends "layout.tpl" %}
{% block body %}
	<div class="section">
		<h2>Novo post</h2>
		<div class="margin">
			<p class="warning"></p>
			<form action="/post/create" method="post">
				<fieldset>
					<label for="title">Título</label> <br />
					<input type="text" name="title" class="normal-width"/> <br />
					<input type="text" name="slug" class="normal-width"/>
					<button id="slugify">Slugify!</button> <br />
					<label for="content">Conteúdo</label> <br />
					<textarea name="content" class="large-width"></textarea> <br />
					<label for="tags">Tags (e.g.: cloud computing, appengine, python)</label> <br />
					<input type="text" name="tags" class="normal-width"/> <br />
					<input type="checkbox" name="draft" value=True>Rascunho<br/>
					<input id="submit" type="submit" value="Criar" />
				</fieldset>
			</form>
		</div>
	</div>
{% endblock %}
{% block scripts %}
	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js"></script>
	<script type="text/javascript" src="/static/js/form.js"></script>
{% endblock %}

