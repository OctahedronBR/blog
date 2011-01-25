{% block stylesheet %}
	<link rel="stylesheet" type="text/css" href="/js/markitup/skins/markitup/style.css" />
	<link rel="stylesheet" type="text/css" href="/js/markitup/sets/bbcode/style.css" />
{% endblock %}
{% extends "layout.tpl" %}
{% block body %}
	<div class="section">
		<h2>Editar post</h2>
		<div class="margin">
			<p class="warning"></p>
			<form action="/post/update" method="post">
				<fieldset>
					<input type="hidden" name="key" value="{{ post.key() }}" class="normal-width"/>
					<label for="title">
						Título: <br />
						<input type="text" name="title" value="{{ post.title }}" class="normal-width"/> <br />
					</label>
					<input type="text" name="slug" value="{{ post.slug }}" class="normal-width"/>
					<button id="slugify">Slugify!</button> <br />
					<label for="content">
						Conteúdo: <a href="/help/bbcode" target="_blank">(BBCode?)</a> <br />
						<textarea type="text" name="content" class="large-width">{{ post.coded_content }}</textarea> <br />
					</label>
					<label for="tags">
						Tags: <br />
						<input type="text" name="tags" value="{{ tags }}" class="normal-width"/> <br />
					</label>
					<label for="draft">
						<input type="checkbox" name="draft" value="True" {% if draft %}checked{% endif %}/>Rascunho <br />
					</label>
					<input id="submit" type="submit" value="Salvar" />
				</fieldset>
			</form>
		</div>
	</div>
{% endblock %}
{% block scripts %}
	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>
	<script type="text/javascript" src="/js/form.js"></script>
	<script type="text/javascript" src="/js/markitup/jquery.markitup.js"></script>
	<script type="text/javascript" src="/js/markitup/sets/bbcode/set.js"></script>
{% endblock %}

