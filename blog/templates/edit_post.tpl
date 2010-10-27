{% extends "layout.tpl" %}
{% block body %}
	<div class="section">
		<h2>Editar post</h2>
		<div class="margin">
			<p class="warning"></p>
			<form action="/post/update" method="post">
				<fieldset>
					<input type="hidden" name="key" value="{{ post.key() }}" class="normal-width"/>
					<label for="title">Título</label> <br />
					<input type="text" name="title" value="{{ post.title }}" class="normal-width"/> <br />
					<input type="text" name="slug" value="{{ post.slug }}" class="normal-width"/>
					<button id="slugify">Slugify!</button> <br />
					<label for="content">Conteúdo</label> <br />
					<textarea type="text" name="content" class="large-width">{{ post.coded_content }}</textarea> <br />
					<label for="tags">Tags</label> <br />
					<input type="text" name="tags" value="{{ tags }}" class="normal-width"/> <br />
					<input id="submit" type="submit" value="Atualizar" />
				</fieldset>
			</form>
		</div>
	</div>
{% endblock %}
{% block scripts %}
	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js"></script>
	<script type="text/javascript" src="/static/js/form.js"></script>
{% endblock %}

